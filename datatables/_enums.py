# -*- coding: utf-8 -*-
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
t = open('reverse-login-chain/formats/枚举表.md', encoding='utf-8', errors='replace').read()
for fn in ['sub_5968A0', 'sub_596B70', 'sub_596C60', 'sub_596510', 'sub_5965F0', 'sub_5964A0', 'sub_596990', 'sub_596A80']:
    m = re.search(r'### `' + fn + r'`.*?(?=\n### |\Z)', t, re.S)
    print(m.group(0)[:1500] if m else (fn + ' NOT FOUND'))
    print('-----')
