# -*- coding: utf-8 -*-
"""_probe_w37_after.py —— #37 收口后的最终自检（只读）

① 行数 / 号形 / 连接键自洽（全部 = 自身 ID）
② 连接键 → #36 命中率（应为全集）
③ 种子文件字节级（CRLF、无 BOM、行数）+ 与库键集合双向差集
"""
import collections
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_settings.csv")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"

LINKS = ["effect_name_list", "hit_effect_list", "muzzle_effect_list", "trail_effect_list",
         "sound_set_list", "voice_set_list", "camera_shake_list", "screen_flash_list",
         "buff_effect_list", "debuff_effect_list", "spawn_effect_list"]


def main():
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute('SELECT btrim(weapon_setting_id) FROM cfg."WEAPON_SETTING"')
        keys = [r[0] for r in cur.fetchall()]
        print("① 行数 %d ／ 号形 %s"
              % (len(keys), dict(sorted(collections.Counter(len(k) for k in keys).items()))))

        bad = 0
        for c in LINKS:
            cur.execute('SELECT count(*) FROM cfg."WEAPON_SETTING"'
                        ' WHERE btrim("%s") <> btrim(weapon_setting_id)' % c)
            n = cur.fetchone()[0]
            bad += n
            print("   键==自身ID 不符的 %-22s : %d" % (c, n))
        print("   合计不符 %d  ⇒ %s" % (bad, "✓ 全自洽" if bad == 0 else "✗"))

        cur.execute('SELECT DISTINCT btrim(weapon_id_key) FROM cfg."WEAPON_BATTLE_DETAIL"')
        d36 = {r[0] for r in cur.fetchall()}
        hit = sum(1 for k in keys if k in d36)
        print()
        print("② 连接键 → #36 命中：%d / %d  %s"
              % (hit, len(keys), "✓" if hit == len(keys)
                 else "✗ 缺 %s" % sorted(set(keys) - d36)[:5]))

    print()
    with open(SEED, encoding="utf-8", newline="") as fh:
        raw = fh.read()
    data = [l for l in raw.split("\r\n") if l.strip() and not l.startswith("#")]
    print("③ 种子：数据行 %d ／ CRLF %d ／ 裸LF %d ／ 无BOM %s"
          % (len(data), raw.count("\r\n"), raw.count("\n") - raw.count("\r\n"),
             not raw.startswith("\ufeff")))
    ids = {l.split(",")[0].strip() for l in data}
    print("   与库键差集：种子独有 %s ／ 库独有 %s"
          % (sorted(ids - set(keys))[:6], sorted(set(keys) - ids)[:6]))
    for w in ("212301109", "212301110", "223005102"):
        print("   %s 在种子 %s ／ 在库 %s" % (w, w in ids, w in set(keys)))
    for w in ("12010101", "12840101", "13200151", "13200251"):
        print("   %s 在种子 %s ／ 在库 %s" % (w, w in ids, w in set(keys)))


if __name__ == "__main__":
    main()
