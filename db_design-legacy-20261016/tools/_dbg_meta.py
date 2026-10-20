# -*- coding: utf-8 -*-
import importlib.util
import json
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location('ic', r'F:\9ymsgo\9you\db_design\tools\import_commands.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

p = Path(r'F:\9ymsgo\9you\protocol_analysis\commands\SC-0x6FF7-lounge-clan_emblem_update_r\README.md')
for i, line in enumerate(p.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
    mm = re.match(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$", line)
    if not mm:
        continue
    k = mm.group(1).strip()
    print(i, json.dumps(k, ensure_ascii=True),
          'inKeys=', k in m.META_KEYS,
          'prefix=', k.startswith(m.META_KEY_PREFIXES))
print('prefixes:', json.dumps(list(m.META_KEY_PREFIXES), ensure_ascii=True))
