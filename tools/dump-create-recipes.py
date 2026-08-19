#!/usr/bin/env python3
"""
dump-create-recipes.py — pull every Create-family recipe out of an installed
Minecraft modpack, without launching the game.

Reads the .jar files in a mods folder, extracts:
  - data/<ns>/recipe/**.json        (recipes; 1.21+ path)
  - data/<ns>/recipes/**.json       (older path, just in case)
  - data/<ns>/tags/item/**.json     (so #tag ingredients can be resolved)
  - assets/<ns>/lang/en_us.json     (so ids can be shown as real names)

Keeps only namespaces that are actually Create-related, then writes a single
gzipped JSON bundle you can hand off.

Usage:
    python3 dump-create-recipes.py /path/to/instance/mods
    python3 dump-create-recipes.py /path/to/instance/mods --all      # no filtering
    python3 dump-create-recipes.py /path/to/instance/mods -o out.json.gz

No dependencies beyond the standard library.
"""

import argparse
import gzip
import json
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

CREATE_HINTS = ("create", "aeronautic", "sable", "railway", "steam_rail", "numismatic")

RECIPE_DIRS = ("recipe/", "recipes/")
TAG_DIRS = ("tags/item/", "tags/items/")


def looks_create(name: str) -> bool:
    n = name.lower()
    return any(h in n for h in CREATE_HINTS)


def walk_ids(obj):
    """Yield every string that looks like a namespaced id or #tag."""
    if isinstance(obj, str):
        if re.fullmatch(r"#?[a-z0-9_.-]+:[a-z0-9_./-]+", obj):
            yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from walk_ids(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_ids(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mods", help="path to the instance's mods folder")
    ap.add_argument("-o", "--out", default="create-recipes.json.gz")
    ap.add_argument("--all", action="store_true",
                    help="keep every namespace, not just Create-related ones")
    args = ap.parse_args()

    mods_dir = Path(args.mods).expanduser()
    if not mods_dir.is_dir():
        sys.exit(f"Not a folder: {mods_dir}")

    jars = sorted(mods_dir.glob("*.jar"))
    if not jars:
        sys.exit(f"No .jar files in {mods_dir}")
    print(f"Scanning {len(jars)} jars in {mods_dir}\n")

    recipes = defaultdict(dict)   # ns -> {recipe_id: recipe_json}
    tags = defaultdict(dict)      # ns -> {tag_id: [entries]}
    lang = {}                     # translation key -> english name
    bad = 0

    for jar in jars:
        try:
            zf = zipfile.ZipFile(jar)
        except zipfile.BadZipFile:
            print(f"  ! skipping unreadable jar: {jar.name}")
            continue

        with zf:
            for entry in zf.namelist():
                if not entry.endswith(".json"):
                    continue

                # ---- recipes ----
                m = re.match(r"data/([a-z0-9_.-]+)/(recipes?/)(.+)\.json$", entry)
                if m and m.group(2) in RECIPE_DIRS:
                    ns, rel = m.group(1), m.group(3)
                    try:
                        recipes[ns][f"{ns}:{rel}"] = json.loads(zf.read(entry))
                    except Exception:
                        bad += 1
                    continue

                # ---- item tags ----
                m = re.match(r"data/([a-z0-9_.-]+)/(tags/items?/)(.+)\.json$", entry)
                if m and m.group(2) in TAG_DIRS:
                    ns, rel = m.group(1), m.group(3)
                    try:
                        data = json.loads(zf.read(entry))
                        key = f"{ns}:{rel}"
                        prev = tags[ns].get(key, [])
                        tags[ns][key] = prev + data.get("values", [])
                    except Exception:
                        bad += 1
                    continue

                # ---- english names ----
                if re.match(r"assets/[a-z0-9_.-]+/lang/en_us\.json$", entry):
                    try:
                        for k, v in json.loads(zf.read(entry)).items():
                            if k.startswith(("item.", "block.", "fluid.")):
                                lang.setdefault(k, v)
                    except Exception:
                        bad += 1

    # ---------- decide which namespaces to keep ----------
    if args.all:
        keep = set(recipes)
    else:
        keep = {"create"}
        for ns, rs in recipes.items():
            if looks_create(ns):
                keep.add(ns)
                continue
            for r in rs.values():
                if looks_create(str(r.get("type", ""))):
                    keep.add(ns)
                    break
                if any(looks_create(i.split(":", 1)[0]) for i in walk_ids(r)):
                    keep.add(ns)
                    break
        keep &= set(recipes)

    kept_recipes = {ns: recipes[ns] for ns in sorted(keep)}
    kept_tags = {ns: tags[ns] for ns in sorted(tags) if ns in keep or ns in ("c", "minecraft", "neoforge")}

    # trim lang to things we might actually reference
    ns_prefixes = tuple(f"{p}.{ns}." for ns in keep | {"minecraft"} for p in ("item", "block", "fluid"))
    kept_lang = {k: v for k, v in lang.items() if k.startswith(ns_prefixes)}

    bundle = {
        "source": str(mods_dir),
        "jar_count": len(jars),
        "namespaces": sorted(keep),
        "recipes": kept_recipes,
        "item_tags": kept_tags,
        "lang": kept_lang,
    }

    out = Path(args.out).expanduser()
    with gzip.open(out, "wt", encoding="utf-8") as fh:
        json.dump(bundle, fh, separators=(",", ":"))

    # ---------- report ----------
    total = sum(len(v) for v in kept_recipes.values())
    print(f"{'namespace':<34}{'recipes':>8}")
    print("-" * 42)
    for ns in sorted(kept_recipes, key=lambda n: -len(kept_recipes[n])):
        n = len(kept_recipes[ns])
        if n:
            print(f"{ns:<34}{n:>8}")
    print("-" * 42)
    print(f"{'TOTAL':<34}{total:>8}")
    print(f"\nnames collected : {len(kept_lang)}")
    print(f"item tag files  : {sum(len(v) for v in kept_tags.values())}")
    if bad:
        print(f"unparsed files  : {bad}")
    print(f"\nWrote {out}  ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
