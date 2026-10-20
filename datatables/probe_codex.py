# -*- coding: utf-8 -*-
"""probe_codex.py —— 看 codex 数据里有没有"资源目录/模型"字段（能直接 join 練度ID ↔ unit）。"""
import glob
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
CD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'unpackdat', 'codex', 'data')
for p in sorted(glob.glob(os.path.join(CD, '*'))):
    print('===', os.path.basename(p), os.path.getsize(p), 'bytes')
    if p.endswith('.json'):
        d = json.load(open(p, encoding='utf-8'))
        if isinstance(d, dict):
            print('  顶层键:', list(d.keys())[:12])
            for k, v in d.items():
                if isinstance(v, list) and v:
                    print('  %s: list[%d]，元素键 = %s' % (k, len(v), list(v[0].keys()) if isinstance(v[0], dict) else type(v[0])))
                    if isinstance(v[0], dict):
                        # 找出可能含"资源/目录/模型"的字段值
                        for kk in v[0].keys():
                            val = str(v[0][kk])
                            if any(s in kk.lower() for s in ('model', 'res', 'chara', 'dir', 'path', 'mesh', 'id')):
                                print('     %-16s = %s' % (kk, val[:70]))
                        for u in v[:3]:
                            print('     样例:', {kk: str(u[kk])[:26] for kk in list(u.keys())[:8]})
    elif p.endswith(('.py', '.bat', '.js', '.html')) or os.path.isdir(p):
        pass
