# 用法：python3 build/build.py && python3 build/assemble.py  → 生成 site/index.html
import os
here = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(here, 'template.html'), encoding='utf-8').read()
d = open(os.path.join(here, 'data.json'), encoding='utf-8').read()
out = os.path.join(here, '..', 'site', 'index.html')
import base64, glob, json
bgs = ['data:image/jpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
       for f in sorted(glob.glob(os.path.join(here, '..', 'site', 'bg', 'bg*.jpg')), key=lambda x: int(os.path.basename(x)[2:-4]))]
forest = ['data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(here, '..', 'site', 'bg', 'forest', name + '.jpg'), 'rb').read()).decode() for name in ['crystal', 'valley', 'books', 'blossom']]
open(out, 'w', encoding='utf-8').write(t.replace('__DATA__', d).replace('__BG__', json.dumps(bgs)).replace('__FOREST_BG__', json.dumps(forest)))
print('wrote', os.path.normpath(out))
