import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from janome.tokenizer import Tokenizer
import q2026 as Q

T = Tokenizer()
FUNC_POS = {'助詞', '記号', '連体詞', 'フィラー'}

def tok_plain(text):
    out = []  # [surface, base, kind, headpos, pos1]
    for t in T.tokenize(text):
        p = t.part_of_speech.split(',')
        s = t.surface
        base = t.base_form if t.base_form != '*' else s
        if out:
            prev = out[-1]
            hp = prev[3]
            attach = False
            if prev[2] == 'w':
                if p[0] == '助動詞' and hp in ('動詞', '形容詞'):
                    attach = True
                elif p[0] == '動詞' and p[1] in ('非自立', '接尾') and hp in ('動詞', '形容詞'):
                    attach = True
                elif p[0] == '助詞' and p[1] == '接続助詞' and s in ('て', 'で') and hp in ('動詞', '形容詞'):
                    attach = True
                elif p[0] == '名詞' and p[1] == '接尾' and hp == '名詞':
                    attach = True
                elif p[0] == '形容詞' and p[1] in ('非自立', '接尾') and hp == '動詞':
                    attach = True
                elif p[0] == '動詞' and base == 'する' and hp == '名詞' and prev[4] == 'サ変接続':
                    attach = True
                    prev[1] = prev[1] + 'する'
                    prev[3] = '動詞'
                elif p[0] == '名詞' and p[1] == '数' and prev[4] == '数':
                    attach = True
                    prev[1] = prev[0] + s
            if attach:
                prev[0] += s
                if prev[3] == '名詞':
                    prev[1] = prev[0]
                continue
        kind = 'f' if (p[0] in FUNC_POS or p[0] == '助動詞' or s.strip() == '') else 'w'
        out.append([s, base, kind, p[0], p[1]])
    return [[a, b if b != a else '', k] for a, b, k, _, _ in out]

MARK = re.compile(r'【([^】]+)】|（　）|［(\d+)］|\n')

def tok(text):
    res = []
    pos = 0
    for m in MARK.finditer(text):
        if m.start() > pos:
            res += tok_plain(text[pos:m.start()])
        g = m.group(0)
        if g == '\n':
            res.append(['', '', 'n'])
        elif g == '（　）':
            res.append(['', '', 'b'])
        elif m.group(2):
            res.append([m.group(2), '', 'b'])
        else:
            w = m.group(1)
            b = ''
            tt = tok_plain(w)
            if tt and tt[0][1]:
                b = tt[0][1] if len(tt) == 1 else ''
            res.append([w, b, 'u'])
        pos = m.end()
    if pos < len(text):
        res += tok_plain(text[pos:])
    return res

import importlib
qs = []
passages = {}
for modname in ('q2026', 'q2512', 'q2507', 'q2412'):
    Q = importlib.import_module(modname)
    P = Q.PAPER
    n = 0
    def qid(n, P=P): return f"{P.replace('.', '-')}-{n:02d}"

    for m, typ, arr in ((1, 'read', Q.M1), (2, 'fill', Q.M2), (3, 'syn', Q.M3)):
        for (stem, zh, ans, opts, note) in arr:
            n += 1
            o = []
            for (t, k, z) in opts:
                o.append({'t': t, 'k': k or '', 'z': z or '', 'x': 1 if (k is None and z is None) else 0, 'tk': tok(t)})
            qs.append({'id': qid(n), 'p': P, 'm': m, 'n': n, 'ty': typ, 'stem': tok(stem), 'plain': stem.replace('【', '').replace('】', ''),
                       'zh': zh, 'ans': ans, 'opts': o, 'pt': note})

    for (w, rd, z, ans, sents, zhs) in Q.M4:
        n += 1
        o = [{'t': s.replace('【', '').replace('】', ''), 'tk': tok(s), 'z': zz} for s, zz in zip(sents, zhs)]
        qs.append({'id': qid(n), 'p': P, 'm': 4, 'n': n, 'ty': 'use', 'word': w, 'rd': rd, 'wz': z, 'stem': tok(w), 'plain': w,
                   'zh': f"{w}{'（'+rd+'）' if rd else ''}：{z}", 'ans': ans, 'opts': o, 'pt': ''})

    for (stem, zh, ans, opts, zs, pt) in Q.M5:
        n += 1
        o = [{'t': t, 'tk': tok(t), 'z': z} for t, z in zip(opts, zs)]
        qs.append({'id': qid(n), 'p': P, 'm': 5, 'n': n, 'ty': 'gram', 'stem': tok(stem), 'plain': stem.replace('\n', ' '),
                   'zh': zh, 'ans': ans, 'opts': o, 'pt': pt})

    for row in Q.M6:
        pre, post, pieces, order, zh, pt, nb = row[:7]; star = row[7] if len(row) > 7 else 3
        n += 1
        o = [{'t': t, 'tk': tok(t), 'z': ''} for t in pieces]
        full = pre + ''.join(pieces[i - 1] for i in order) + post
        qs.append({'id': qid(n), 'p': P, 'm': 6, 'n': n, 'ty': 'sort', 'pre': tok(pre), 'post': tok(post),
                   'plain': (pre + ''.join('★' if j == star - 1 else '＿' for j in range(4)) + post).replace('\n', ' '), 'full': full, 'starAt': len(pre) + sum(len(pieces[i - 1]) for i in order[:star - 1]), 'order': order, 'star': star, 'ans': order[star - 1],
                   'zh': zh, 'opts': o, 'pt': pt + (('\n' + nb) if nb else '')})

    pid = P + '-m7'
    passages[pid] = {'intro': Q.M7_INTRO, 'tk': tok(Q.M7_PASSAGE)}
    for (blank, ans, opts, zs, zh, pt) in Q.M7:
        n += 1
        o = [{'t': t, 'tk': tok(t), 'z': z} for t, z in zip(opts, zs)]
        qs.append({'id': qid(n), 'p': P, 'm': 7, 'n': n, 'ty': 'text', 'pid': pid, 'blank': blank,
                   'plain': f'文章空格［{blank}］', 'zh': zh, 'ans': ans, 'opts': o, 'pt': pt})

data = {'questions': qs, 'passages': passages}
out = os.path.join(os.path.dirname(__file__), 'data.json')
json.dump(data, open(out, 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(qs), os.path.getsize(out))
