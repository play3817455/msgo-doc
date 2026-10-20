# -*- coding: utf-8 -*-
"""判定真库 #36 的取值口径：把「干净 sidecar（wiki 面板值）」按 IDA 推导的
「面板→客户端原值」换算，逐条与真库对照；再补两道哨：

  ① 换算命中率 —— `have`（真库）必须 **100%** 等于 `want`（sidecar 经换算）；
  ② 原值域哨 —— 真库每一行都要落在 `weapon_client_raw.RAW_DOMAIN` 内
     （域外 = 面板刻度直写/错列残渣，读侧会算出离谱的连射冷却、装填时间、锁定距离）；
  ③ CSV ↔ 库 漂移 —— `weapon_battle_detail.csv` 与库的 `(键, 属性)` 集合/取值必须逐条相同
     （CSV 是本管线的唯一权威；不一致就说明"净化只做了一半"）。

只报告，不写。
"""
import csv
import io
import os
import struct
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import weapon_client_raw as RAW  # noqa: E402

SIDE = os.path.join(HERE, "names", "武器分配明细.csv")
T36 = os.path.join(os.path.dirname(HERE), "server", "datafiles", "lounge", "item",
                   "weapon_battle_detail.csv")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
FAMS = list(RAW.FAMILIES_36)

# ---- 从 load_paired_ms_db.py 原样搬过来的换算（同常量、同算法）----
_F_500 = struct.unpack("<f", bytes.fromhex("0000FA43"))[0]
_F_0002 = struct.unpack("<f", bytes.fromhex("6F12033B"))[0]
_F_1000 = struct.unpack("<f", bytes.fromhex("00007A44"))[0]
_F_2 = struct.unpack("<f", bytes.fromhex("00000040"))[0]
_F_0526 = struct.unpack("<f", bytes.fromhex("A2BC063F"))[0]
_F_1500 = struct.unpack("<f", bytes.fromhex("0080BB44"))[0]
_F_10 = struct.unpack("<f", bytes.fromhex("00002041"))[0]
_F_001 = struct.unpack("<f", bytes.fromhex("0AD7233C"))[0]
_F_04 = struct.unpack("<f", bytes.fromhex("CDCCCC3E"))[0]
_STAB_K = _F_0002 * _F_1000
_RAPID_K = _F_0526 * _F_1500


def _trunc(x):
    return int(x) if x >= 0 else -int(-x)


def _best(lo, hi, score):
    bx, be = None, None
    steps = 4000
    for i in range(steps + 1):
        x = lo + (hi - lo) * i / steps
        e = abs(score(x))
        if be is None or e < be:
            bx, be = x, e
            if e == 0:
                break
    return bx


def c_power(w):
    n = int(float(w))
    sign = -1 if n < 0 else 1
    mag = abs(n)
    raw = int(round(mag / 10.0))
    best = raw
    for c in range(max(0, raw - 2), raw + 3):
        if abs(c * 10 - mag) < abs(best * 10 - mag):
            best = c
    return "0" if best == 0 and n == 0 else str(sign * best)


def c_stab(w):
    t = int(float(w))
    guess = _F_500 - (t + 0.1) / _STAB_K

    def disp(m):
        return _trunc((_F_500 - m) * _STAB_K + _F_04)
    mem = _best(guess - 2, guess + 2, lambda m: disp(m) - t)
    return "%.6f" % (mem / 100.0)


def c_rapid(w):
    t = int(float(w))
    guess = _F_2 - (t - _F_04) / _RAPID_K

    def disp(x):
        return _trunc((_F_2 - x) * _RAPID_K + _F_04)
    return "%.6f" % _best(guess - 0.05, guess + 0.05, lambda v: disp(v) - t)


def c_reload(w):
    t = int(float(w))
    guess = _F_10 - (t - _F_04) / 100.0

    def disp(x):
        return _trunc((_F_10 - x) * 100.0 + _F_04)
    return "%.6f" % _best(guess - 0.05, guess + 0.05, lambda v: disp(v) - t)


def c_lock(w):
    t = int(float(w))

    def disp(csv):
        return _trunc(float(csv) * _F_001 * _F_1000 + _F_04)
    return "%.6f" % _best(t / 10.0 - 0.2, t / 10.0 + 0.2, lambda v: disp(v) - t)


def num(s):
    s = (s or "").strip()
    if not s or s in ("~", "-", "—", "－"):
        return ""
    out = []
    for ch in s:
        if ch.isdigit() or ch == ".":
            out.append(ch)
            if len(out) > 12:
                break
        elif out:
            break
    return "".join(out)


CONV = [
    (10, "POWER", c_power),
    (13, "RANGE", None),
    (11, "STABILITY", c_stab),
    (12, "RAPIDDELAY", c_rapid),
    (14, "RELOAD", c_reload),     # 「装填性能」；该格空则回退 col15「装填时间」（两列严格互斥）
    (16, "LOCKON_CAM", c_lock),
    (17, "HIGH_LOCKON", None),
]


def main():
    rows = [r for r in csv.reader(open(SIDE, encoding="utf-8", errors="replace"))
            if r and r[0].strip().isdigit() and len(r) >= 18]
    conn = psycopg.connect(DSN)
    cur = conn.cursor()
    cur.execute("""select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value)
                     from cfg."WEAPON_BATTLE_DETAIL" """)
    db = {}
    for k, a, v in cur.fetchall():
        db[(int(k), a)] = v
    conn.close()

    hit = {a: [0, 0] for _, a, _ in CONV}
    sample = []
    for r in rows:
        wid = int(r[1])
        for col, attr, fn in CONV:
            v = num(r[col])
            if not v and attr == "RELOAD":
                # ★回退列，与 `weapon_client_raw.SIDECAR_36_FALLBACK` 同口径：
                #   维基老页面表头写「装填時間」、新页面写「装填性能」，同一白字。
                v = num(r[15])
            if not v:
                continue
            want = fn(v) if fn else v
            have = db.get((wid, attr))
            if have is None:
                continue
            hit[attr][1] += 1
            if have == want or (have.replace(".000000", "") == want.replace(".000000", "")):
                hit[attr][0] += 1
            elif len(sample) < 24 and attr in ("POWER", "RANGE", "STABILITY", "RAPIDDELAY", "RELOAD", "LOCKON_CAM"):
                sample.append((wid, attr, v, want, have))
    print("=== ① 换算命中率（want = 干净 sidecar 经 IDA 换算，have = 真库）===")
    for _, a, _ in CONV:
        h, t = hit[a]
        print("  %-12s %4d / %4d  (%.0f%%)" % (a, h, t, 100.0 * h / max(1, t)))
    print()
    print("=== ①b 不一致样本（wiki列值 / 应写 / 库里）===")
    for wid, attr, v, want, have in sample:
        print("  %-10d %-12s wiki=%-8s 应=%-14s 库=%s" % (wid, attr, v, want, have))

    # ---- ② 原值域哨（真库全表）----
    print()
    print("=== ② 原值域哨（weapon_client_raw.RAW_DOMAIN）===")
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value)
                         from cfg."WEAPON_BATTLE_DETAIL" """)
        bad = {}
        n = {}
        cbad = {}
        cn = {}
        for k, a, v in cur.fetchall():
            if a not in FAMS:
                continue
            n[a] = n.get(a, 0) + 1
            if not RAW.is_raw_domain(a, v):
                bad.setdefault(a, []).append((k, v))
    # ★下发件也要过同一道哨：CSV 是客户端要下载的那份（`download_list.csv` 里的
    #   `WEAPON_BATTLE_DETAIL`），库里干净而 CSV 里留面板刻度同样会毒到客户端。
    for r in csv.reader(open(T36, encoding="utf-8", errors="replace")):
        if len(r) > 2 and r[0].strip() in FAMS and r[1].strip().isdigit():
            cn[r[0].strip()] = cn.get(r[0].strip(), 0) + 1
            if not RAW.is_raw_domain(r[0].strip(), r[2].strip()):
                cbad.setdefault(r[0].strip(), []).append((r[1].strip(), r[2].strip()))
    print("  %-12s %17s %17s" % ("属性", "真库（域外/行）", "下发件（域外/行）"))
    for a in FAMS:
        print("  %-12s %10d / %-5d %9d / %-5d %s"
              % (a, len(bad.get(a, [])), n.get(a, 0), len(cbad.get(a, [])), cn.get(a, 0),
                 (cbad.get(a, []) or bad.get(a, []))[:3] or '✓'))

    # ---- ③ CSV ↔ 库 漂移 ----
    print()
    print("=== ③ CSV ↔ 库 漂移（#36 八族，逐 (键, 属性)）===")
    csvp = {}
    for r in csv.reader(open(T36, encoding="utf-8", errors="replace")):
        if len(r) > 2 and r[0].strip() and not r[0].startswith("#") and r[1].strip().isdigit():
            csvp[(int(r[1].strip()), r[0].strip())] = r[2].strip()
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value)
                         from cfg."WEAPON_BATTLE_DETAIL" """)
        dbp = {}
        for k, a, v in cur.fetchall():
            if a in FAMS and k.isdigit():
                dbp[(int(k), a)] = v

    def same(x, y):
        """同值判据：先按数字比（`570` == `570.000000`），不是数字才逐字比。"""
        if x == y:
            return True
        try:
            return abs(float(x) - float(y)) < 1e-9
        except (TypeError, ValueError):
            return False

    only_db = sorted(set(dbp) - set(csvp))
    only_csv = sorted(set(csvp) - set(dbp))
    valdiff = sorted(k for k in set(dbp) & set(csvp) if not same(dbp[k], csvp[k]))
    print("  CSV pair %d / 库 pair %d" % (len(csvp), len(dbp)))
    print("  只在库 %d %s" % (len(only_db), only_db[:8]))
    print("  只在 CSV %d %s" % (len(only_csv), only_csv[:8]))
    print("  值不同 %d %s" % (len(valdiff), [(k, dbp[k], csvp[k]) for k in valdiff[:8]]))

    # 分族判：sidecar 族 = 本管线**管**的键（必须逐行同值）；8 位 icon-id 族 = 由库里回灌。
    side_keys = set()
    for r in csv.reader(open(SIDE, encoding="utf-8-sig", errors="replace")):
        if len(r) > 1 and r[1].strip() and not r[0].startswith("#"):
            side_keys.add(int(r[1].strip().lstrip("\ufeff")))
    for tag, sel in (("sidecar 族（本管线管）", lambda k: k[0] in side_keys),
                     ("8 位 icon-id 族（库→CSV 回灌）", lambda k: k[0] not in side_keys)):
        od = [k for k in only_db if sel(k)]
        oc = [k for k in only_csv if sel(k)]
        vd = [k for k in valdiff if sel(k)]
        mark = "✓" if not (od or oc or vd) else "✗"
        print("  %s：只在库 %d / 只在 CSV %d / 值不同 %d %s"
              % (tag, len(od), len(oc), len(vd), mark))


if __name__ == "__main__":
    main()
