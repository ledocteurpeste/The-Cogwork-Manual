#!/usr/bin/env python3
import gzip, json, re, collections

import argparse
ap = argparse.ArgumentParser(description='Match tooltip, Ponder scene and advancement text onto known items.')
ap.add_argument('--text-gz', default='data/raw/create-text.json.gz', help='input gz from dump-create-text.py')
ap.add_argument('--payload', default='data/payload.json', help='payload.json from build_recipes.py (defines the known item catalog)')
ap.add_argument('--out', default='data/wiki.json', help='output wiki json')
args = ap.parse_args()

TXT = json.load(gzip.open(args.text_gz, 'rt'))
L, PONDER_RAW, ADV = TXT['lang'], TXT['ponder'], TXT['advancements']

payload = json.load(open(args.payload))
S = payload['S']
SSET = set(S)
byns = collections.defaultdict(list)
for s in S:
    if ':' in s:
        byns[s.split(':', 1)[0]].append(s.split(':', 1)[1])

def clean(t):
    if not isinstance(t, str):
        return t
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'_(.+?)_', r'<b>\1</b>', t)
    return t.strip()

# ---------------- tooltips ----------------
TIP = {}
per = collections.defaultdict(dict)
for k, v in L.items():
    m = re.match(r'(item|block)\.([a-z0-9_]+)\.([a-z0-9_.]+)\.tooltip\.(\w+?)(\d*)$', k)
    if not m:
        continue
    ns, path, kind, idx = m.group(2), m.group(3), m.group(4), m.group(5)
    cand = f'{ns}:{path}'
    if cand not in SSET:
        continue
    per[cand][(kind, int(idx) if idx else 0)] = v

for iid, d in per.items():
    summary = d.get(('summary', 0))
    pairs = []
    n = 1
    while ('behaviour', n) in d:
        pairs.append([clean(d[('behaviour', n)]), clean(d.get(('condition', n)))])
        n += 1
    if summary or pairs:
        TIP[iid] = {'s': clean(summary), 'p': pairs}

# ---------------- ponder scenes ----------------
scenes = collections.defaultdict(dict)
for k, v in PONDER_RAW.items():
    m = re.match(r'([a-z0-9_]+)\.ponder\.([a-z0-9_]+)\.(header|text_\d+)$', k)
    if m:
        scenes[(m.group(1), m.group(2))][m.group(3)] = v

def resolve_scene(ns, sid):
    for c in (f'{ns}:{sid}', f'create:{sid}'):
        if c in SSET:
            return c
    # exact path match in exactly one namespace
    hits = [f'{n2}:{sid}' for n2, paths in byns.items() if sid in paths]
    if len(hits) == 1:
        return hits[0]
    # prefix match: sid startswith <item_path>_ , longest wins, same-ns preferred
    best, best_len = None, 0
    for n2 in (ns, 'create'):
        for p in byns.get(n2, []):
            if sid == p or (sid.startswith(p + '_') and len(p) > best_len):
                best, best_len = f'{n2}:{p}', len(p)
    if best:
        return best
    return None

PONDER = collections.defaultdict(list)
for (ns, sid), parts in scenes.items():
    if 'header' not in parts:
        continue
    iid = resolve_scene(ns, sid)
    if not iid:
        continue
    lines = [parts['header']]
    n = 1
    while f'text_{n}' in parts:
        lines.append(parts[f'text_{n}'])
        n += 1
    if len(lines) < 2:
        continue
    PONDER[iid].append({'h': clean(lines[0]), 't': [clean(x) for x in lines[1:]]})

# cap to avoid a wall of repeated scenes on any one item
for iid in PONDER:
    PONDER[iid] = PONDER[iid][:4]

# ---------------- advancements ----------------
def lang_resolve(field):
    if isinstance(field, dict):
        field = field.get('translate') or field.get('fallback')
    if not isinstance(field, str):
        return None
    return L.get(field, field if not field.startswith('advancements.') else None)

ADVOUT = collections.defaultdict(list)
for aid, v in ADV.items():
    icon = v.get('icon')
    if icon not in SSET:
        continue
    title = lang_resolve(v.get('title'))
    desc = lang_resolve(v.get('desc'))
    if title:
        ADVOUT[icon].append({'t': clean(title), 'd': clean(desc) if desc else None})
for iid in ADVOUT:
    ADVOUT[iid] = ADVOUT[iid][:3]

# ---------------- combine ----------------
WIKI = {}
for iid in sorted(SSET):
    e = {}
    if iid in TIP: e['tip'] = TIP[iid]
    if iid in PONDER: e['pon'] = PONDER[iid]
    if iid in ADVOUT: e['adv'] = ADVOUT[iid]
    if e: WIKI[iid] = e

out = json.dumps(WIKI, separators=(',', ':'))
open(args.out, 'w').write(out)

print('items with tooltip     :', len(TIP))
print('items with ponder notes:', len(PONDER))
print('items with advancement :', len(ADVOUT))
print('items with ANY new text:', len(WIKI))
print('wiki.json size          : %.1f KB' % (len(out) / 1024))

# spot check
for t in ['create:crushing_wheel', 'create:mechanical_saw', 'create:wrench',
          'create:goggles', 'create:andesite_alloy', 'dndecor:andesite_frontlight']:
    print('\n---', t, '---')
    print(json.dumps(WIKI.get(t, 'NONE'), indent=1)[:600])
