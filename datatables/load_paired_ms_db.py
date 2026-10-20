# -*- coding: utf-8 -*-
"""把「武器编号已全部配对」的机体参数写入 serverv 的 cfg 库。

筛选：gow_wiki/data/units.json 里，每条有名称的武器行都有 8 位 icon_id，
并且机体有 7 位練度ID。只改这些机体；其余机体的行不动。

写入（已有行则更新，没有则插入）：
  cfg."CHARA_PARAM"          搭载量、装甲基值；空着的战斗明细键补成練度ID
  cfg."MSMA_BATTLE_DETAIL"   面板第一档（强化上限不入库）
  cfg."ITEM"                 武器物品；sort_group 空则写成物品号（图标号）
  cfg."WEAPON_BATTLE_DETAIL" 威力/射程/集弹/连射/装填/锁定（wiki 第一档）
  cfg."WEAPON_SETTING"       类别、持握；弹数须另经明确wiki绑定写col104/105
  cfg."MSMA_WEAPONSET"       用配对到的物品号换掉该机体原来的武器组

同一物品号在多台机体上数值不一致时，取出现次数最多的第一档。
不写类别基线、不猜盾的复合列、不猜倒地值。
"""
import collections
import io
import json
import os
import re
import struct
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UNITS = os.path.join(ROOT, "gow_wiki", "data", "units.json")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"

TIER = re.compile(r"^\s*(-?\d+(?:\.\d+)?)")
CLS = [
    ("SHIELD", r"シールド|盾|shield"),
    ("WRESTLE", r"サーベル|セイバー|ナギナタ|ブレイド|ソード|剣|軍刀|军刀|剑|剑刃|薙刀|鞭|锤|ハンマー|saber|blade|クロー"),
    ("REPAIR", r"リペア|回復|修理|修复|補給|补给"),
    ("RADARPOD", r"レーダー|雷达"),
    ("CAMERAGUN", r"カメラ|撮影|摄影"),
    ("LANDMINE", r"機雷|地雷"),
    ("HAND_THROW", r"グレネード|手榴弾|手雷|破片|閃光|闪光|投擲|投掷|炸弾|爆雷"),
    ("SHOTGUN", r"ショットガン|散弾|散弹|霰弹|shotgun"),
    ("BEAM_SNIPE", r"狙撃用ビーム|ビーム狙撃|光束狙击"),
    ("SNIPER_RIFLE", r"スナイパー|狙撃|狙击|sniper"),
    ("BEAM_SPRAYGUN", r"スプレー|拡散ビーム|光束喷枪|光束喷涂|喷枪|スプレーガン"),
    ("BEAM_RIFLE", r"ビームライフル|ビーム・ライフル|ビームガン|メガ粒子砲|メガ|米加|光束步枪|光束枪|光束手枪|手枪|步枪|ライフル|ピストル"),
    ("SUBMACHINEGUN", r"冲锋枪|短機関|サブマシンガン"),
    ("MACHINEGUN", r"マシンガン|機関砲|ガトリング|バルカン|机枪|机关炮|加特林|火神炮"),
    ("CHARGE_BAZOOKA", r"チャージバズーカ"),
    ("BAZOOKA", r"バズーカ|ロケット砲|火箭|バズ"),
    ("CHARGE_RIFLE", r"チャージライフル|チャージ"),
    ("MISSILE", r"ミサイル|导弹|誘導弾"),
    ("HOWITZER", r"キャノン|加農|加农|榴弾|榴弹|砲|炮"),
    ("TRENCH_MORTAR", r"迫撃|臼炮"),
]
CC = [(n, re.compile(p, re.I)) for n, p in CLS]
C28_2_C52 = {
    "MACHINEGUN": "MACHINEGUN", "SUBMACHINEGUN": "MACHINEGUN",
    "SHOTGUN": "SHOTGUN", "BEAM_RIFLE": "BEAM", "BEAM_SPRAYGUN": "BEAM",
    "CHARGE_RIFLE": "BEAM", "BEAM_SNIPE": "SNIPE", "SNIPER_RIFLE": "SNIPE",
    "BAZOOKA": "BAZOOKA", "CHARGE_BAZOOKA": "BAZOOKA", "HOWITZER": "BAZOOKA",
    "MISSILE": "MISSILE", "TRENCH_MORTAR": "TRENCH_MORTAR",
    "HAND_THROW": "HAND_THROW", "LANDMINE": "LANDMINE", "WRESTLE": "WRESTLE",
    "SHIELD": "SHIELD", "REPAIR": "REPAIR", "RADARPOD": "RADAR", "CAMERAGUN": "CAMERAGUN",
}
GRIP = {"SHIELD": "SHIELD", "WRESTLE": "TWOHAND", "BAZOOKA": "SHOLDER",
        "TRENCH_MORTAR": "SHOLDER", "MISSILE": "SHOLDER"}
PANEL = {
    "armor": "アーマー", "speed": "最高速度", "boost": "ブースト容量",
    "payload": "積載量", "boost_cd": "ブーストチャージ",
    "return_val": "緊急帰投性能", "time": "TIME", "cost": "COST",
}
DETAIL = [
    ("RESPAWN_TIME", "time", "int"),
    ("MAX_HP", "armor", "int"),
    ("MOVE", "speed", "float"),
    ("BOOST_GAUGEMAX", "boost", "int"),
    ("BOOST_GAUGEHEAL", "boost_cd", "float"),
    ("COST", "cost", "int"),
    ("WARP_TIME", "return_val", "int"),
]
SLOT = [
    ("battle_detail_key_respawn", "time"),
    ("battle_detail_key_warp", "return_val"),
    ("battle_detail_key_cost", "cost"),
    ("battle_detail_key_max_hp", "armor"),
    ("battle_detail_key_energy", "armor"),
    ("battle_detail_key_move", "speed"),
    ("battle_detail_key_boost_gaugemax", "boost"),
    ("battle_detail_key_boost_gaugeheal", "boost_cd"),
    ("battle_detail_key_boost_speed", "speed"),
]
WIKI_ATTR = [
    ("威力", "POWER", "int"),
    ("射程距離", "RANGE", "float"),
    ("集弾性能", "STABILITY", "float"),
    ("連射速度", "RAPIDDELAY", "float"),
    ("リロード時間", "RELOAD", "float"),
    ("ロックオン", "LOCKON_CAM", "float"),
    ("ロック範囲", "HIGH_LOCKON", "float"),
]


def first_tier(v):
    s = str(v or "").strip().replace(",", "").replace("，", "")
    if not s or s in ("~", "-", "—", "－"):
        return ""
    m = TIER.match(s)
    return m.group(1) if m else ""


def as_num(tv, kind):
    if not tv:
        return ""
    if kind == "int":
        return str(int(float(tv)))
    return tv if "." in tv else tv + ".000000"


# 机库白字不是 CSV 原样。下面把 wiki 显示值换成客户端原值。
# 威力原值×10；集弹 (500-原值)×2；连射/冷却 (2-原值)×0.526315808×1500；
# 装填 (10-原值)×100；锁定原值×10（读入时先×0.01）。射程、红锁不在这六行里，保持显示值。
_F_500 = struct.unpack("<f", bytes.fromhex("0000FA43"))[0]
_F_0002 = struct.unpack("<f", bytes.fromhex("6F12033B"))[0]
_F_1000 = struct.unpack("<f", bytes.fromhex("00007A44"))[0]
_F_2 = struct.unpack("<f", bytes.fromhex("00000040"))[0]
_F_0526 = struct.unpack("<f", bytes.fromhex("A2BC063F"))[0]
_F_1500 = struct.unpack("<f", bytes.fromhex("0080BB44"))[0]
_F_10 = struct.unpack("<f", bytes.fromhex("00002041"))[0]
_F_01 = struct.unpack("<f", bytes.fromhex("CDCCCC3D"))[0]
_F_001 = struct.unpack("<f", bytes.fromhex("0AD7233C"))[0]
_F_04 = struct.unpack("<f", bytes.fromhex("CDCCCC3E"))[0]
_STAB_K = _F_0002 * _F_1000
_RAPID_K = _F_0526 * _F_1500


def _trunc(x):
    return int(x) if x >= 0 else -int(-x)


def _best(lo, hi, score):
    best_x, best_err = None, None
    steps = 4000
    span = hi - lo
    for i in range(steps + 1):
        x = lo + span * i / steps
        err = abs(score(x))
        if best_err is None or err < best_err:
            best_x, best_err = x, err
            if err == 0:
                break
    return best_x


def client_power(wiki):
    n = int(float(wiki))
    sign = -1 if n < 0 else 1
    mag = abs(n)
    raw = int(round(mag / 10.0))
    best = raw
    for cand in range(max(0, raw - 2), raw + 3):
        if abs(cand * 10 - mag) < abs(best * 10 - mag):
            best = cand
    return "0" if best == 0 and n == 0 else str(sign * best)


def client_stability_csv(wiki):
    target = int(float(wiki))

    def disp(mem):
        return _trunc((_F_500 - mem) * _STAB_K + _F_04)

    guess = _F_500 - (target + 0.1) / _STAB_K
    mem = _best(guess - 2, guess + 2, lambda m: disp(m) - target)
    return ("%.6f" % (mem / 100.0))


def client_rapid_csv(wiki):
    target = int(float(wiki))

    def disp(x):
        return _trunc((_F_2 - x) * _RAPID_K + _F_04)

    guess = _F_2 - (target - _F_04) / _RAPID_K
    x = _best(guess - 0.05, guess + 0.05, lambda v: disp(v) - target)
    return "%.6f" % x


def client_reload_csv(wiki):
    target = int(float(wiki))

    def disp(x):
        return _trunc((_F_10 - x) * 100.0 + _F_04)

    guess = _F_10 - (target - _F_04) / 100.0
    x = _best(guess - 0.05, guess + 0.05, lambda v: disp(v) - target)
    return "%.6f" % x


def client_lock_csv(wiki):
    target = int(float(wiki))

    def disp(csv):
        stored = float(csv) * _F_001
        return _trunc(stored * _F_1000 + _F_04)

    guess = target / 10.0
    x = _best(guess - 0.2, guess + 0.2, lambda v: disp(v) - target)
    return "%.6f" % x


def client_battle_value(attr, wiki):
    if attr == "POWER":
        return client_power(wiki), ""
    if attr == "STABILITY":
        csv = client_stability_csv(wiki)
        return csv, csv
    if attr == "RAPIDDELAY":
        return client_rapid_csv(wiki), ""
    if attr == "RELOAD":
        return client_reload_csv(wiki), ""
    if attr == "LOCKON_CAM":
        return client_lock_csv(wiki), ""
    return wiki, ""


# Hangar 緊急帰投 label (sub_7CE560) is
# trunc((flt_E018E8 - raw) * flt_E01918 * flt_D76150 + flt_E01914).
# Wiki 緊急帰投性能 is that label, so WARP_TIME stores the raw preimage.
_WARP_E = struct.unpack("<f", bytes.fromhex("0000c841"))[0]
_WARP_K = struct.unpack("<f", bytes.fromhex("8c2e3a3d"))[0]
_WARP_M = struct.unpack("<f", bytes.fromhex("00007a44"))[0]
_WARP_B = struct.unpack("<f", bytes.fromhex("5c8f023f"))[0]


def warp_client_raw(display):
    """Client raw whose hangar label is the wiki number, or the nearest representable label.

    The label steps by about 45, so some wiki integers have no exact raw.
    """
    shown = int(display)
    scale = _WARP_K * _WARP_M
    guess = int(round(_WARP_E - shown / scale))
    best = guess
    best_err = None
    for raw in range(guess - 6, guess + 7):
        got = int((_WARP_E - raw) * scale + _WARP_B)
        err = abs(got - shown)
        if best_err is None or err < best_err:
            best = raw
            best_err = err
    return str(best)


def panel_value(u, key):
    raw = (u.get("panel") or {}).get(PANEL[key])
    if isinstance(raw, list):
        raw = raw[0] if raw else ""
    return as_num(first_tier(raw), "float" if key in ("speed", "boost_cd") else "int")


def classify(name):
    for n, rx in CC:
        if rx.search(name or ""):
            return n
    return "MACHINEGUN"


def weapon_rows(u):
    out = []
    for g in u.get("weapons") or []:
        for r in g.get("rows") or []:
            name = (r.get("名称") or "").strip()
            if name and name != "~":
                out.append(r)
    return out


def fully_paired(u):
    rs = weapon_rows(u)
    did = (u.get("dev_id") or "").strip()
    if not rs or not (len(did) == 7 and did.isdigit()):
        return False
    return all(len(str(r.get("icon_id") or "")) == 8 and str(r["icon_id"]).isdigit() for r in rs)


def winner(counter):
    if not counter:
        return ""
    best = max(counter.values())
    return sorted(k for k, v in counter.items() if v == best)[0]


def canon_item(icon_id):
    n = int(icon_id)
    if 0 < n < 100_000_000:
        return "%08d" % n
    return str(n)


def key_expr(col):
    return (
        "CASE WHEN btrim(%s) ~ '^[0-9]{1,8}$' THEN lpad(btrim(%s), 8, '0') ELSE btrim(%s) END"
        % (col, col, col)
    )


def row_ids(cur, table, col, iid):
    cur.execute(
        'select _row_id from cfg."%s" where %s = %%s order by _row_id' % (table, key_expr(col)),
        (iid,),
    )
    return [r[0] for r in cur.fetchall()]


def main():
    units = json.load(open(UNITS, encoding="utf-8"))
    chosen = [u for u in units if fully_paired(u)]
    votes = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    names = collections.defaultdict(collections.Counter)
    cats = collections.defaultdict(collections.Counter)
    for u in chosen:
        seen = set()
        for r in weapon_rows(u):
            iid = canon_item(r["icon_id"])
            if iid in seen:
                continue
            seen.add(iid)
            name = (r.get("名称") or "").strip()
            names[iid][name] += 1
            cats[iid][classify(name)] += 1
            for key, attr, kind in WIKI_ATTR:
                tv = as_num(first_tier(r.get(key)), kind)
                if tv:
                    votes[iid][attr][tv] += 1

    conn = psycopg.connect(DSN)
    conn.autocommit = False
    cur = conn.cursor()
    cur.execute('select btrim(msma_id) from cfg."CHARA_PARAM"')
    have = {r[0] for r in cur.fetchall()}
    n_item_upd = n_item_ins = n_wbd = n_ws_upd = n_ws_ins = 0
    for iid, by_attr in votes.items():
        name = winner(names[iid])
        item_rows = row_ids(cur, "ITEM", "item_id", iid)
        if item_rows:
            cur.execute(
                """update cfg."ITEM"
                      set item_id=%s, sort_group=%s, name=%s, item_type='WEAPON'
                    where _row_id=%s""",
                (iid, iid, name, item_rows[0]))
            if len(item_rows) > 1:
                cur.execute('delete from cfg."ITEM" where _row_id = any(%s)', (item_rows[1:],))
            n_item_upd += 1
        else:
            cur.execute(
                """insert into cfg."ITEM" (item_id, sort_group, name, description, item_type, stack_limit, linked_table_id, icon_variant)
                   values (%s,%s,%s,'','WEAPON','','','')""",
                (iid, iid, name))
            n_item_ins += 1
        for attr, counter in by_attr.items():
            val = winner(counter)
            if not val:
                continue
            stored, extra = client_battle_value(attr, val)
            cur.execute(
                'delete from cfg."WEAPON_BATTLE_DETAIL" where %s = %%s and btrim(attr_name)=%%s'
                % key_expr("weapon_id_key"),
                (iid, attr))
            cur.execute(
                'insert into cfg."WEAPON_BATTLE_DETAIL" (attr_name, weapon_id_key, attr_value, attr_value_2) values (%s,%s,%s,%s)',
                (attr, iid, stored, extra))
            n_wbd += 1
            if attr == "RAPIDDELAY":
                cur.execute(
                    'delete from cfg."WEAPON_BATTLE_DETAIL" where %s = %%s and btrim(attr_name)=%%s'
                    % key_expr("weapon_id_key"),
                    (iid, "COOLTIME"))
                cur.execute(
                    'insert into cfg."WEAPON_BATTLE_DETAIL" (attr_name, weapon_id_key, attr_value, attr_value_2) values (%s,%s,%s,%s)',
                    ("COOLTIME", iid, stored, ""))
                n_wbd += 1
        c28 = winner(cats[iid]) or "MACHINEGUN"
        c52 = C28_2_C52.get(c28, "MACHINEGUN")
        grip = GRIP.get(c52, "ONEHAND")
        set_rows = row_ids(cur, "WEAPON_SETTING", "weapon_setting_id", iid)
        if set_rows:
            cur.execute(
                """update cfg."WEAPON_SETTING"
                      set weapon_setting_id = %s,
                          model_id_lo = %s,
                          equip_slot_type = %s,
                          weapon_category = %s,
                          ammo_type_id = '1',
                          effect_name_list = %s,
                          hit_effect_list = %s,
                          muzzle_effect_list = %s,
                          trail_effect_list = %s,
                          sound_set_list = %s,
                          voice_set_list = %s,
                          camera_shake_list = %s,
                          screen_flash_list = %s,
                          buff_effect_list = %s,
                          debuff_effect_list = %s,
                          spawn_effect_list = %s
                    where _row_id = %s""",
                (iid, str(int(iid)), grip, c52,
                 iid, iid, iid, iid, iid, iid, iid, iid, iid, iid, iid,
                 set_rows[0]))
            if len(set_rows) > 1:
                cur.execute('delete from cfg."WEAPON_SETTING" where _row_id = any(%s)', (set_rows[1:],))
            n_ws_upd += 1
        else:
            cur.execute(
                """insert into cfg."WEAPON_SETTING"
                     (weapon_setting_id, parent_setting_id, model_id_lo, equip_slot_type, weapon_category, ammo_type_id,
                      effect_name_list, hit_effect_list, muzzle_effect_list, trail_effect_list,
                      sound_set_list, voice_set_list, camera_shake_list, screen_flash_list,
                      buff_effect_list, debuff_effect_list, spawn_effect_list)
                   values (%s,'0',%s,%s,%s,'1',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (iid, str(int(iid)), grip, c52,
                 iid, iid, iid, iid, iid, iid, iid, iid, iid, iid, iid))
            n_ws_ins += 1

    n_unit = n_detail = n_wrows = n_skip = 0
    over = []
    for u in chosen:
        did = u["dev_id"]
        if did not in have:
            n_skip += 1
            continue
        fields = {k: panel_value(u, k) for k in PANEL}
        sets = []
        args = []
        if fields["payload"]:
            sets.append("payload_capacity_base = %s")
            args.append(fields["payload"])
        if fields["armor"]:
            sets.append("armor_base = %s")
            args.append(fields["armor"])
        for col, key in SLOT:
            if not fields.get(key) and key != "armor":
                continue
            sets.append(
                col + " = case when btrim(coalesce(" + col + ",'')) = '' then %s else " + col + " end")
            args.append(did)
        if sets:
            args.append(did)
            cur.execute('update cfg."CHARA_PARAM" set ' + ", ".join(sets) + " where btrim(msma_id)=%s", args)
        for attr, key, kind in DETAIL:
            val = fields.get(key) or ""
            if kind == "int" and val.endswith(".000000"):
                val = val[:-7]
            if not val:
                continue
            if attr == "WARP_TIME":
                val = warp_client_raw(val)
            cur.execute(
                'update cfg."MSMA_BATTLE_DETAIL" set entry_value=%s where btrim(attribute_name)=%s and btrim(entry_key)=%s',
                (val, attr, did))
            if cur.rowcount == 0:
                cur.execute(
                    'insert into cfg."MSMA_BATTLE_DETAIL" (attribute_name, entry_key, entry_value) values (%s,%s,%s)',
                    (attr, did, val))
            n_detail += 1
        for attr, val in (("ENERGY", "1000"), ("BOOST_SPEED", "0.840000")):
            cur.execute(
                'select 1 from cfg."MSMA_BATTLE_DETAIL" where btrim(attribute_name)=%s and btrim(entry_key)=%s',
                (attr, did))
            if cur.fetchone() is None:
                cur.execute(
                    'insert into cfg."MSMA_BATTLE_DETAIL" (attribute_name, entry_key, entry_value) values (%s,%s,%s)',
                    (attr, did, val))
                n_detail += 1
        weapons = []
        seen = set()
        for r in weapon_rows(u):
            iid = canon_item(r["icon_id"])
            if iid in seen:
                continue
            seen.add(iid)
            weapons.append((iid, classify(r.get("名称") or "")))
        if len(weapons) > 30:
            over.append((u["name"], did, len(weapons)))
        cur.execute('delete from cfg."MSMA_WEAPONSET" where btrim(weapon_group_id)=%s', (did,))
        for i, (iid, c28) in enumerate(weapons):
            cur.execute(
                """insert into cfg."MSMA_WEAPONSET"
                     (weapon_group_id, weapon_item_id, slot_category, weapon_category, enabled, sort_priority, region_gate)
                   values (%s,%s,%s,%s,'1',%s,'CHINA')""",
                (did, iid, "MAIN" if i == 0 else "EX", c28, str(i)))
            n_wrows += 1
        n_unit += 1

    cur.execute(
        """
        update cfg."WEAPON_BATTLE_DETAIL" d
           set weapon_id_key = lpad(btrim(d.weapon_id_key), 8, '0')
         where btrim(d.weapon_id_key) ~ '^[0-9]{1,7}$'
           and exists (
             select 1 from cfg."ITEM" i
              where btrim(i.item_id) = lpad(btrim(d.weapon_id_key), 8, '0')
           )
           and not exists (
             select 1 from cfg."WEAPON_BATTLE_DETAIL" e
              where btrim(e.weapon_id_key) = lpad(btrim(d.weapon_id_key), 8, '0')
                and btrim(e.attr_name) = btrim(d.attr_name)
           )
        """
    )
    cur.execute(
        """
        delete from cfg."WEAPON_BATTLE_DETAIL" d
         where btrim(d.weapon_id_key) ~ '^[0-9]{1,7}$'
           and exists (
             select 1 from cfg."ITEM" i
              where btrim(i.item_id) = lpad(btrim(d.weapon_id_key), 8, '0')
           )
        """
    )
    conn.commit()
    cur.execute(
        """select weapon_item_id, slot_category, weapon_category
             from cfg."MSMA_WEAPONSET" where btrim(weapon_group_id)='1101011' order by _row_id""")
    gm = cur.fetchall()
    cur.execute(
        """select attr_name, attr_value from cfg."WEAPON_BATTLE_DETAIL"
            where btrim(weapon_id_key)='01010401' order by attr_name""")
    mg = cur.fetchall()
    conn.close()
    print("全部配对 %d 台，写入机体 %d，库里没有这台練度ID %d" % (len(chosen), n_unit, n_skip))
    print("物品 更新 %d / 新建 %d ；武器数值行 %d ；武器设定 更新 %d / 新建 %d" % (
        n_item_upd, n_item_ins, n_wbd, n_ws_upd, n_ws_ins))
    print("武器组行 %d ；超过 30 把的机体 %d" % (n_wrows, len(over)))
    for row in over[:8]:
        print("  ", row)
    print("吉姆武器组", gm)
    print("100mm机枪数值", mg)
    conn2 = psycopg.connect(DSN)
    c2 = conn2.cursor()
    c2.execute(
        """select btrim(item_id), btrim(item_type), btrim(name)
             from cfg."ITEM"
            where btrim(item_id) in ('03010101','3010101','04010101','4010101')
            order by item_id""")
    print("喷枪/军刀物品", c2.fetchall())
    conn2.close()


if __name__ == "__main__":
    main()
