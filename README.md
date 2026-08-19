# The Cogwork Manual

A steampunk-themed, offline-first mobile reference for the **All of Create**
CurseForge modpack (Minecraft 1.21.1 / NeoForge). Every recipe, tooltip and
Ponder explanation is read directly out of the pack's own mod jars — nothing
here is guessed or hand-transcribed.

**[→ Open the app](docs/cogwork-manual.html)** (or enable GitHub Pages, see below)

## What's in here

```
docs/
  cogwork-manual.html    the built app — a single self-contained HTML file
data/
  raw/                   the raw extraction dumps from your Minecraft instance
  payload.json           compact recipe/item data the app embeds
  wiki.json              tooltip / Ponder scene / advancement text, matched to items
tools/
  dump-create-recipes.py reads recipe JSON straight out of the mod jars
  dump-create-text.py    reads tooltip, Ponder and advancement text out of the jars
  build_recipes.py       raw dump -> data/payload.json
  build_wiki.py          raw dump + payload.json -> data/wiki.json
  gen.py                 payload.json + wiki.json -> docs/cogwork-manual.html
```

## Using the app

Open `docs/cogwork-manual.html` in Safari (not the Files app preview — it needs
a real browser to run its JavaScript), then Share → **Add to Home Screen** for
a full-screen, offline app icon. See the GitHub Pages option below for a way
to do this without a local file server.

## Rebuilding it

Only needed if you update the modpack, add mods, or want to regenerate after
editing the hand-written guide text in `tools/gen.py`.

```bash
# 1. Extract raw data from your own Minecraft instance (once per pack update)
python3 tools/dump-create-recipes.py /path/to/instance/mods -o data/raw/create-recipes.json.gz
python3 tools/dump-create-text.py /path/to/instance/minecraft -o data/raw/create-text.json.gz

# 2. Process it
python3 tools/build_recipes.py
python3 tools/build_wiki.py
python3 tools/gen.py
```

Each tool takes `--help` for its options; all of them default to the paths
shown in the layout above, so running them with no arguments from the repo
root just works.

## Hosting it on GitHub Pages

Instead of copying the HTML file around by hand, you can serve it straight
from this repo:

1. Push this repo to GitHub.
2. Repo Settings → Pages → Source: **Deploy from a branch**, branch `main`,
   folder `/docs`.
3. GitHub gives you a URL like `https://<you>.github.io/<repo>/cogwork-manual.html`.
4. Open that URL in Safari on your phone, then Share → **Add to Home Screen**.

That gets you a stable HTTPS link that updates automatically every time you
push a new build, with no file-syncing app required in between.

## A note on the data

`data/` and `docs/cogwork-manual.html` contain recipe names, tooltip text and
Ponder scene text extracted from ~200 third-party mod jars, each under its own
license. The build tooling and the app's own code are yours to do what you
like with, but if you ever want to make this repo **public**, it's worth
checking a few of the bigger mods' licenses first — most Minecraft mod
licenses are fine with this kind of reference use, but not all of them permit
redistributing extracted data wholesale. A private repo sidesteps the question
entirely.
