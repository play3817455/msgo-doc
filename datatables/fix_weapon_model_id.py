# -*- coding: utf-8 -*-
"""武器小图标文件名是 s%08d(模型号)。weapon_settings 的模型号原先写死为 1，
客户端就只打开 s00000001。这里把已配对武器的模型号改成武器自己的编号。
"""
import hashlib
import json
import os

import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNITS = os.path.join(ROOT, "gow_wiki", "data", "units.json")
CSV = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_settings.csv")
ICON = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat", "interface", "icon", "item", "s")
DSN = "postgres://postgres:admin123@127.0.0.1:5432/msgo"


def canon(n):
    n = int(n)
    if 0 < n < 100_000_000:
        return "%08d" % n
    return str(n)


def paired_ids():
    units = json.load(open(UNITS, encoding="utf-8"))
    out = set()
    for u in units:
        rows = []
        for g in u.get("weapons") or []:
            for r in g.get("rows") or []:
                name = (r.get("名称") or "").strip()
                if name and name != "~":
                    rows.append(r)
        did = (u.get("dev_id") or "").strip()
        if not rows or not (len(did) == 7 and did.isdigit()):
            continue
        if not all(len(str(r.get("icon_id") or "")) == 8 and str(r["icon_id"]).isdigit() for r in rows):
            continue
        for r in rows:
            out.add(canon(r["icon_id"]))
    return out


def main():
    want = paired_ids()
    raw = open(CSV, "rb").read()
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    text = raw.decode("utf-8-sig")
    lines = text.splitlines()
    template = None
    seen = set()
    changed = 0
    out = []
    for line in lines:
        if not line or line.startswith("#"):
            out.append(line)
            continue
        parts = line.split(",")
        if not parts[0].isdigit():
            out.append(line)
            continue
        if template is None and len(parts) > 20:
            template = parts
        c = canon(parts[0])
        if c in want:
            while len(parts) < 3:
                parts.append("")
            parts[2] = str(int(parts[0]))
            line = ",".join(parts)
            seen.add(c)
            changed += 1
        out.append(line)
    missing = sorted(want - seen)
    if template is None:
        raise SystemExit("weapon_settings.csv has no data row to clone")
    for c in missing:
        row = list(template)
        row[0] = str(int(c))
        row[1] = "0"
        row[2] = str(int(c))
        if len(row) > 3:
            row[3] = "0"
        out.append(",".join(row))
    conn = psycopg.connect(DSN)
    cur = conn.cursor()
    cur.execute(
        """select btrim(weapon_setting_id), btrim(equip_slot_type), btrim(weapon_category)
             from cfg."WEAPON_SETTING"
            where btrim(weapon_setting_id) ~ '^[0-9]+$'"""
    )
    meta = {}
    for sid, grip, cat in cur.fetchall():
        meta[canon(sid)] = (grip or "ONEHAND", cat or "MACHINEGUN")
    fixed_cat = 0
    rebuilt = []
    for line in out:
        if not line or line.startswith("#"):
            rebuilt.append(line)
            continue
        parts = line.split(",")
        if not parts[0].isdigit() or len(parts) < 33 or parts[3] != "0":
            rebuilt.append(line)
            continue
        c = canon(parts[0])
        grip, cat = meta.get(c, ("ONEHAND", "MACHINEGUN"))
        parts[13] = grip
        parts[21] = cat
        rebuilt.append(",".join(parts))
        fixed_cat += 1
    # second pass: copy fire-mode / damage from an older row of the same category
    by_cat = {}
    for line in rebuilt:
        if not line or line.startswith("#"):
            continue
        parts = line.split(",")
        if len(parts) < 33 or not parts[0].isdigit() or parts[3] == "0":
            continue
        if parts[21] and parts[30]:
            by_cat.setdefault(parts[21], (parts[30], parts[32] if len(parts) > 32 else ""))
    out = []
    for line in rebuilt:
        if not line or line.startswith("#"):
            out.append(line)
            continue
        parts = line.split(",")
        if len(parts) >= 33 and parts[0].isdigit() and parts[3] == "0":
            pair = by_cat.get(parts[21])
            if pair:
                parts[30] = pair[0]
                if len(parts) > 32:
                    parts[32] = pair[1]
            line = ",".join(parts)
        out.append(line)
    print("appended rows recategorized", fixed_cat)
    conn.close()
    body = nl.join(s.encode("utf-8") for s in out) + nl
    open(CSV, "wb").write(body)

    conn = psycopg.connect(DSN)
    conn.autocommit = False
    cur = conn.cursor()
    cur.execute(
        """update cfg."WEAPON_SETTING"
              set model_id_lo = ltrim(btrim(weapon_setting_id), '0')
            where btrim(weapon_setting_id) ~ '^[0-9]+$'
              and length(ltrim(btrim(weapon_setting_id), '0')) <= 8
              and lpad(btrim(weapon_setting_id), 8, '0') = any(%s)""",
        (list(want),),
    )
    n_db = cur.rowcount
    digest = hashlib.sha256(body).hexdigest()
    cur.execute(
        """select file, filepath from meta.cfg_manifest
            where filepath like '%weapon_settings.csv'"""
    )
    mans = cur.fetchall()
    for file_id, path in mans:
        cur.execute(
            """update meta.cfg_manifest
                  set raw_csv = %s, sha256 = %s, row_count = %s, loaded_at = now()
                where file = %s""",
            (body, digest, len(out), file_id),
        )
    conn.commit()
    sample = ["01010401", "03010101", "02711603", "04010101"]
    print("csv rows rewritten", changed, "appended", len(missing), "db model_id_lo", n_db)
    print("manifest", mans)
    for s in sample:
        print(s, "dds", os.path.exists(os.path.join(ICON, "s%s.dds" % s)))
    conn.close()


if __name__ == "__main__":
    main()
