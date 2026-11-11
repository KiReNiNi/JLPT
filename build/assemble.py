# 用法：python3 build/build.py && python3 build/assemble.py  → 生成 site/index.html
import os
here = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(here, 'template.html'), encoding='utf-8').read()
d = open(os.path.join(here, 'data.json'), encoding='utf-8').read()
out = os.path.join(here, '..', 'site', 'index.html')
open(out, 'w', encoding='utf-8').write(t.replace('__DATA__', d))
print('wrote', os.path.normpath(out))
