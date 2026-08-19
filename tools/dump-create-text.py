#!/usr/bin/env python3
"""
dump-create-text.py — second pass. Pulls the *descriptive* text out of a
modpack: tooltips, Create ponder scenes, Patchouli guidebooks, advancement
descriptions, and the pack's FTB quest book.

Run it pointed at the same instance as before:

    python3 dump-create-text.py ~/snap/prismlauncher-alpo/common/instances/"All of Create"/minecraft

It finds mods/ and config/ underneath that path automatically.
Writes create-text.json.gz. Standard library only.
"""

import argparse, gzip, json, re, sys, zipfile
from collections import defaultdict
from pathlib import Path


def read_json(b):
    try:
        return json.loads(b.decode("utf-8-sig"))
    except Exception:
        try:
            # some packs ship JSON5-ish quest files with trailing commas
            t = b.decode("utf-8-sig", "replace")
            t = re.sub(r",(\s*[}\]])", r"\1", t)
            return json.loads(t)
        except Exception:
            return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("instance", help="the .minecraft / minecraft folder of the instance")
    ap.add_argument("-o", "--out", default="create-text.json.gz")
    args = ap.parse_args()

    root = Path(args.instance).expanduser()
    if not root.is_dir():
        sys.exit(f"Not a folder: {root}")

    mods = root / "mods"
    if not mods.is_dir():
        # maybe they pointed at the instance root
        for cand in (root / "minecraft" / "mods", root / ".minecraft" / "mods"):
            if cand.is_dir():
                mods = cand
                root = cand.parent
                break
    if not mods.is_dir():
        sys.exit(f"No mods folder under {root}")

    jars = sorted(mods.glob("*.jar"))
    print(f"Reading {len(jars)} jars from {mods}\n")

    lang = {}              # every en_us key, unfiltered
    ponder = {}            # create.ponder.* and addon equivalents
    books = defaultdict(dict)   # patchouli entries
    advancements = {}
    bad = 0

    for jar in jars:
        try:
            zf = zipfile.ZipFile(jar)
        except zipfile.BadZipFile:
            print(f"  ! unreadable: {jar.name}")
            continue
        with zf:
            for e in zf.namelist():
                if not e.endswith(".json"):
                    continue

                if re.match(r"assets/[a-z0-9_.-]+/lang/en_us\.json$", e):
                    j = read_json(zf.read(e))
                    if not isinstance(j, dict):
                        bad += 1; continue
                    for k, v in j.items():
                        if not isinstance(v, str):
                            continue
                        if ".ponder." in k or k.startswith("ponder."):
                            ponder.setdefault(k, v)
                        else:
                            lang.setdefault(k, v)
                    continue

                m = re.match(r"(?:assets|data)/([a-z0-9_.-]+)/patchouli_books/(.+)\.json$", e)
                if m:
                    j = read_json(zf.read(e))
                    if j is None:
                        bad += 1; continue
                    books[m.group(1)][m.group(2)] = j
                    continue

                m = re.match(r"data/([a-z0-9_.-]+)/advancements?/(.+)\.json$", e)
                if m:
                    j = read_json(zf.read(e))
                    if isinstance(j, dict) and "display" in j:
                        d = j["display"]
                        advancements[f"{m.group(1)}:{m.group(2)}"] = {
                            "title": d.get("title"),
                            "desc": d.get("description"),
                            "icon": (d.get("icon") or {}).get("id") or (d.get("icon") or {}).get("item"),
                        }
                    continue

    # ---------- quest books & pack config ----------
    quests = {}
    cfg = root / "config"
    for pat in ("ftbquests/**/*.snbt", "ftbquests/**/*.json",
                "questbook/**/*.snbt", "betterquesting/**/*.json"):
        for f in cfg.glob(pat):
            try:
                quests[str(f.relative_to(cfg))] = f.read_text("utf-8", "replace")
            except Exception:
                bad += 1
    # KubeJS scripts often hold the pack's custom recipes/tweaks
    kjs = {}
    for f in (root / "kubejs").rglob("*.js"):
        try:
            kjs[str(f.relative_to(root / "kubejs"))] = f.read_text("utf-8", "replace")
        except Exception:
            bad += 1

    bundle = {
        "lang": lang,
        "ponder": ponder,
        "patchouli": {k: v for k, v in books.items()},
        "advancements": advancements,
        "quests": quests,
        "kubejs": kjs,
    }

    out = Path(args.out).expanduser()
    with gzip.open(out, "wt", encoding="utf-8") as fh:
        json.dump(bundle, fh, separators=(",", ":"))

    tips = sum(1 for k in lang if ".tooltip" in k or ".description" in k or ".desc" in k)
    print(f"lang keys        : {len(lang)}")
    print(f"  of which tips  : {tips}")
    print(f"ponder lines     : {len(ponder)}")
    print(f"patchouli books  : {sum(len(v) for v in books.values())} entries "
          f"across {len(books)} mods")
    print(f"advancements     : {len(advancements)}")
    print(f"quest files      : {len(quests)}")
    print(f"kubejs scripts   : {len(kjs)}")
    if bad:
        print(f"unparsed         : {bad}")
    print(f"\nWrote {out}  ({out.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
