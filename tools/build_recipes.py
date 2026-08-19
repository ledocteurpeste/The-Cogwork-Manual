#!/usr/bin/env python3
import gzip, json, re, collections

import argparse
ap = argparse.ArgumentParser(description='Convert the raw Create recipe dump into the compact payload the app embeds.')
ap.add_argument('--gz', default='data/raw/create-recipes.json.gz', help='input gz from dump-create-recipes.py')
ap.add_argument('--out', default='data/payload.json', help='output compact payload json')
args = ap.parse_args()

d = json.load(gzip.open(args.gz, 'rt'))
RECIPES, TAGS, LANG = d['recipes'], d['item_tags'], d['lang']

# ---------- names ----------
def nice(idstr):
    if idstr.startswith('#'):
        return 'Any ' + idstr.split(':')[-1].replace('_', ' ').replace('/', ' ')
    ns, path = idstr.split(':', 1)
    for pre in ('block', 'item', 'fluid'):
        k = f'{pre}.{ns}.{path.replace("/", ".")}'
        if k in LANG:
            return LANG[k]
    return path.replace('_', ' ').title()

# ---------- tag expansion ----------
TAGMAP = {}
for ns, files in TAGS.items():
    for tid, vals in files.items():
        TAGMAP.setdefault(tid, [])
        TAGMAP[tid].extend(vals)

def expand(tag, depth=0, seen=None):
    seen = seen or set()
    if depth > 4 or tag in seen:
        return []
    seen.add(tag)
    out = []
    for v in TAGMAP.get(tag, []):
        if isinstance(v, dict):
            v = v.get('id', '')
        if not isinstance(v, str) or not v:
            continue
        if v.startswith('#'):
            out.extend(expand(v[1:], depth + 1, seen))
        else:
            out.append(v)
    return out

# ---------- ingredient parsing ----------
def ing_id(o, depth=0):
    if depth > 5: return None
    if isinstance(o, str):
        return o if ':' in o else None
    if isinstance(o, list):
        for x in o:
            r = ing_id(x, depth+1)
            if r: return r
        return None
    if not isinstance(o, dict):
        return None
    if 'tag' in o and isinstance(o['tag'], str):
        return '#' + o['tag']
    for k in ('item', 'id', 'fluid'):
        if k in o:
            v = o[k]
            if isinstance(v, str) and ':' in v: return v
            r = ing_id(v, depth+1)
            if r: return r
    return None

def out_entry(o):
    if isinstance(o, str):
        return (o, 1, None) if ':' in o else None
    if not isinstance(o, dict):
        return None
    i = ing_id(o)
    if not i:
        return None
    cnt = o.get('count', 1)
    if not isinstance(cnt, int): cnt = 1
    amt = o.get('amount')
    if isinstance(amt, int) and amt > 1: cnt = amt
    ch = o.get('chance')
    if not isinstance(ch, (int, float)): ch = None
    return (i, cnt, ch)

# ---------- normalise ----------
S, SI = [], {}
def sid(x):
    if x not in SI:
        SI[x] = len(S); S.append(x)
    return SI[x]

TYPES, TI = [], {}
def tid(x):
    if x not in TI:
        TI[x] = len(TYPES); TYPES.append(x)
    return TI[x]

recs = []
for ns, rs in RECIPES.items():
    for rid, r in sorted(rs.items()):
        t = r.get('type', '?')
        outs, ins, pat, key = [], [], None, None

        # outputs
        for src in (r.get('results'), r.get('result')):
            if src is None: continue
            for o in (src if isinstance(src, list) else [src]):
                e = out_entry(o)
                if e: outs.append(e)
        if not outs: continue

        # shaped grids
        if 'pattern' in r and 'key' in r:
            pat = r['pattern']
            key = {}
            for ch, v in r['key'].items():
                i = ing_id(v)
                if i: key[ch] = sid(i)
            for i in key.values():
                pass
            counts = collections.Counter(''.join(pat))
            for ch, ix in key.items():
                ins.append((ix, counts.get(ch, 1)))
        else:
            raw = r.get('ingredients') or r.get('ingredient')
            if raw is not None:
                for o in (raw if isinstance(raw, list) else [raw]):
                    i = ing_id(o)
                    if i:
                        amt = o.get('amount') if isinstance(o, dict) else None
                        ins.append((sid(i), amt or 1))
        # sequenced assembly: pull the whole sequence in as inputs
        seq = []
        if t == 'create:sequenced_assembly':
            for step in r.get('sequence', []):
                sing = [ing_id(x) for x in step.get('ingredients', [])]
                sing = [x for x in sing if x and 'incomplete' not in x]
                seq.append([step.get('type', '').split(':')[-1], [sid(x) for x in sing]])

        agg = {}
        order = []
        for ix, q in ins:
            if ix not in agg:
                agg[ix] = 0; order.append(ix)
            agg[ix] += q
        ins = [(ix, agg[ix]) for ix in order]

        flags = {}
        if r.get('heat_requirement'): flags['h'] = r['heat_requirement']
        if r.get('loops'): flags['l'] = r['loops']
        if seq: flags['q'] = seq
        if r.get('processing_time'): flags['p'] = r['processing_time']

        rec = [tid(t), [[sid(i), c, ch] for i, c, ch in outs], ins]
        if pat: rec.append([pat, key])
        else: rec.append(0)
        rec.append(flags or 0)
        recs.append(rec)

# ---------- item index ----------
mentioned = collections.Counter()
for rec in recs:
    for o in rec[1]: mentioned[rec and S[o[0]]] += 0
items = {}
for rec in recs:
    for o in rec[1]:
        items.setdefault(S[o[0]], 0)
    for i in rec[2]:
        items.setdefault(S[i[0]], 0)

NAMES = {}
for it in items:
    if it.startswith('#'):
        NAMES[it] = nice(it)
    else:
        NAMES[it] = nice(it)

# tag expansions, capped
TAGX = {}
for it in items:
    if it.startswith('#'):
        e = expand(it[1:])
        seen, uniq = set(), []
        for x in e:
            if x not in seen:
                seen.add(x); uniq.append(x)
        if uniq: TAGX[it] = uniq[:14]

payload = {
    'S': S,
    'T': TYPES,
    'R': recs,
    'N': NAMES,
    'G': TAGX,
}
raw = json.dumps(payload, separators=(',', ':'))
open(args.out, 'w').write(raw)
print('items indexed :', len(items))
print('recipes       :', len(recs))
print('strings       :', len(S))
print('types         :', len(TYPES))
print('tag expansions:', len(TAGX))
print('payload raw   : %.1f MB' % (len(raw) / 1048576))
print('payload gzip  : %.1f MB' % (len(gzip.compress(raw.encode())) / 1048576))

ns_counts = collections.Counter(i.split(':')[0] for i in items if not i.startswith('#'))
print('\ntop namespaces by item count:')
for n, c in ns_counts.most_common(70):
    print(f'  {n:<34}{c:>6}')
