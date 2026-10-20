#!/usr/bin/env python3
"""字节级模型 → 字段功能归位（域 → 对象 → 角色 → 关联）。

地基（只读，零改动）
====================
  * `schema/commands/*.json`    915 条命令：capabilities / direction / pair /
                                behavior[] / db_effects[] / fields[].composite_ref
  * `schema/composites/*.json`  132 个线布局：members[] 带 disposition + VA
  * `schema/entities/*.json`    73 个规范实体：alias_of / layout_same_as / wire_forms
  * `schema/_legacy_tables/tbl_*.json`  75 张旧提议表：row_key 声明（对象锚点来源）
  * `schema/_meta/legacy_evidence.json` 冻结的旧库证据（旧表声明 + 旧库唯一键列序/列清单）

产出（本模块只写 homing/，不动旧 tables/ 管线）
==============================================
  * `schema/homing/fields.jsonl`     归位表：一行一个字段实例
  * `schema/homing/objects/*.json`   对象模型（L2）
  * `schema/homing/relations.json`   表关联（FK）
  * `schema/homing/unresolved.md`    引擎判不了的（人工批次入口）
  * `schema/homing/summary.json`     覆盖率与门禁指标

三层口径（详见 `docs/05-字段归位与重做库.md`）
==============================================
  L1 域   —— 命令 capabilities[] 的 `域.` 前缀
  L2 对象 —— composites 折叠：other_wire_forms / layout_same_as / alias_of /
             prefix_of；row_key 表作「锚点」（A3 优先于 A2 的视图折叠）
  L3 角色 —— 十类闭集，按名字/线类型判定，每条带 VA
  D  写入归属 —— CS 写 / SC 读（实测零反例），db_effects 为权威覆盖

纪律
====
  1. 只认模型里已有的证据；判不定一律进 `unresolved.md`，禁止臆造。
  2. 不修改任何输入文件（幂等可重跑）。
  3. 命令模型零改动（WIRE_EPOCH / CHECK_EPOCH 不动）。

用法
====
  python tools/derive_homing.py --report          # 只统计，不写文件
  python tools/derive_homing.py --write           # 落 homing/
"""

from __future__ import annotations

import argparse
import collections
import datetime
import json
import re
import shutil
import sys
from pathlib import Path

SCHEMA = Path(__file__).resolve().parents[1] / "schema"
HOMING = SCHEMA / "homing"

# ---------------------------------------------------------------- 角色词表

ROLES = (
    "identity", "scope", "slot", "counter", "flag", "timestamp",
    "ref", "padding", "payload", "attribute",
)

# 对象级 disposition（docs/00 §3）。人工订正只允许在这几个值里选：
#   PERSIST → 建表；EVENT/TBD/TRANSIENT/DERIVED/CONFIG → 不进本轮 DDL。
DISPOSITIONS = ("PERSIST", "EVENT", "TBD", "TRANSIENT", "DERIVED", "CONFIG")

# 对象自身身份名的候选（决定 PK）。**只认「自己的记录号」**：
# `*_id` 一律不作 PK——那些是**指向别人**的引用（`clan_id`/`item_id`/`msma_id`），
# 误当 PK 会把「一名机师一条详情」错钉成「一个军团一条详情」（见 docs/05 §4.B）。
IDENT_NAMES = ("uniqid", "uniq_id", "id")

# 跨 schema 的作用域列（行主不变量，见 docs/05 §6.1）
CROSS_SCHEMA_TARGET = {
    "pilot_id": "core.pilot_registry.pilot_id",
    "world_id": "core.worlds.world_id",
}

# 主数据（静态配置）在 `schema/cfg/tables/*.json`，80 张。
# `X_id` 若命中 cfg 的主键列名，它是**指向静态配置的引用**，不是 `game.*` 外键：
# 目标表在 cfg schema、不由服务器写。口径见 docs/05 §4.E。
CFG_DIR = SCHEMA / "cfg" / "tables"

# 战斗期实体句柄：这类 id 指向**本场战斗内存里的实体**，不落库、无目标表。
# 只收 `ent`（entity）语义——上一版把 `msg_id`/`node_id` 也算进来是错的：
# 那些是 lounge 侧的消息/淘汰赛节点 id，属未决而不是战斗句柄。
RUNTIME_RE = re.compile(r"(^|_)(ent|entid|entity)(_?id)?$|_entid$")

# 「指向机师/世界」的名字形态：`master_pilotid` / `leader_pilot_id` → core 作用域表。
_PILOT_ID_RE = re.compile(r"(^|_)pilot_?id$|^pilotid$")
_WORLD_ID_RE = re.compile(r"(^|_)world_?id$|^worldid$")


def cfg_master_index() -> tuple[dict[str, list[str]], set[str]]:
    """主数据索引：`(主键列名 → cfg 表列表, cfg 表名集合)`。

    只收「第一列」（cfg 表的主键位，证据 `read_order` 最小），避免把普通列
    当主键——上一版用「列名前缀」命中，把 `clan_id` 错配到 `LVUP_CLAN`、
    `icon_id` 错配到 `FORCEGAUGE_INFO`，全是臆造。
    """
    by_pk: dict[str, list[str]] = collections.defaultdict(list)
    names: set[str] = set()
    if not CFG_DIR.is_dir():
        return {}, names
    for p in sorted(CFG_DIR.glob("*.json")):
        d = load(p)
        tid = str(d.get("id") or p.stem)
        names.add(norm(tid))
        cols = sorted(d.get("columns") or [],
                      key=lambda c: (c.get("read_order") or 99))
        pk = ""
        for c in cols:
            nm = c.get("name") or c.get("db_column") or ""
            if nm:
                pk = nm
                break
        if pk:
            by_pk[norm(pk)].append(tid)
    return dict(by_pk), names

# 值只是「指向别的对象的身份」的名字（不为自己建对象时当 FK 用）
SLOT_NAMES = frozenset((
    "slot", "deck_slot", "deck_set", "db_index", "inv_place",
    "equip_set_slot", "elem_index",
))
SCOPE_NAMES = frozenset(("world_id", "pilot_id"))
# 行键前缀顺序（行主不变量，见 docs/05 §6.1）：world_id 先于 pilot_id
SCOPE_ORDER = ("world_id", "pilot_id")
TIMESTAMP_NAMES = frozenset(("tm_sec", "tm_usec"))
PAD_RE = re.compile(r"^(pad|tail_pad|reserved|dummy|unused|_pad|spare|align)")
FLAG_RE = re.compile(r"^(is_|has_|can_|need_)")
FLAG_SUF_RE = re.compile(r"(_bits|_flg|_flag|_flags|_on)$")
COUNTER_RE = re.compile(r"(_cnt|_count|_num)$|^(count|num)$")
OPAQUE_TYPES = ("bytes", "blob", "opaque")

# 已知的引用词干 → 对象 id（人工锚，仅收确定无歧义的）。
# 逐词干的**业务裁决**不放这里，放 `_overrides.json.ref_stem`（数据而非代码，
# 且每条都要写理由——`clan` 一族五个派生表就是必须写理由的例子）。
STEM_ALIAS = {
    "unlocked_navi": "unlocked_navi",
}

# `_overrides.json.member_rows_in_root` 的运行时副本：`(父对象 id, 成员名)` → 裁决。
# 见 `set_member_roots` / `build_table_graph`：这些数组成员的**行**存在另一个对象的
# 根表里，所以既不建子表副本、父对象的 `keys.children` 里也不该有它。
_MEMBER_ROOT: dict[tuple[str, str], dict] = {}

# `_overrides.json.ref_stem` 的运行时副本：词干 → 裁决（kind/target/category/reason）
_REF_STEM: dict[str, dict] = {}
# 本轮真正被问到的词干（用于检出「已过期」的裁决：字段改名/消失后没人再查它）
_REF_STEM_HITS: set[str] = set()
# 归一化身份成员名 → 有该身份列的对象 id（`room_id` → [`roominfo`]）
_IDENT_INDEX: dict[str, list[str]] = {}


def set_ref_stem(ov: dict | None) -> None:
    """装载词干级引用裁决（`_overrides.json.ref_stem`）。"""
    global _REF_STEM
    _REF_STEM_HITS.clear()
    raw = (ov or {}).get("ref_stem") or {}
    _REF_STEM = {norm(k): v for k, v in raw.items()
                 if not str(k).startswith("_") and isinstance(v, dict)}


def set_ident_index(objects: dict[str, dict]) -> None:
    """建「身份成员名 → 对象」表。

    给 `X_id` 一条**很强的**兜底：字段名恰好是某个对象的身份列名（`room_id` 之于
    `roominfo`），就说明它指的是那个对象的行——比按词干模糊匹配对象名可靠得多
    （`room` 既不是 `coop_room` 的前缀、也不是 `roominfo` 的前缀，模糊规则看不到）。
    """
    global _IDENT_INDEX
    idx: dict[str, list[str]] = {}
    for oid, o in objects.items():
        for x in o["members"]:
            if x.get("role") == "identity":
                idx.setdefault(norm(x["name"]), []).append(oid)
    _IDENT_INDEX = idx


def set_member_roots(objects: dict[str, dict], m: Model, ov: dict | None) -> list[str]:
    """装载 `_overrides.json.member_rows_in_root`：**数组成员的行在别人的根表里**。

    问题形态（docs/05 §4.G 第 4 项，`unlockw` 是唯一一例）：一个复合体既是 `X.y[3]`
    的元素类型（被父对象当数组引用 → 引擎按「父表__成员名」建子表副本），又在 SC 报文里
    以顶层数组出现、且有**自己的行键声明**（→ 旧表守恒又给它建了一张根表）。两张表装
    同一批行：写方落在哪一张，另一张就是没人维护的副本，迟早漂移。

    这类成员的**行键来自元素自己的字段**（`unlockw.db_index`＝「数据库索引」，且
    `SC-0x45E4/0x81FB` 的应答就是 `(uniqid_ms, item_id, db_index)` 三元组 ⇒ 行键是
    `(uniqid_ms, db_index)`），父记录里那 3 格只是**定长线形上的平铺视图**（48A4 的元素
    是 416B 定长记录，装不下 30 格；A832 顶层数组才是那 30 格的全量）。两条先例同向：
    `item`（真槽位列 `inv_place` 胜过合成数组下标）、`avatar`（保留写方落点那张表，
    退休多余副本，见 `retire_tables`）。

    写法：

        {"parent": "ms_rokaku", "member": "weapons", "object": "unlockw",
         "retire_child_table": "game.ms_rokaku__weapons",
         "writers": ["CS-0x550A-..."], "readers": ["SC-0xA832-..."],
         "reason": "...", "evidence_va": "..."}

    效果：
      * `build_table_graph.expand` 不再为该成员建子表，改记一条 `view_of_root` 链接；
      * `_project_base` 不把它算进父对象的 `keys.children`；
      * `object` 的形状**升为 root**（它的行有自己的表，不随父行键）；行键仍由
        `pk`/旧表声明给出；
      * `writers`/`readers` 按 `_declared_touch` 口径登记（该对象的写方是单条命令、
        不带数组上下文，`attribute_commands` 从线体里看不到，只能点名）。

    校验：父对象/成员/目标对象必须存在，成员必须是**指向该目标**的数组链接，目标必须
    有根表，`retire_child_table` 必须在 `retire_tables` 里登记（退场记录只放一处，
    这里只引用），且必须写 `reason`——否则生成期直接失败。
    """
    global _MEMBER_ROOT
    _MEMBER_ROOT = {}
    notes: list[str] = []
    if not ov:
        return notes
    retired = retire_map(ov)
    cmds = {str(c.get("id")): c for c in m.commands}
    for i, spec in enumerate(ov.get("member_rows_in_root") or []):
        if not isinstance(spec, dict):
            raise SystemExit(f"member_rows_in_root[{i}]: 必须是对象")
        pid = str(spec.get("parent") or "")
        member = str(spec.get("member") or "")
        oid = str(spec.get("object") or "")
        label = f"member_rows_in_root[{i}] ({pid}.{member})"
        p = objects.get(pid)
        if p is None:
            raise SystemExit(f"{label}: 模型里没有父对象 {pid!r}")
        mem = next((x for x in p["members"] if x["name"] == member), None)
        if mem is None:
            raise SystemExit(f"{label}: {pid} 没有成员 {member!r}")
        if mem.get("link_kind") != "array" or mem.get("element_composite_ref") != oid:
            raise SystemExit(
                f"{label}: 成员不是指向 {oid!r} 的数组链接"
                f"（link_kind={mem.get('link_kind')!r}, "
                f"element_composite_ref={mem.get('element_composite_ref')!r}）")
        if oid not in objects:
            raise SystemExit(f"{label}: 模型里没有对象 {oid!r}")
        if not str(spec.get("reason") or "").strip():
            raise SystemExit(f"{label}: 必须写 reason（这是「不建那张表」的依据）")
        ct = str(spec.get("retire_child_table") or "")
        if not ct:
            raise SystemExit(f"{label}: 必须写 retire_child_table（要退场的那张子表名）")
        if ct not in retired:
            raise SystemExit(
                f"{label}: {ct} 不在 retire_tables 里——退场记录要落在 retire_tables"
                "（理由/出处一处一份），这里只引用")
        obj = objects[oid]
        obj["shape_override"] = {
            "shape": "root", "from": obj.get("shape"), "by": label,
            "reason": str(spec.get("reason") or ""),
        }
        writers, readers = _declared_touch(cmds, f"{label}.", spec)
        obj["writes"] = _merge_touch(obj.get("writes"), writers)
        obj["reads"] = _merge_touch(obj.get("reads"), readers)
        # 行从「父表的子表副本」搬到「自己的根表」后，父行的链接从**结构继承**
        # 变成一条真 FK：目标对象里那个承载父身份的列要显式指回父对象的身份列。
        # 写法 `"fk": {"member": "uniqid_ms", "target": "ms_rokaku.uniqid",
        # "evidence_va": "…", "reason": "…"}`。角色**不改**：这一列本来就是目标
        # 对象的行键成员，同时又是外键——两件事同时成立，不互相取代。
        fk = spec.get("fk")
        if isinstance(fk, dict) and fk:
            fx = str(fk.get("member") or "")
            ftg = str(fk.get("target") or "")
            fm = next((z for z in obj["members"] if z["name"] == fx), None)
            if fm is None:
                raise SystemExit(f"{label}.fk: {oid} 没有成员 {fx!r}")
            if ftg.count(".") != 1:
                raise SystemExit(f"{label}.fk: target 要写成 <对象>.<列>，收到 {ftg!r}")
            tgt_obj, tgt_col = ftg.split(".")
            if tgt_obj != pid:
                raise SystemExit(f"{label}.fk: target 的宿主必须是父对象 {pid!r}"
                                 f"（否则父行链接没落点），收到 {tgt_obj!r}")
            if not any(z["name"] == tgt_col for z in p["members"]):
                raise SystemExit(f"{label}.fk: {pid} 没有列 {tgt_col!r}")
            if not str(fk.get("reason") or "").strip():
                raise SystemExit(f"{label}.fk: 必须写 reason")
            obj.setdefault("declared_fks", []).append({
                "from": f"{oid}.{fx}", "to": ftg, "kind": "fk",
                "basis": f"根表化：{str(fk.get('reason') or '')}",
                "evidence_va": str(fk.get("evidence_va") or fm.get("evidence_va") or ""),
            })
            notes.append(f"{label} → 声明 FK {oid}.{fx} → {ftg}")
        _MEMBER_ROOT[(pid, member)] = {
            "parent": pid, "member": member, "object": oid,
            "retire_child_table": ct,
            "composite": str(mem.get("element_composite_ref") or ""),
            "column": mem.get("column") or _snake(member),
            "count": _array_count(mem.get("wire_type") or ""),
            "length": mem.get("length"),
            "evidence_va": str(spec.get("evidence_va") or mem.get("evidence_va") or ""),
            "reason": str(spec.get("reason") or ""),
        }
        notes.append(f"{label} → 行在 {oid} 的根表；退场 {ct}")
    return notes


def member_root_of(oid: str, member: str) -> dict | None:
    """该成员是否已被裁为「行在别人的根表里」（`_project_base` / 建表图用）。"""
    return _MEMBER_ROOT.get((oid, member))

# 线类型 → 是否原生数组 / 元素类型
ARR_RE = re.compile(r"^(?P<elem>.+?)\[(?P<n>\d+|\*)\]$")


def today() -> str:
    return datetime.date.today().isoformat()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_dir(name: str) -> list[dict]:
    out = []
    for p in sorted((SCHEMA / name).glob("*.json")):
        try:
            out.append(load(p))
        except json.JSONDecodeError as e:
            print(f"  WARN 解析失败 {p.name}: {e}", file=sys.stderr)
    return out


def norm(name: str) -> str:
    return re.sub(r"[^0-9a-z]+", "_", (name or "").lower()).strip("_")


# ================================================================ L0 输入


class Model:
    """一次性装载字节级模型，供各阶段只读消费。"""

    def __init__(self) -> None:
        self.composites: dict[str, dict] = {
            c["id"]: c for c in load_dir("composites")}
        # 字节区间重叠的成员只能留一个：线模型（`proto/model/composites_gen.go`）
        # 按**声明序**保留先到者、丢掉后来重叠的（`dc_point.bef_next[12,24)` 压在
        # `reward_item_ids[9,25)` 上，所以模型里根本没有 BefNext 字段，旧 0003 也
        # 没建它的列/子表）。这里同口径过滤，否则会造出模型里不存在的字段，
        # store 生成器直接 `model 里找不到 dc_point.aft_next`。
        self.dropped_overlaps: list[str] = []
        for cid, comp in self.composites.items():
            comp["members"] = self._drop_overlaps(cid, comp.get("members") or [])
        self.entities: dict[str, dict] = {
            e["id"]: e for e in load_dir("entities")}
        self.tables: dict[str, dict] = {
            t["id"]: t for t in load_dir("_legacy_tables")}
        self.commands: list[dict] = []
        for p in sorted((SCHEMA / "commands").glob("*.json")):
            c = load(p)
            if isinstance(c, dict) and str(c.get("id", "")).startswith(("CS-", "SC-")):
                self.commands.append(c)
        # 复合体 → 触及它的命令（含方向与 line 位置）
        self.touch: dict[str, list[tuple[dict, str]]] = collections.defaultdict(list)
        for c in self.commands:
            seen: set[str] = set()
            for ref, where in refs_in_command(c):
                if ref in self.composites:
                    seen.add(ref)
            for ref in seen:
                self.touch[ref].append((c, where_of(c, ref)))

    def _drop_overlaps(self, cid: str, members: list[dict]) -> list[dict]:
        """按声明序丢掉与已保留成员字节区间重叠的成员（与线模型同口径）。

        只在两者都有 `offset`/`length` 时判定；缺偏移的成员一律保留。
        """
        kept: list[dict] = []
        spans: list[tuple[int, int]] = []
        for m in members:
            off, ln = m.get("offset"), m.get("length")
            if not isinstance(off, int) or not isinstance(ln, int) or ln <= 0:
                kept.append(m)
                continue
            end = off + ln
            if any(off < e and s < end for s, e in spans):
                self.dropped_overlaps.append(f"{cid}.{m.get('name')}")
                continue
            spans.append((off, end))
            kept.append(m)
        return kept


def refs_in_command(c: dict) -> list[tuple[str, str]]:
    """命令里出现的 composite_ref / element_composite_ref（去重前的原始列表）。"""
    out: list[tuple[str, str]] = []

    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("composite_ref", "element_composite_ref", "struct_ref") \
                        and isinstance(v, str) and v:
                    out.append((v, f"{path}/{k}"))
                walk(v, f"{path}/{k}")
        elif isinstance(o, list):
            for x in o:
                walk(x, f"{path}[]")

    walk(c)
    return out


def where_of(c: dict, ref: str) -> str:
    """该 ref 出现在 request / response / fields 的哪一侧（决定 CS/SC 读写）。"""
    s = json.dumps(c.get("structs") or {}, ensure_ascii=False)
    if f'"{ref}"' in s:
        for side in ("request", "response"):
            if f'"{ref}"' in json.dumps(
                    (c.get("structs") or {}).get(side) or {}, ensure_ascii=False):
                return side
    return "fields"


# ================================================================ L2 对象折叠


class Fold:
    """并查集：把同一业务对象的多个线布局折成一束。"""

    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            # 锚点优先当根：锚点是被 row_key 钉住的对象身份
            self.parent[rb] = ra


def build_fold(m: Model, ov: dict | None = None) -> tuple[Fold, dict[str, list[str]], list[str]]:
    """折叠边 + 锚点。返回 (并查集, 对象→线视图来源, 折叠证据说明)。"""
    f = Fold()
    notes: list[str] = []
    ov = ov or {}

    # 锚点：有 row_key 声明的表 → 其 entity_ref 是对象身份（A3）
    anchors: dict[str, str] = {}
    for tid, t in m.tables.items():
        rk = (t.get("row_key") or {}).get("columns") or []
        ent = t.get("entity_ref") or ""
        if rk and ent:
            anchors[ent] = tid
            notes.append(f"锚点 {ent} ← {tid}.row_key={rk}")

    # 边 1：composite.evidence.other_wire_forms[] → 同一对象的不同线宽（A2）
    other_forms: dict[str, list[str]] = collections.defaultdict(list)
    for cid, c in m.composites.items():
        for w in (c.get("evidence") or {}).get("other_wire_forms") or []:
            tgt = w.get("composite")
            if tgt and tgt in m.composites:
                f.union(cid, tgt)
                other_forms[cid].append(tgt)
                other_forms[tgt].append(cid)
                notes.append(f"线宽折叠 {cid} ↔ {tgt}（{w.get('length')}B）")

    # 边 2：composite.prefix_of（A1）
    #
    # **只认 `prefix_of`，不认 `layout_same_as`**。`layout_same_as` 说的是「线布局
    # 逐字节同形」，**不是**「同一业务对象」；按它折叠会把两张旧表压成一张
    # （实测丢了 13 张旧表：`block_detail`/`friend_histories`/`toppilots`/…）。
    # 这正是 P2 复核批次 `batch_02_fold` 的裁决 `reject_fold`（保守不折叠：
    # 折叠错丢表丢列，不折叠只多一张冗余表）。要合得先按业务确认，再写进
    # `_overrides.json.fold` 人工覆盖项。
    for cid, c in m.composites.items():
        tgt = c.get("prefix_of")
        if isinstance(tgt, str) and tgt in m.composites:
            f.union(cid, tgt)
            notes.append(f"prefix_of {cid} → {tgt}")

    # 边 3：entity.alias_of / prefix_of（A1）——同上，`layout_same_as` 不参与折叠。
    for eid, e in m.entities.items():
        for key in ("alias_of", "prefix_of"):
            tgt = e.get(key)
            if isinstance(tgt, str) and tgt in m.composites:
                f.union(eid, tgt)
                notes.append(f"entity.{key} {eid} → {tgt}")
            elif isinstance(tgt, str) and tgt in m.entities:
                f.union(eid, tgt)
                notes.append(f"entity.{key} {eid} → entity {tgt}")

    # 边 4：多张表指向同一 entity_ref（图本身已折叠，这里补 entity↔composite 同名）
    for eid in m.entities:
        if eid in m.composites:
            f.union(eid, eid)

    # 锚点必须成为它那一束的根
    for ent, tid in anchors.items():
        root = f.find(ent)
        if root != ent:
            f.parent[root] = ent

    # 人工折叠订正（P2 复核批次产物）：把同形但没连起来的线布局合成一个对象
    force_id: dict[str, str] = {}
    for grp in ov.get("fold") or []:
        comps = [c for c in (grp.get("composites") or []) if c in m.composites]
        oid = grp.get("as") or ""
        if len(comps) < 2:
            notes.append(f"人工 fold 组 {grp!r} 有效复合体不足 2 个，跳过")
            continue
        for c in comps[1:]:
            f.union(comps[0], c)
        if oid:
            for c in comps:
                force_id[c] = oid
        notes.append(f"人工 fold {'+'.join(comps)} → {oid or comps[0]}")

    # 线视图来源：本束内所有 composite
    groups: dict[str, list[str]] = collections.defaultdict(list)
    for cid in m.composites:
        groups[f.find(cid)].append(cid)
    f.force_id = force_id
    return f, groups, notes


def canonical_targets(m: Model) -> set[str]:
    """被别的线布局 `layout_same_as`/`prefix_of` 指过的复合体 = 规范形态。"""
    out = set()
    for c in m.composites.values():
        for k in ("layout_same_as", "prefix_of"):
            t = c.get(k)
            if isinstance(t, str) and t in m.composites:
                out.add(t)
    for e in m.entities.values():
        for k in ("alias_of", "layout_same_as", "prefix_of"):
            t = e.get(k)
            if isinstance(t, str):
                out.add(t)
    return out


def _member_link(m: Model, x: dict) -> tuple[str, str]:
    """成员的**子表归属**：`(kind, composite)`，没有则 `("", "")`。

    三种等价写法都要认（`activity.avatar` 就是第三种——复合体 json 只写了
    `"wire_type": "avatar"`，没写 `composite_ref`，只认 `composite_ref` 会把它
    当普通列，然后 `_emit` 又把它当 struct，两头不靠）：
      * `element_composite_ref`（数组元素）；
      * `composite_ref`（内嵌）；
      * `wire_type` 直接是复合体名（`avatar` / `unlockw[3]` / `avatar(18B)`）。
    """
    e = x.get("element_composite_ref")
    if isinstance(e, str) and e in m.composites:
        return "array", e
    r = x.get("composite_ref")
    if isinstance(r, str) and r in m.composites:
        return "nested", r
    wt = (x.get("wire_type") or "").strip()
    mt = ARR_RE.match(wt)
    if mt and mt.group("elem") in m.composites:
        return "array", mt.group("elem")
    # **只认光名**：`avatar` 是内嵌结构，`avatar(18B)` 是「已知宽度的不透明块」
    # （`shapes.py` 就把 clan_ranking_entry.avatar 判成 opaque）。带括号的写法
    # 一律不去括号当复合体名——否则 DDL 说「子表」而 model 说是 `[]byte`，
    # 生成器当场对不上。
    if wt in m.composites:
        return "nested", wt
    return "", ""


def wire_shapes(m: Model) -> tuple[set[str], dict[str, set[str]], dict[str, set[str]]]:
    """线布局的引用形态（详见 docs/05 §4.F）。

    返回 `(写侧命令顶层数组元素, 数组父, 内联父)`：
      * `cmd_array`  —— 在 **CS（写）** 命令里以 `element_composite_ref` 出现
        = 客户端把一整批行发上来 → 对象建自己的根表；
      * `comp_array` —— 被某复合体当 `element_composite_ref` 引用 = 数组 → 子表；
      * `comp_nested`—— 被某复合体当 `composite_ref` 引用 = 内联结构 → 不建表。

    判定优先级 **根 > 子 > 内联**：`pilot` 既被 8 个复合体内联引用、又是命令顶层的
    `array<pilot>` 元素，旧库把它建成 `game.pilot` 表（而非内联）——以「根」为准。

    **`cmd_array` 只认 CS 侧**：这条规则的本意是写侧——客户端发来 `array<X>`，
    服务端要按 N 行落库。读侧（SC）的顶层数组不改变归属，它只是把某个宿主行的
    子表**平铺**给客户端看，宿主仍是写侧那个对象。按全方向收会造出重复且退化的表：
    `rental_module` 本是 `pilot_detail.hav_rental_modules`（数组子表，键含 `elem_index`，
    128 格 × 8B = 1024B），被 `SC-0xFCD2 pilot_rental_module_remain_info_notice`
    的顶层数组一抬，就多出一张 `game.rental_module` 根表、键退化成
    `(world_id, pilot_id)` → 128 个模块互相 upsert 覆盖。
    """
    cmd_array: set[str] = set()
    comp_array: dict[str, set[str]] = collections.defaultdict(set)
    comp_nested: dict[str, set[str]] = collections.defaultdict(set)
    for c in m.commands:
        if str(c.get("direction") or "").upper() != "CS":
            continue
        cmd_array |= _element_refs(c)
    for cid, comp in m.composites.items():
        for mem in comp.get("members") or []:
            kind, ref = _member_link(m, mem)
            if kind == "array":
                comp_array[ref].add(cid)
            elif kind == "nested":
                comp_nested[ref].add(cid)
    return cmd_array, comp_array, comp_nested


def _element_refs(c: dict) -> set[str]:
    """命令里以 `element_composite_ref` 出现的复合体 id。"""
    out: set[str] = set()

    def walk(o) -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "element_composite_ref" and isinstance(v, str) and v:
                    out.add(v)
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(c)
    return out


def assign_shapes(objects: dict[str, dict], shapes) -> None:
    """给每个对象定形态（root/child/inline）与父对象。"""
    cmd_array, comp_array, comp_nested = shapes
    owner: dict[str, str] = {}
    for o in objects.values():
        for c in o["folded_composites"]:
            owner[c] = o["id"]

    def owners_of(pool) -> list[str]:
        return sorted({owner[c] for c in pool if c in owner})

    for o in objects.values():
        mems = o["folded_composites"]
        multi = any(c in cmd_array for c in mems)
        arr = owners_of({p for c in mems for p in comp_array.get(c, ())})
        nest = owners_of({p for c in mems for p in comp_nested.get(c, ())})
        o["multi"] = multi
        o["array_parents"] = arr
        o["inline_parents"] = nest
        if multi or (not arr and not nest):
            o["shape"], o["parent"], o["parents"] = "root", "", []
        elif arr:
            o["shape"], o["parent"], o["parents"] = "child", arr[0], arr
        else:
            # 人工裁决：嵌套结构**独立成表 + FK 到父**，不内联（docs/05 §4.F）。
            # 一个嵌套结构可能被多个父引用（`avatar` 被 8 个对象引用），
            # 所以是「1 个对象 → N 张 1:1 子表」，每张表键 = 对应父的键。
            o["shape"], o["parent"], o["parents"] = "nested", nest[0], nest


def pick_object_id(m: Model, members: list[str], anchors: dict[str, str],
                   force_id: dict[str, str] | None = None,
                   targets: set[str] | None = None) -> str:
    """对象 id 取名优先级：人工指定 > 锚点（有 row_key 的真源）> 规范形态
    （被别的线布局指向的那个）> 线宽最大者。

    `clan_zeon`→`clan_eff`、`trchallenge_info`→`challenge_info` 这类要取**被指向**
    的名字当对象名，否则对象名随遍历顺序漂移。
    """
    if force_id:
        for c in members:
            if c in force_id:
                return force_id[c]
    for eid in members:
        if eid in anchors:
            return eid
    targets = targets or set()
    canonical = [c for c in members if c in targets]
    if canonical:
        return max(canonical, key=lambda c: (m.composites[c].get("length") or 0, c))
    return max(members, key=lambda c: (m.composites[c].get("length") or 0, c))


# ================================================================ L2 对象构建


def _is_placeholder(name: str) -> bool:
    """占位成员名（`TBD`/`unknown`）——字节模型自己都还没分解出来。"""
    n = norm(name)
    return n in ("tbd", "unknown", "na", "none") or n.startswith("unknown_")


def merge_members(m: Model, views: list[str]) -> dict[str, dict]:
    """把多个线视图的成员按名字合并（同一对象同一字段 = 同一列）。

    disposition 在对象级合并：**PERSIST 优先**（见 docs/05 §4.C）。
    """
    merged: dict[str, dict] = {}
    for vid in sorted(views, key=lambda v: m.composites[v].get("length") or 0):
        comp = m.composites[vid]
        status = str(comp.get("status") or "")
        for mem in comp.get("members") or []:
            name = mem.get("name") or ""
            if not name:
                continue
            cur = merged.get(name)
            disp = (mem.get("disposition") or "TBD").upper()
            if cur is None:
                merged[name] = {
                    "name": name,
                    "wire_type": mem.get("wire_type") or "",
                    "length": mem.get("length"),
                    "meaning": mem.get("meaning") or "",
                    "dispositions": {disp: [vid]},
                    "views": [vid],
                    "statuses": {status},
                    "offsets": {vid: mem.get("offset")},
                    "composite_ref": mem.get("composite_ref"),
                    "element_composite_ref": mem.get("element_composite_ref"),
                    "memory_only": bool(mem.get("memory_only")),
                    "evidence_va": mem.get("asm_evidence_va")
                    or _first_va(mem.get("wire_sources")),
                    "evidence_ref": _evidence_ref(mem),
                }
            else:
                cur["dispositions"].setdefault(disp, []).append(vid)
                cur["views"].append(vid)
                cur["statuses"].add(status)
                cur["offsets"][vid] = mem.get("offset")
                if not cur.get("evidence_va"):
                    cur["evidence_va"] = mem.get("asm_evidence_va") \
                        or _first_va(mem.get("wire_sources"))
                if not cur.get("evidence_ref"):
                    cur["evidence_ref"] = _evidence_ref(mem)
                if not cur.get("meaning"):
                    cur["meaning"] = mem.get("meaning") or ""
                # 长度不一致 → 记下（对象级冲突，进 unresolved）
                if mem.get("length") != cur.get("length"):
                    cur.setdefault("length_conflict", {})[vid] = mem.get("length")
    return merged


def body_view(m: Model, obj: dict) -> str:
    """挑出「落库线体」——DDL 列类型/行类型的来源（口径见 docs/05 §4.F）。

    优先级：
      1. 锚点旧表声明的 `entity_ref`（`tbl_adop_list` 声明 `adop_list`）——布局孪生
         （`adop_list`/`adop_get`）的宽度差必须听旧库的，否则行类型会换成另一条命令的
         结构体，手写面 `NewAdopListRow` 的签名也就对不上；
      2. 有 PERSIST 成员的视图里**最长**的那个——持久化视图才是 DDL 描述的那张表；
      3. 兜底：全部视图里最长的。

    必须与 `serverv/tools/schema_design/plan_objects.py::_member_index` 的选择一致：
    那边是 `[wire_body] + folded_composites` 取首个，所以 wire_body 先到先得。
    """
    anchor_tid = obj.get("anchored_by") or ""
    if anchor_tid and anchor_tid in m.tables:
        declared = m.tables[anchor_tid].get("entity_ref") or ""
        if declared in obj["folded_composites"]:
            return declared
    persist = [x for x in obj.get("members") or [] if x.get("lifetime") == "PERSIST"]
    pool = [v for v in obj["folded_composites"]
            if any(x.get("views") and v in x["views"] for x in persist)] \
        or list(obj["folded_composites"])
    if not pool:
        return ""
    return max(pool, key=lambda c: m.composites[c].get("length") or 0)


def resolve_member_widths(m: Model, obj: dict) -> None:
    """把成员宽度定到落库线体，并把各线形的差异留档在 `wire_variants`。

    为什么必须定到落库线体：一个成员在多个 `wire_form` 里宽度可以不同——
    `ms_rokaku.is_costover` 在 battle 视图（`ms`）是 `u8`，在机库视图
    （`ms_lounge`/`ms_rokaku`）是 `char[2]`；`over_custom_level` 是 `u16` vs `u32`。
    DDL 的列只由落库线体生成（`plan_objects._member_index` 先取 `wire_body`），
    而对象成员的 `wire_type` 原先由**最短**视图打底，于是模型里写着 `u8`/`u16`、
    库里却是 `TEXT`/`BIGINT`——站点把列类型讲窄了，而 `unresolved.md §6` 还把这种
    「同名不同宽」当成未决冲突挂着。

    宽度**不取最大**是刻意的：列宽跟落库线体走（锚点旧库口径优先，见 `body_view`），
    但任何视图比列宽更宽都要能被机器看见——`wire_variants` 记下差异，
    `_survey_homing.py` 的「列宽装得下每条线形」不变量据此把关。
    """
    views = list(obj.get("folded_composites") or [])
    per_view: dict[str, dict[str, dict]] = {}
    for vid in views:
        comp = m.composites.get(vid)
        if comp:
            per_view[vid] = {mm.get("name"): mm for mm in comp.get("members") or []}
    body = obj.get("wire_body") or ""
    for x in obj.get("members") or []:
        name = x["name"]
        cands = [(vid, per_view[vid][name]) for vid in (x.get("views") or [])
                 if vid in per_view and name in per_view[vid]]
        if not cands:
            continue
        pick = next((c for c in cands if c[0] == body), None)
        if pick is None:
            pick = max(cands, key=lambda c: c[1].get("length") or 0)
        if pick[1].get("wire_type"):
            x["wire_type"] = pick[1].get("wire_type")
        x["length"] = pick[1].get("length")
        variants = {}
        for vid, mm in cands:
            if (mm.get("wire_type"), mm.get("length")) \
                    != (pick[1].get("wire_type"), pick[1].get("length")):
                variants[vid] = {"wire_type": mm.get("wire_type"),
                                 "length": mm.get("length")}
        if variants:
            x["wire_variants"] = variants
        x.pop("length_conflict", None)


def _first_va(sources) -> str:
    for s in sources or []:
        va = s.get("evidence_va")
        if va:
            return str(va)
    return ""


def _first_va_split(va_field) -> str:
    """`row_key.evidence_va` 是 `A|B|C` 形态的多 VA 串，取第一个非空。"""
    for part in str(va_field or "").split("|"):
        if part.strip():
            return part.strip()
    return ""


def _evidence_ref(mem: dict) -> dict | None:
    """VA 缺失时的可追溯定位：命令 + 子程序 + README 章节。

    82 个成员有 `reader`/`protocol_path §N` 却没有地址级 VA——证据在，只是没记到地址。
    这不算「无出处」，但也不能冒充 VA：单独记 `evidence_ref` 并计入软缺口。
    """
    for s in mem.get("wire_sources") or []:
        if s.get("command"):
            return {
                "command": s.get("command"),
                "struct": s.get("struct") or "",
                "field": s.get("field_name") or "",
                "reader": s.get("reader") or "",
                "printer": s.get("printer") or "",
                "protocol_path": s.get("protocol_path") or "",
                "section": s.get("section") or "",
            }
    return None


def lifetime_of(disps: dict[str, list[str]]) -> tuple[str, str]:
    """对象级 disposition 合并：PERSIST > COMPOSITE > EVENT > TBD。"""
    keys = set(disps)
    if "PERSIST" in keys:
        return "PERSIST", "PERSIST"
    if "COMPOSITE" in keys:
        return "COMPOSITE", "PERSIST"
    if keys == {"EVENT"}:
        return "EVENT", "EVENT"
    if keys == {"EVENT", "TBD"}:
        return "EVENT", "EVENT"
    return "TBD", "TBD"


# ================================================================ L3 角色


# 对象 id 上的形态后缀：去掉后再与成员 stem 比，认出自指身份名
# （`navi_entry` → `navi` ← `navi_id`；`gacha_lineup` → `gacha` ← `gacha_id`）
_ID_SUFFIXES = (
    "_info", "_entry", "_list", "_set", "_lineup", "_desc", "_state",
    "_detail", "_hit", "_card", "_node", "_conf", "_map", "_data", "_item",
)


def _self_identity(obj_id: str, mems: list[dict]) -> str:
    """无 row_key 时，靠**名字**认出对象自己的记录号。

    只做「自己的名字」这一件事，不看别的对象（否则 PK 判定会依赖遍历顺序）。
    判据：成员名以 `id` 结尾，去掉 `id` 后的词干与对象名（或其去形态后缀的形式）
    互相是前缀关系——`channel`↔`channelid`、`quest_info`↔`quest_id`。
    """
    stem = norm(obj_id)
    bases = {stem}
    for suf in _ID_SUFFIXES:
        if stem.endswith(suf) and len(stem) > len(suf):
            bases.add(stem[: -len(suf)])
    best = ""
    for x in mems:
        n = norm(x["name"])
        if not n.endswith("id") or n in SCOPE_NAMES:
            continue
        s = n[:-2].strip("_")
        if not s or norm(x["name"]) in ("uniqid", "uniq_id", "id"):
            continue
        if norm(x["name"]) in SLOT_NAMES:
            continue
        if x.get("element_composite_ref") or _is_array(x.get("wire_type") or ""):
            continue
        for b in bases:
            if s == b or b.startswith(s + "_") or s.startswith(b + "_") \
                    or b == s + "id":
                return x["name"]
        # 最长前缀命中优先（`missionunit_set` → `missionunit_id` 而非 `mission_id`）
        for b in bases:
            if b.startswith(s) and len(s) > len(best):
                best = x["name"]
    return best


def _member_by_column(mems, col: str, oid: str, ov: dict | None = None) -> str:
    """`row_key.columns` 里的**列名** → 成员名（含 `colname` 人工订正）。

    旧表的行键按**列名**写（`tbl_equip_set.row_key = [uniq_id, equip_set_slot]`），
    而线成员可能叫别的名字（`equip_set.slot`，旧库把它存进列 `equip_set_slot`，
    见 `tbl_equip_set.json.row_key.reason`）。不认这层映射就会既合成一个重复的
    `equip_set_slot` 列、又让 PK 丢掉槽位维度。
    """
    cn = (ov or {}).get("colname") or {}
    for x in mems:
        name = x["name"]
        if name == col or (cn.get(f"{oid}.{name}") or name) == col:
            return name
    return ""


def assign_pk(obj: dict, ov: dict | None = None) -> str:
    """第一遍：只定 PK（不依赖其他对象的判定结果）。

    DDL 行键口径（docs/05 §4.E）：`PRIMARY KEY (scope…, own…)`，`scope` 恒为
    `(world_id, pilot_id)`（行主不变量，见 docs/05 §6.1）。本函数只定 `own`：

    1. 表级 `row_key` 声明 —— 唯一真源（`adop_list` / `ms_set` / `equip_set` …）；
    2. `uniqid`/`uniq_id`/`id` —— 自证身份名；
    3. 名字推出的自身记录号 —— `quest_info`↔`quest_id`（`_self_identity`）；
    4. 槽位 —— 数组元素的自然键（`slot`/`deck_slot`/…），与旧库 UNIQUE
       `(world_id,pilot_id,slot)` 同口径；
    5. 都没有 → `own=[]`，即**每个 (world_id, pilot_id) 单行**（旧库同口径）。

    第 4 步不可省：`pilot`/`lpcard`/`ranking` 这类「每机师一张、按槽位多行」的表
    在旧库里正是 `(world_id,pilot_id,slot)`，丢了 slot 会把数组压成一行。
    """
    mems = obj["members"]
    by_name = {x["name"]: x for x in mems}
    pk: list[str] = []
    for c in obj["row_key"]:
        mname = _member_by_column(mems, c, obj["id"], ov)
        if mname and norm(mname) not in SCOPE_NAMES and mname not in pk:
            pk.append(mname)
    kind = "row_key" if pk else ""
    if not pk:
        for cand in IDENT_NAMES:
            x = by_name.get(cand)
            if x is None or x.get("element_composite_ref") \
                    or x.get("memory_only") or _is_array(x.get("wire_type") or ""):
                continue
            pk = [cand]
            kind = "uniqid"
            break
    if not pk:
        self_id = _self_identity(obj["id"], mems)
        if self_id:
            pk = [self_id]
            kind = "self_named"
    if not pk:
        slots = [x["name"] for x in mems
                 if norm(x["name"]) in SLOT_NAMES
                 and not x.get("element_composite_ref")
                 and not _is_array(x.get("wire_type") or "")
                 and not x.get("memory_only")]
        if slots:
            # 槽位名固定顺序，保证 PK 列序与旧库 UNIQUE 一致（`deck_type` 先于 `deck_slot`）
            slots.sort(key=lambda n: _slot_order(norm(n)))
            pk = slots
            kind = "slot"
    if not pk:
        kind = "scope_only"
    obj["pk_members"] = pk
    obj["pk_kind"] = kind
    return pk[0] if pk else ""


_SLOT_ORDER = ("deck_type", "deck_set", "deck_slot", "equip_set_slot",
               "db_index", "inv_place", "elem_index", "slot")


def _slot_order(n: str) -> int:
    return _SLOT_ORDER.index(n) if n in _SLOT_ORDER else len(_SLOT_ORDER)


def build_index(objects: dict[str, dict]) -> dict[str, str]:
    """对象 id（归一化）→ 对象 id。用于把 `X_id` 解析到目标对象。"""
    idx: dict[str, str] = {}
    for oid in objects:
        idx.setdefault(norm(oid), oid)
    return idx


_MASTER_CACHE: tuple[dict[str, list[str]], set[str]] | None = None


def master_index() -> tuple[dict[str, list[str]], set[str]]:
    global _MASTER_CACHE
    if _MASTER_CACHE is None:
        _MASTER_CACHE = cfg_master_index()
    return _MASTER_CACHE


def _id_forms(n: str) -> list[str]:
    """`X_id` 的等价写法（线名 vs cfg 列名口径不同时要能对上）。

    `replay_info.missionId` 在字节模型里是驼峰（`norm` 后 = `missionid`），而 cfg
    主键列是 `mission_id`；不补这一步，字段就永远命中不了主数据索引。
    """
    out = [n]
    if n.endswith("id") and not n.endswith("_id"):
        out.append(n[:-2] + "_id")
    return out


def _classify_nonobject(n: str, stem: str) -> tuple[str, str, str]:
    """对象索引解不了时的归属判定：主数据 / 战斗期句柄 / 真未决。

    这是「92 条未解析引用」的正解：其中绝大多数**不是外键**——
    `mission_id` / `msma_id` / `npc_id` 指向 `cfg.*` 静态配置（不由服务器写），
    `ent_id` / `*_msgid` / `node_id` 是**本场战斗内存里的实体句柄**（不落库）。
    把它们一律记成「引用目标未解析」，会让人以为缺了一批外键。
    """
    by_pk, names = master_index()
    # 1. 主数据：名字正好是某张 cfg 表的主键列
    for cand in _id_forms(n):
        if cand in by_pk:
            tabs = sorted(by_pk[cand])
            tgt = f"cfg.{tabs[0]}.{cand}"
            why = (f"主数据 {tabs[0]}（cfg 主键列名命中）" if len(tabs) == 1
                   else f"主数据候选 {tabs}（cfg 主键列名多命中，待定）")
            return tgt, why, "master"
    # 2. 主数据：词干就是某张 cfg 表名（`module_id` → MODULE）
    if stem in names:
        t = stem.upper()
        return f"cfg.{t}.{n}", f"主数据 {t}（cfg 表名命中）", "master"
    # 3. 战斗期实体句柄
    if RUNTIME_RE.search(n):
        return "", "战斗期实体句柄（本场内存，不落库）", "runtime"
    return "", f"词干 {stem!r} 无对应对象", "none"


def _stem_verdict(stem: str, n: str,
                  oid: str = "") -> tuple[str, str, str, str] | None:
    """词干级人工裁决（`_overrides.json.ref_stem`）→ `(目标, 依据, kind, 类别)`。

    写法（每条都要写 `reason`——这是「不臆造」的落点）：
      `{"kind": "master", "target": "cfg.QUEST.quest_id", "reason": "…"}`
      `{"kind": "fk", "target": "roominfo.room_id", "reason": "…"}`
      `{"kind": "runtime", "reason": "…"}`
      `{"kind": "notref", "reason": "…"}`（名以 id 结尾但不是引用，如 `wbu_rapid`）
      `{"kind": "dangling", "category": "world_entity", "reason": "…"}`
    """
    spec, key = None, ""
    # 词干可以带前缀修饰（`pay_byword` / `rwd_item` / `use_buffitem`）：先全长，
    # 再逐级去掉最前面的片段（`pay_byword` → `byword`），取**最长命中**。
    parts = stem.split("_")
    for cand in [n] + ["_".join(parts[i:]) for i in range(len(parts))]:
        if cand in _REF_STEM:
            spec, key = _REF_STEM[cand], cand
            break
    if not spec:
        return None
    _REF_STEM_HITS.add(key)
    kind = str(spec.get("kind") or "").strip()
    reason = str(spec.get("reason") or "").strip() or "人工裁决（未写理由）"
    target = str(spec.get("target") or "").strip()
    if kind == "master":
        return target, f"人工裁决·主数据：{reason}", "master", ""
    if kind == "fk":
        # 目标就在本对象自己身上（`news.msg_id` → `news.msg_id`）→ 它是身份列
        if target.split(".")[0] == oid:
            return target, f"自指：{reason}", "self", ""
        return target, f"人工裁决·外键：{reason}", "fk", ""
    if kind == "runtime":
        return "", f"人工裁决·战斗期句柄：{reason}", "runtime", ""
    if kind == "notref":
        return "", f"人工裁决·非引用：{reason}", "notref", ""
    if kind == "dangling":
        cat = str(spec.get("category") or "unknown").strip()
        return "", f"{reason}", "dangling", cat
    return None


def _identity_hit(n: str, oid: str) -> tuple[str, str, str] | None:
    """字段名恰好是某个对象的**身份列名** → 那个对象的行（`room_id` → `roominfo`）。

    只在「唯一命中」时成立；多命中（`clan_id` 之于五张 clan 派生表）说明这个词干
    本来就没有唯一的对象指代，交给词干裁决。
    """
    hits = _IDENT_INDEX.get(n) or []
    if len(hits) != 1:
        return None
    tgt = hits[0]
    if tgt == oid:
        return "", "自指：本对象自己的身份名", "self"
    return f"{tgt}.{n}", f"身份列名命中 {tgt}.{n}", "fk"


def resolve_ref(name: str, oid: str, index: dict[str, str],
                objects: dict[str, dict]) -> tuple[str, str, str, str]:
    """`X_id` → (目标列, 依据, kind, 类别)。

    kind ∈ {fk, self, master, runtime, notref, dangling, none}；类别只在
    `dangling` 时有值（world_entity / local_table / value_object / master_candidate…）。

    只认「目标对象有**单一**身份列」的情况：复合行键（`deck_type+deck_set`）或
    没有身份列的对象不能当 FK 目标——硬指过去只会编出一个不存在的列名。
    解析顺序：作用域维度 → 词干人工裁决 → 对象索引 → 身份列名 → 词干模糊匹配
    → `_classify_nonobject`（cfg 主数据 / 战斗期句柄）。
    """
    n = norm(name)
    if n in CROSS_SCHEMA_TARGET:
        return CROSS_SCHEMA_TARGET[n], "scope", "fk", ""
    # `master_pilotid` / `leader_pilot_id` / `master_worldid` 也是行主维度的外键
    if _PILOT_ID_RE.search(n) and n not in SCOPE_NAMES:
        return CROSS_SCHEMA_TARGET["pilot_id"], f"名字形如机师 id（{name}）", "fk", ""
    if _WORLD_ID_RE.search(n) and n not in SCOPE_NAMES:
        return CROSS_SCHEMA_TARGET["world_id"], f"名字形如世界 id（{name}）", "fk", ""
    if not n.endswith("id") or n in ("uniqid", "uniq_id", "id"):
        return "", "非引用形", "none", ""
    stem = n[:-2].strip("_")
    if not stem:
        return "", "词干为空", "none", ""
    verdict = _stem_verdict(stem, n, oid)
    if verdict:
        return verdict
    if stem in STEM_ALIAS:
        tgt = STEM_ALIAS[stem]
        if not tgt:
            return _classify_nonobject(n, stem) + ("",)
    elif stem in index:
        tgt = index[stem]
    else:
        hit = _identity_hit(n, oid)
        if hit:
            return hit + ("",)
        # 词干模糊匹配必须**卡边界**：`clan` 命中 `clan_eff`（对），
        # 但 `mission` 不该命中 `missionunit_set`（那是另一个对象）。
        hits = sorted({o for k, o in index.items()
                       if k == stem or k.startswith(stem + "_")
                       or stem.startswith(k + "_")})
        if len(hits) > 1:
            # 多命中不代表「引用判不了」：先看 cfg 主数据（`mission_id` 命中
            # MISSION_COOP/MISSION_VS），再认「命中对象里有同名身份列的」。
            master = _classify_nonobject(n, stem)
            if master[2] != "none":
                return master + ("",)
            exact = [o for o in hits if n in _IDENT_INDEX
                     and o in (_IDENT_INDEX.get(n) or [])]
            if len(exact) == 1:
                tgt = exact[0]
                return f"{tgt}.{n}", f"身份列名命中 {tgt}.{n}（词干多命中里唯一同名身份列）", "fk", ""
            return "", f"词干 {stem!r} 命中多个对象：{hits}", "none", ""
        if not hits:
            return _classify_nonobject(n, stem) + ("",)
        tgt = hits[0]
    if tgt == oid:
        return "", "自指：本对象自己的身份名", "self", ""
    to = objects[tgt]
    pk = to.get("pk_members") or []
    if len(pk) == 1:
        # 对象身份名与字段名不同 → 是「实例 id 指向对象」，真外键；
        # 相同（`item_id`→`item`）则在 cfg 主数据里另有一解，登记候选待人工判。
        by_pk, _names = master_index()
        if n in by_pk:
            return (f"cfg.{sorted(by_pk[n])[0]}.{n}",
                    f"主数据/实例两解：cfg {sorted(by_pk[n])} 与对象 {tgt}",
                    "master", "")
        return f"{tgt}.{pk[0]}", f"对象名命中 {tgt}", "fk", ""
    if not pk:
        for cand in IDENT_NAMES:
            if any(x["name"] == cand for x in to["members"]):
                return f"{tgt}.{cand}", f"对象名命中 {tgt}（取 {cand}）", "fk", ""
        return "", f"目标 {tgt!r} 没有可用身份列", "none", ""
    return "", f"目标 {tgt!r} 行键是复合键 {pk}，不能做 FK 目标", "none", ""


def assign_roles(obj: dict, index: dict[str, str], ref_notes: list[dict],
                 objects: dict[str, dict]) -> None:
    """第二遍：判角色 + 解 FK（此时所有对象的 PK 都已定稿）。"""
    mems = obj["members"]
    pk = obj["pk_members"]
    alt: list[str] = []

    for x in mems:
        x["role"] = _role_of(x["name"], (x.get("wire_type") or "").lower(), x, pk)
        if x["role"] == "ref":
            target, why, kind, cat = resolve_ref(x["name"], obj["id"], index, objects)
            x["ref_kind"] = kind
            if kind == "fk":
                x["fk_target"] = target
                x["ref_basis"] = why
            elif kind == "self":
                # 指的是自己 → 它是身份名，不是外键（自指 FK 无意义）
                x["role"] = "identity"
                x["ref_kind"] = "self"
                x["ref_basis"] = why
                alt.append(x["name"])
            elif kind in ("master", "runtime"):
                # 主数据 / 战斗期句柄：**不是 game.* 外键**，不进悬空集合。
                x.pop("fk_target", None)
                x["ref_basis"] = why
                if kind == "master" and target:
                    x["master_target"] = target
            elif kind == "notref":
                # 名字以 `id` 结尾但**不是**引用（`wbu_rapid` 是连射率）→ 退回属性。
                x["role"] = "attribute"
                x["ref_basis"] = why
            elif kind == "dangling":
                # 人工裁决过、但目标不在本轮模型里（世界级实体 / 本地表资源 /
                # 值对象）：保留为普通列，理由与类别留档，**不计入未决**。
                x.pop("fk_target", None)
                x["ref_basis"] = why
                x["ref_category"] = cat
            else:
                x.pop("fk_target", None)
                x["ref_basis"] = why
                ref_notes.append({
                    "object": obj["id"], "field": x["name"],
                    "reason": why, "evidence_va": x.get("evidence_va", ""),
                })
    if alt:
        obj["alternate_identity"] = alt
    obj["identity"] = pk


def _is_array(wt: str) -> bool:
    return bool(ARR_RE.match(wt)) or wt.endswith("[]")


def _role_of(name: str, wt: str, x: dict, pk: list[str]) -> str:
    n = norm(name)
    if x.get("memory_only"):
        return "padding"
    if PAD_RE.match(n) or wt.startswith("pad") or x.get("composite_ref") == "pad":
        return "padding"
    if n in SCOPE_NAMES:
        return "scope"
    if n in SLOT_NAMES:
        return "slot"
    if name in pk:
        return "identity"
    if wt.split("[")[0] in OPAQUE_TYPES:
        return "payload"
    if n in TIMESTAMP_NAMES or n.endswith("_time") or n.endswith("_tm") \
            or n.endswith("_at"):
        return "timestamp"
    if FLAG_RE.match(n) or FLAG_SUF_RE.search(n):
        return "flag"
    if COUNTER_RE.search(n):
        return "counter"
    if n.endswith("id") and n not in ("uniqid", "uniq_id", "id"):
        return "ref"
    return "attribute"


# ================================================================ D 写入归属


def attribute_commands(m: Model, views: list[str]) -> dict:
    """对象 × 命令：谁写谁读（CS 写 / SC 读；db_effects 为权威覆盖）。"""
    viewset = set(views)
    writers: list[dict] = []
    readers: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for vid in views:
        for c, _where in m.touch.get(vid, []):
            cid = c["id"]
            direction = c.get("direction")
            verbs = [t for t in (c.get("capabilities") or [])
                     if t not in ("unclassified",) and "." not in t]
            if direction == "CS":
                op = next((v for v in verbs
                           if v in ("create", "update", "delete", "settle")), "update")
                if (cid, op) not in seen:
                    seen.add((cid, op))
                    writers.append({"command": cid, "op": op, "via": vid,
                                    "verbs": verbs})
            else:
                if (cid, "read") not in seen:
                    seen.add((cid, "read"))
                    readers.append({"command": cid, "op": "read", "via": vid})
    # db_effects 权威覆盖
    overrides: list[dict] = []
    for c in m.commands:
        for e in c.get("db_effects") or []:
            ent = e.get("entity")
            if ent in viewset:
                overrides.append({"command": c["id"], "entity": ent,
                                  "op": e.get("op"),
                                  "fields": e.get("fields") or [],
                                  "table_ref": e.get("table_ref")})
    return {"writers": sorted(writers, key=lambda w: w["command"]),
            "readers": sorted(readers, key=lambda r: r["command"]),
            "db_effects": overrides}


def domain_of(m: Model, views: list[str]) -> tuple[str, dict]:
    """L1 域：命令 capabilities 的 `域.` 前缀投票；没有就退到 proto。

    退到 proto 而不是直接写 `core`——`core` 是**独立 schema**的名字，
    把「无域标签」混同成 `core` 会造出假的 schema 归属（docs/05 §3）。
    """
    votes: collections.Counter = collections.Counter()
    for vid in views:
        for c, _ in m.touch.get(vid, []):
            for t in c.get("capabilities") or []:
                if "." in t:
                    votes[t.split(".")[0]] += 1
    if votes:
        return votes.most_common(1)[0][0], dict(votes)
    protos: collections.Counter = collections.Counter()
    for vid in views:
        for c, _ in m.touch.get(vid, []):
            if c.get("proto"):
                protos[c["proto"]] += 1
    if protos:
        return protos.most_common(1)[0][0], dict(protos)
    return "unknown", {}


# --------------------------------------------------- 声明式共享实体（人工登记）


def _declared_touch(cmds: dict[str, dict], where: str,
                    spec: dict) -> tuple[list[dict], list[dict]]:
    """声明的读写命令 → 与 `attribute_commands` 同形的 `(writers, readers)`。

    命令必须存在、方向必须与栏位一致（`writers` 只收 CS、`readers` 只收 SC）：
    声明式对象没有线体，`attribute_commands` 在这条路上取不到东西，所以读写方
    只能由人点名——那就把「点错名/点错方向」变成生成期报错。
    """
    writers: list[dict] = []
    readers: list[dict] = []
    for tag, want_dir in (("writers", "CS"), ("readers", "SC")):
        for cid in spec.get(tag) or []:
            c = cmds.get(str(cid))
            if c is None:
                raise SystemExit(f"{where}.{tag}: 命令不存在 {cid!r}")
            if str(c.get("direction") or "") != want_dir:
                raise SystemExit(
                    f"{where}.{tag}: {cid} 方向是 {c.get('direction')}，"
                    f"与 {tag} 不符")
            verbs = [t for t in (c.get("capabilities") or [])
                     if t not in ("unclassified",) and "." not in t]
            if tag == "writers":
                op = next((v for v in verbs
                           if v in ("create", "update", "delete", "settle")),
                          "update")
                writers.append({"command": str(cid), "op": op, "via": "",
                                "verbs": verbs, "declared": True})
            else:
                readers.append({"command": str(cid), "op": "read", "via": "",
                                "declared": True})
    return (sorted(writers, key=lambda w: w["command"]),
            sorted(readers, key=lambda r: r["command"]))


def declared_objects(m: Model, ov: dict | None) -> dict[str, dict]:
    """`_overrides.json.new_objects` → 共享实体的**作用域与读写方登记**。

    为什么需要这一节：`clan_id` / `cupteam_id` 指的是**跨机师共享的实体**
    （战队、杯赛队伍），它们的身份列在所有线体里都只作为**别人的属性**出现
    （`pilot.clan_id`、`pcard.cupteam_id`、`bracket_info.cupteam_id_a`）：线里
    没有以它们为顶层的报文，于是归位引擎找不到能当 FK 目标的根对象，判成
    `dangling` 只是承认「目标不在本轮模型」——不是结论：氏族级 / 杯赛命令已经
    **逐列**给出了这些实体自身的属性与出处。

    成员**不在这里**声明：实体自己的线布局 / 类型 / 宽度 / 逐列 VA 的真源是手写
    实体复合体 `schema/composites/<composite>.json`（`declared: true` 标明它不是
    某条报文的字节布局：无 offset、无 total_bytes，DDL 侧也就没有 wire 线长）。
    复合体自带成员，归位引擎自然就会推出一张对象（每个复合体自成一组），这一节
    只把推导出来的对象补成「共享实体」：

      * `composite` —— 必须是推出该对象的那个实体复合体（不是就报错，防张冠李戴）；
      * `scope: ["world_id"]` —— 跨机师共享（默认是 `(world_id, pilot_id)`）；
      * `writers` / `readers`：点名的 CS 写方与 SC 读方，方向不符直接报错
        （声明式实体没有线体，`attribute_commands` 在这条路上取不到东西）。

    为什么不能「只写一份 members 清单」：Go 模型类型只由 `composites/*.json` 生成
    （codecgen 的模型表遍历 composites）。成员不在任何复合体里的对象 `wire_body`
    为空、`plan.entity` 落成对象 id，生成的代码引用 `model.clan` 不存在（编译不过）；
    成员没有 `Column.path` 时 `FromModel` 还会静默留零。所以先写复合体，再来点名。
    """
    spec_all = (ov or {}).get("new_objects") or {}
    cmds = {str(c.get("id")): c for c in m.commands}
    out: dict[str, dict] = {}
    for oid, spec in spec_all.items():
        if str(oid).startswith("_") or not isinstance(spec, dict):
            continue
        scope = [str(s) for s in (spec.get("scope") or SCOPE_ORDER)]
        bad = [s for s in scope if s not in SCOPE_ORDER]
        if bad:
            raise SystemExit(f"new_objects.{oid}.scope: 不是作用域维度 {bad}")
        cid = str(spec.get("composite") or "").strip()
        if not cid:
            raise SystemExit(
                f"new_objects.{oid}: 必须写 composite（实体复合体 id）——"
                "成员/类型/VA 的真源是 composites/<id>.json")
        if cid not in m.composites:
            raise SystemExit(
                f"new_objects.{oid}.composite: composites/{cid}.json 不存在")
        writers, readers = _declared_touch(cmds, f"new_objects.{oid}", spec)
        out[oid] = {
            "composite": cid,
            "scope": scope,
            "title": str(spec.get("title") or ""),
            "reason": str(spec.get("reason") or ""),
            "note": str(spec.get("note") or ""),
            "writes": writers,
            "reads": readers,
        }
    return out


def _merge_touch(have: list[dict] | None, extra: list[dict]) -> list[dict]:
    """合并读写方（按命令去重；声明那条胜出，它带 `declared` 标记）。"""
    out: dict[str, dict] = {}
    for x in list(have or []) + list(extra or []):
        out.setdefault(str(x.get("command")), x)
    return [out[k] for k in sorted(out)]


def apply_declared(objects: dict[str, dict], decls: dict[str, dict]) -> None:
    """把 `new_objects` 的登记叠到推导出来的对象上（推不出来就报错）。"""
    for oid, decl in decls.items():
        cur = objects.get(oid)
        if cur is None:
            raise SystemExit(
                f"new_objects.{oid}: 模型里推不出这个对象"
                f"（composite={decl['composite']}）——实体复合体要能自成一组，"
                "检查它是否被 fold 进了别的对象")
        folded = cur.get("folded_composites") or []
        if decl["composite"] not in folded:
            raise SystemExit(
                f"new_objects.{oid}.composite: 对象 {oid} 的成员不是从 "
                f"{decl['composite']} 来的（folded={folded}）")
        if decl["composite"] != cur.get("wire_body"):
            raise SystemExit(
                f"new_objects.{oid}.composite: 落库线体不是 {decl['composite']}"
                f"（wire_body={cur.get('wire_body')}）")
        cur["declared"] = True
        cur["declared_reason"] = decl["reason"]
        cur["scope"] = list(decl["scope"])
        if decl["title"]:
            cur["title"] = decl["title"]
        if decl["note"]:
            cur["note"] = decl["note"]
        cur["writes"] = _merge_touch(cur.get("writes"), decl["writes"])
        cur["reads"] = _merge_touch(cur.get("reads"), decl["reads"])


# ------------------------------------------------- 写方点名（declared writers）


def declared_writers(objects: dict[str, dict], m: Model,
                     ov: dict | None) -> list[str]:
    """`_overrides.json.writers`：**线体里没有实体、命令却点着它写**的写方登记。

    引擎认写方的口径是「命令的线体里带了这个复合体」（`attribute_commands`）。
    列表类实体有一类例外：写方只带**目标机师 id**，报文里没有卡片结构——
    例如屏蔽名单的写方 `CS-0xECDA-block_list_add` 只有
    `pilotid` / `world_id` / `to_pilot_name`（状态串 @0x00EEC138），
    `CS-0x753A-block_list_remove` 同形（@0xeec168），好友名单的
    `CS-0xA30C-friend_list_remove`（@0xEEC018）同理。归位引擎看不出这些命令与
    `block_detail` / `friend_detail` 有关，于是把它们判成 **0 CS 写方**；
    而「0 CS 写方 + 行可派生 ⇒ 不建表」的收口口径一旦套上去，丢掉的是
    **真实写路径**（谁把谁拉进了名单）——退表退掉的不是冗余副本，是那份关系本身。

    所以这类对象必须点名登记，并且 reason 要写清「为什么看线体认不出来」
    （§「负断言的枚举证明」：说 0 写方之前先把这类命令枚举干净）。写法：

        "writers": {
          "block_detail": {
            "commands": ["CS-0xECDA-lounge-block_list_add",
                         "CS-0x753A-lounge-block_list_remove"],
            "evidence_va": "0x00EEC138 / 0xeec168",
            "reason": "写方只带目标 pilotid，线体里没有 113B 卡片结构"
          }
        }

    命令必须存在、且方向是 CS（`_declared_touch` 会把点错名/点错方向变成生成期
    报错）；登记结果与归属写方合流（`_merge_touch` 去重）。
    """
    notes: list[str] = []
    spec_all = (ov or {}).get("writers") or {}
    cmds = {str(c.get("id")): c for c in m.commands}
    for oid, spec in spec_all.items():
        if str(oid).startswith("_"):
            continue
        o = objects.get(oid)
        if o is None:
            notes.append(f"writers 登记指向不存在的对象 {oid!r}")
            continue
        if not isinstance(spec, dict):
            notes.append(f"writers.{oid}: 要写成 {{commands:[…], reason:…}}")
            continue
        if not str(spec.get("reason") or "").strip():
            notes.append(f"writers.{oid}: 缺 reason（为什么线体里认不出这些写方）")
        # 本节的键是 `commands`（写方），`_declared_touch` 认的是 `writers`/`readers`
        # 两个栏位——转一手，顺带支持 `readers`（若某条读命令也带不出线体）。
        touch_spec = {
            "writers": spec.get("commands") or [],
            "readers": spec.get("readers") or [],
        }
        writers, readers = _declared_touch(cmds, f"writers.{oid}", touch_spec)
        for x in writers + readers:
            x["declared_reason"] = str(spec.get("reason") or "")
            x["evidence_va"] = str(spec.get("evidence_va") or "")
        o["writes"] = _merge_touch(o.get("writes"), writers)
        o["reads"] = _merge_touch(o.get("reads"), readers)
    return notes


# ================================================================ 主流程


# ------------------------------------------------------ 注入列（inject_members）

# 注入列能落库的线类型 → 字节宽度（**不猜宽度**：认不出的类型直接报错）。
_INJECT_WIRE_BYTES = {
    "u64": 8, "u32": 4, "u16": 2, "u8": 1,
    "i64": 8, "i32": 4, "i16": 2, "i8": 1,
}

# 注入列的**值从哪来**（`inject_members.<key>.resolved_by`，默认 `wire_sibling`）：
#   * `wire_sibling`：同一个报文的**兄弟字段**（`party_member.party_id` @0xB4542D、
#     `mshipbid_card.mclan_id` @0xB9FD99）——出处就是那一条写线指令；
#   * `session`：**服务端会话上下文**（`news.clan_id`：板归「我的氏族」，5 条 CS 一条
#     都不带 clan id，旧实现即 `s.clanCtxOf(sess).clanID`）——`evidence_va` 证明的是
#     「面板/命令是按这个实体打开的」，不是写入点。这类列只能是**行键列**：不进行键的
#     会话列是缓存，会在多行之间漂移（守卫 20 钉住）。
_INJECT_RESOLVERS = ("wire_sibling", "session")


def injected_members(objects: dict[str, dict], ov: dict | None) -> list[str]:
    """`_overrides.json.inject_members` → 给元素表补「线上没有、库里要有」的外部行键列。

    为什么需要这一节：`party_member` / `party_member_stat` 这类**元素表**的身份写在
    报文的**兄弟字段**上（SC-0x305D 的 `recruit.party_id`、SC-0x76B1 下发的是「某队
    的成员状态列表」），元素自身只有成员字段、没有「所属队伍」——于是行键只能靠 scope
    （`world_id,pilot_id`）撑着，`party_id` 引用也只能判 `dangling`。

    这一节把「这一列线上不存在、但库里必须有」显式登记下来：

      * 成员进 `members[]`（`views: []` ⇒ `columns[].synthetic = true`）；
      * `key: true` 追加进 `pk_members` ⇒ 进唯一索引，并让 store 的构造函数把它做成
        **必传形参**（口径同 `item.slot`：值不由解码结构体取，由调用方显式给）；
      * `role: ref` + `fk_target` ⇒ 进 `relations[]` 的 `fk`。

    为什么不写进 `composites/`：复合体是**报文的字节布局**（有 offset、有总长，
    codecgen 由它生成 Go 解码结构体）。往线结构体里加一个线上不存在的成员，会造出
    「解码时多读 4 字节」的假线体，Go 模型也与报文对不上。

    为什么不走 `role`/`fk` 订正：那两节是**给已有成员改判**用的；注入的成员在线视图里
    根本不存在，`_find_member` 找不到它。
    """
    spec_all = (ov or {}).get("inject_members") or {}
    notes: list[str] = []
    for key, spec in spec_all.items():
        if str(key).startswith("_") or not isinstance(spec, dict):
            continue
        oid, _, mname = str(key).partition(".")
        if not oid or not mname:
            raise SystemExit(f"inject_members 的键要写成 <对象>.<成员>：{key!r}")
        o = objects.get(oid)
        if o is None:
            raise SystemExit(f"inject_members.{key}: 模型里没有对象 {oid!r}")
        if any(x["name"] == mname for x in o["members"]):
            raise SystemExit(
                f"inject_members.{key}: 成员已存在——这一节只为「线上没有、库里要有」"
                "的列而设；线上真有这个成员时该改的是 composites/")
        wt = str(spec.get("wire_type") or "").strip()
        if wt not in _INJECT_WIRE_BYTES:
            raise SystemExit(
                f"inject_members.{key}.wire_type: 认不出宽度 {wt!r}"
                f"（可选 {'/'.join(_INJECT_WIRE_BYTES)}）——不猜宽度")
        role = str(spec.get("role") or "ref").strip()
        if role not in ROLES:
            raise SystemExit(f"inject_members.{key}.role: 未知角色 {role!r}")
        va = str(spec.get("evidence_va") or "").strip()
        if not va:
            raise SystemExit(f"inject_members.{key}.evidence_va: 必须给出地址级证据"
                             "（守卫 3：成员必须有出处）")
        meaning = str(spec.get("meaning") or "").strip()
        if not meaning:
            raise SystemExit(f"inject_members.{key}.meaning: 必须给出含义")
        resolved_by = str(spec.get("resolved_by") or "wire_sibling").strip()
        if resolved_by not in _INJECT_RESOLVERS:
            raise SystemExit(
                f"inject_members.{key}.resolved_by: 未知来源 {resolved_by!r}"
                f"（可选 {'/'.join(_INJECT_RESOLVERS)}）")
        if resolved_by == "session" and not spec.get("key"):
            raise SystemExit(
                f"inject_members.{key}: resolved_by=session 的列必须是行键列"
                "（key: true）——会话解析出来的普通列只是缓存，会在多行之间漂移")
        x = {
            "name": mname,
            "wire_type": wt,
            "length": _INJECT_WIRE_BYTES[wt],
            "meaning": meaning,
            "lifetime": "PERSIST",
            "dispositions": {"PERSIST": []},
            # 空 `views` ⇒ 不在任何线复合体里：生成器据此把它当**外部行键**
            # （值由调用方显式传，不从解码结构体取）。
            "views": [],
            "composite_ref": None,
            "element_composite_ref": None,
            "link_kind": "",
            "link_composite": "",
            "memory_only": False,
            "evidence_va": va,
            "role": role,
            "injected": True,
            "injected_basis": str(spec.get("basis") or "").strip(),
            "injected_resolved_by": resolved_by,
        }
        if role == "ref":
            tgt = str(spec.get("fk_target") or "").strip()
            if "." not in tgt:
                raise SystemExit(f"inject_members.{key}.fk_target: 要写成 <对象>.<列>，"
                                 f"收到 {tgt!r}")
            if not x["injected_basis"]:
                raise SystemExit(f"inject_members.{key}.basis: role=ref 必须写理由"
                                 "（不臆造 FK 是硬要求）")
            x["ref_kind"] = "fk"
            x["fk_target"] = tgt
            x["ref_basis"] = f"外部行键：{x['injected_basis']}"
        o["members"].append(x)
        o["members"].sort(key=lambda z: z["name"])
        if spec.get("key"):
            pks = list(o.get("pk_members") or [])
            if mname not in pks:
                pks.append(mname)
            o["pk_members"] = pks
            o["pk_kind"] = "injected_key"
            o["is_root"] = True
        notes.append(f"注入列 {key}（{wt}，role={role}"
                     + ("，进行键" if spec.get("key") else "")
                     + ("，会话解析" if resolved_by == "session" else "")
                     + f"）@ {va}")
    return notes


def build(m: Model) -> tuple[dict[str, dict], list[str], dict]:
    ov = load_overrides()
    fold, groups, fold_notes = build_fold(m, ov)
    force_id = getattr(fold, "force_id", {}) or {}
    anchors = {t.get("entity_ref"): tid for tid, t in m.tables.items()
               if ((t.get("row_key") or {}).get("columns") or []) and t.get("entity_ref")}

    objects: dict[str, dict] = {}
    unresolved: list[str] = []
    targets = canonical_targets(m)
    shapes = wire_shapes(m)
    for root, members in sorted(groups.items()):
        members = sorted(set(members))
        oid = pick_object_id(m, members, anchors, force_id, targets)
        merged = merge_members(m, members)
        # row_key 声明来自锚点表（对象 id 就是锚点 entity）——不能靠 entities/ 文件
        # 是否存在，`ms_set`/`equip_set`/`buildup_info` 都没有同名 entity 文件。
        rk: list[str] = []
        ext_decl: dict[str, dict] = {}
        rk_evidence = ""
        tid = anchors.get(oid, "")
        if tid:
            rkt = m.tables[tid].get("row_key") or {}
            rk = [str(c) for c in rkt.get("columns") or []]
            rk_evidence = str(rkt.get("evidence_va") or "")
            ext_decl = {str(k): v for k, v in (rkt.get("external") or {}).items()
                        if isinstance(v, dict)}
        # 声明了行键、但该列不在线体里（是复合体的兄弟字段）→ 合成一个外部键成员。
        # 「在线体里」按**列名**判（含 `colname` 订正）：`equip_set_slot` 就是线成员
        # `slot` 的旧列名，再合成一个就多一列重复数据。
        external_keys = [c for c in rk
                         if not _member_by_column(list(merged.values()), c, oid, ov)]
        for col in external_keys:
            spec = ext_decl.get(col) or {}
            merged[col] = {
                "name": col,
                "wire_type": str(spec.get("wire_type") or ""),
                "length": spec.get("length"),
                "meaning": str(spec.get("meaning") or "行键（复合体的兄弟字段，不在线体内）"),
                "dispositions": {"PERSIST": []},
                "views": [],
                "statuses": {"complete"},
                "offsets": {},
                "composite_ref": None,
                "element_composite_ref": None,
                "memory_only": False,
                # 外部键的证据来自表级 row_key 声明（列本身不在线体里）
                "evidence_va": str(spec.get("evidence_va")
                                   or _first_va_split(rk_evidence)),
                "evidence_ref": None,
                "external_key": True,
            }
        # 锚点表的**非复合体列**也要并入对象。
        # 例：`tbl_item` = `inv_place`(u16, 背包栏位) + `item`(struct 22B)。
        # `inv_place` 是命令级字段、不在 `item` 复合体里，于是 `game.item` 会
        # 丢掉 `slot` 列（= `inv_place`），PK 也会错判成 `uniqid`——而旧库
        # 的真实自然键是 UNIQUE `(world_id,pilot_id,slot)`，且 `store/shop_buy.go`
        # 正是按 slot 寻址。证据就是表定义里的列，不是猜。
        # 注意锚点表的选取口径要和下面 `legacy_table` 一致：`tbl_item` 没有
        # row_key 声明，不在 `anchors` 里，只有 `entity_ref`——不能只看 `anchors`。
        anchor_tid = anchors.get(oid, "")
        if not anchor_tid:
            anchor_tid = next((ltid for ltid, t in m.tables.items()
                               if t.get("entity_ref") == oid), "")
        if not anchor_tid:
            anchor_tid = next((ltid for ltid, t in m.tables.items()
                               if t.get("entity_ref") in members), "")
        anchor_cols: list[str] = []
        if anchor_tid:
            for col in m.tables[anchor_tid].get("columns") or []:
                nm = str(col.get("name") or "")
                if not nm or nm in merged:
                    continue
                if str(col.get("disposition") or "") == "COMPOSITE":
                    continue
                src = (col.get("wire_sources") or [{}])[0]
                merged[nm] = {
                    "name": nm,
                    "wire_type": str(src.get("wire_type") or ""),
                    "length": src.get("length"),
                    "meaning": str(col.get("meaning") or ""),
                    "dispositions": {str(col.get("disposition")
                                         or "PERSIST"): []},
                    "views": [],
                    "statuses": {str(col.get("status") or "complete")},
                    "offsets": {},
                    "composite_ref": None,
                    "element_composite_ref": None,
                    "memory_only": False,
                    "evidence_va": str(src.get("evidence_va") or ""),
                    "evidence_ref": None,
                    "anchor_column": True,
                }
                anchor_cols.append(nm)
        # 线视图：文件名 + 线长 + 出线命令
        views = []
        for vid in members:
            comp = m.composites[vid]
            views.append({
                "composite": vid,
                "length": comp.get("length"),
                "memory_claim": comp.get("memory_claim"),
                "reader": comp.get("reader"),
                "printer": comp.get("printer"),
                "commands": sorted({c["id"] for c, _ in m.touch.get(vid, [])}),
            })
        dom, votes = domain_of(m, members)
        # 表名：锚点表优先（带 row_key 的真源，`ms_rokaku` 必须落 game.ms_rokaku
        # 而不是 members 里先撞上的 tbl_ms）；然后取 entity_ref 与本对象同名的表
        # （对象名已是规范形态，`lpcard` 要落 game.lpcard 而不是 game.block_detail）；
        # 最后才退到任意覆盖本对象的旧表。
        legacy_table = anchors.get(oid, "")
        if not legacy_table:
            legacy_table = next(
                (ltid for ltid, t in m.tables.items()
                 if t.get("entity_ref") == oid), "")
        if not legacy_table:
            legacy_table = next(
                (ltid for ltid, t in m.tables.items()
                 if t.get("entity_ref") in members), "")
        obj = {
            "id": oid,
            "title": m.composites.get(oid, {}).get("title") or oid,
            "domain": dom,
            "domain_votes": votes,
            "folded_composites": members,
            "anchored_by": anchors.get(oid, ""),
            "legacy_table": legacy_table,
            "row_key": rk,
            "views": views,
            "members": [
                {
                    "name": k,
                    "wire_type": v["wire_type"],
                    "length": v["length"],
                    "meaning": v["meaning"],
                    "lifetime": lifetime_of(v["dispositions"])[0],
                    "dispositions": v["dispositions"],
                    "views": v["views"],
                    "composite_ref": v.get("composite_ref"),
                    "element_composite_ref": v.get("element_composite_ref"),
                    "link_kind": _member_link(m, v)[0],
                    "link_composite": _member_link(m, v)[1],
                    "memory_only": v.get("memory_only"),
                    "evidence_va": v.get("evidence_va") or "",
                    "evidence_ref": v.get("evidence_ref"),
                    **({"external_key": True} if v.get("external_key") else {}),
                    **({"anchor_column": True} if v.get("anchor_column") else {}),
                    **({"known_gap": True,
                        "gap_reason": _gap_reason(v)} if _gap_reason(v) else {}),
                    **({"length_conflict": v["length_conflict"]}
                       if v.get("length_conflict") else {}),
                }
                for k, v in sorted(merged.items(), key=lambda kv: kv[0])
            ],
        }
        obj["wire_body"] = body_view(m, obj)
        resolve_member_widths(m, obj)
        cmd = attribute_commands(m, members)
        obj["writes"] = cmd["writers"]
        obj["reads"] = cmd["readers"]
        obj["db_effects"] = cmd["db_effects"]
        objects[oid] = obj

    # 声明式共享实体（`_overrides.json.new_objects`）：成员由手写实体复合体推出来
    # （每个复合体自成一组），这一节只登记作用域与读写方——见 declared_objects。
    apply_declared(objects, declared_objects(m, ov))
    # 写方点名（`_overrides.json.writers`）：线体里没有实体、命令只带目标 id 的写方
    # （屏蔽/好友名单那几条），不点名就会被判成 0 CS 写方——见 declared_writers。
    writers_notes = declared_writers(objects, m, ov)

    # 第一遍：所有对象先定 PK（避免「先判的对象看不到后判对象的行键」的顺序依赖）
    for o in objects.values():
        assign_pk(o, ov)
    for o in objects.values():
        # `is_root` 曾用「有 PK / 有 scope / 有旧表」来判，于是 `bmgpack` 这种
        # 「命令顶层 array、但线里没有 scope 列」的对象被误判成非根（守卫会漏检它的表名）。
        # 根不根是**结构问题**（§4.F），由 `assign_shapes` 定；scope 是另一件事。
        o["is_root"] = bool(o.get("pk_members")) or any(
            x["name"] in SCOPE_NAMES for x in o["members"]) \
            or bool(o.get("anchored_by")) or bool(o.get("legacy_table"))
    # 第二遍：判角色 + 解 FK
    index = build_index(objects)
    set_ident_index(objects)
    set_ref_stem(ov)
    ref_notes: list[dict] = []
    for o in objects.values():
        assign_roles(o, index, ref_notes, objects)
    # 注入列（`_overrides.json.inject_members`）：给「身份写在兄弟字段上」的元素表补
    # 外部行键列。必须排在 `assign_roles` 之后——角色由这一节显式给定（在线视图里
    # 根本没有这个成员，判不出角色），排在 `apply_overrides` 之前——`pk` 订正要能
    # 点到这些注入出来的成员名。
    inject_notes = injected_members(objects, ov)
    # 第三遍：叠人工裁决（P2 复核批次产物），再按最终状态重算未决
    override_notes = apply_overrides(objects, ov)
    ref_notes = recompute_ref_notes(objects)
    # 「数组成员的行在别人的根表里」（`_overrides.json.member_rows_in_root`）：登记
    # 目标对象的读写方，并把它的形态标记成 root——真的改 shape 要等 `assign_shapes`
    # 之后（那一步会按线引用重算形态）。
    member_root_notes = set_member_roots(objects, m, ov)
    # DDL 投影（形态/表名/线体/键/不落库成员）——先定形态，再据此定「是不是根」
    assign_shapes(objects, shapes)
    for o in objects.values():
        so = o.get("shape_override")
        if so:
            o["shape"], o["parent"], o["parents"] = "root", "", []
        o["is_root"] = o.get("shape") == "root"
        o["has_scope"] = bool(o.get("scope")) or any(
            x["name"] in SCOPE_NAMES for x in o["members"])
        project(m, objects, o)
    # 表图：跨对象、按「父表__成员名」递归建表并挂子表指针。
    # 必须等所有对象的 columns 都算完（子表列集来自被引用对象）。
    build_table_graph(objects, m, ov)
    for o in objects.values():
        root_t = next((t for t in o["tables"] if t["shape"] == "root"), None)
        o["keys"]["primary_key"] = (
            (root_t or o["tables"][0])["primary_key"] if o["tables"]
            else list(SCOPE_ORDER))
        o["tables"] = sorted(o["tables"], key=lambda t: t["name"])

    metrics = {
        "fold_notes": fold_notes,
        "anchors": anchors,
        "ref_notes": ref_notes,
        "override_notes": override_notes,
        "inject_notes": inject_notes,
        "member_root_notes": member_root_notes,
        "writers_notes": writers_notes,
        "twins": layout_twins(m, objects, set(
            (ov.get("twin_verdicts") or {}).keys())),
        "twins_reviewed": len([k for k in (ov.get("twin_verdicts") or {})
                               if not str(k).startswith("_")]),
        "unresolved": unresolved,
    }
    return objects, unresolved, metrics


# ------------------------------------------------------- 对象 → DDL 投影


def array_count(wt: str) -> int:
    """`u32[3]` / `unlockw[3]` → 3；非数组 → 0。"""
    mm = ARR_RE.match((wt or "").strip())
    if not mm:
        return 0
    n = mm.group("n")
    return int(n) if n.isdigit() else 0


def _inherited_parent_keys(objects: dict[str, dict], obj: dict,
                           depth: int = 0) -> list[str]:
    """子表要从**顶层父行**抄下来的键列（父的 own；父是子表则继续往上）。

    只抄 `own`（identity/slot），不抄 scope——scope 本来就是注入列。
    """
    p = objects.get(obj.get("parent") or "")
    if not p or depth > 4:
        return []
    own = list(p.get("pk_members") or [])
    if p.get("shape") == "child":
        own = _inherited_parent_keys(objects, p, depth + 1) + own
    return own


def _inherited_keys_of(objects: dict[str, dict], parent_id: str,
                       depth: int = 0) -> list[str]:
    """从**顶层父行**抄下来的键列（父的 own；父本身是子表则继续往上）。

    只抄 `own`（identity/slot），不抄 scope——scope 本来就是注入列。
    """
    p = objects.get(parent_id or "")
    if not p or depth > 4:
        return []
    own = list(p.get("pk_members") or [])
    if p.get("shape") in ("child", "nested"):
        own = _inherited_keys_of(objects, p.get("parent") or "", depth + 1) + own
    return own


def project(m: Model, objects: dict[str, dict], obj: dict) -> None:
    """对象级投影骨架（列/键/线体）。真正的建表见 `build_table_graph`。"""
    _project_base(m, objects, obj)


def _stem_of(obj: dict) -> str:
    """对象自己那张「根表」的主干名：锚点旧表名优先，否则对象 id。"""
    lt = obj.get("legacy_table") or ""
    return _snake(lt.removeprefix("tbl_")) if lt else _snake(obj["id"])


def _array_count(wt: str) -> int:
    mt = ARR_RE.match((wt or "").strip())
    if mt and mt.group("n") != "*":
        try:
            return int(mt.group("n"))
        except (TypeError, ValueError):
            return 0
    return 0


# DDL 生成器（`serverv/tools/gen_migration`）对每张表**固定**写出的列名：表头
# `id/world_id/pilot_id` 与表尾 `updated_at/version`。PostgreSQL 同表不允许重名列，
# 所以成员列与这五个同名时必须改名。
FIXED_COLS = ("id", "world_id", "pilot_id", "updated_at", "version")


def _table_prefix(name: str) -> str:
    return name.removeprefix("game.")


def _table_columns(cols: list[dict], prefix: str, reserved: set[str]) -> list[dict]:
    """对象列 → **本表**列（表级改名：与固定列/键列同名的成员前缀化）。

    **改名而不是删列**是旧 `plan.py` 的口径，也是数据正确的口径：与固定列同名的
    成员往往不是同一个值——`clan_eff.world_id` 是另一个世界 id（旧库存成
    `clan_eff_world_id`）、`pilot.pilot_id` 是线里的机师号（旧库 `pilot_pilot_id`）、
    子表 `favms.pilot_id` 是父行引用（旧库 `pilot_detail_pilot_id`，
    `no_blob_test.go` 的注释正是按这个名字写的）。删列会**静默丢字段**。
    """
    out: list[dict] = []
    taken: set[str] = set()
    for c in cols:
        name = c["column"]
        renamed = ""
        if name in reserved:
            renamed = name
            name = f"{prefix}_{name}"
        n = 2
        while name in taken:
            name = f"{prefix}_{renamed or c['column']}_{n}"
            n += 1
        taken.add(name)
        e = dict(c)
        e["column"] = name
        if renamed:
            e["renamed_from"] = renamed
        out.append(e)
    return out


def _finalize_tables(objects: dict[str, dict]) -> None:
    """给每张表定**最终列名**与行键（见 `_table_columns`）。

    列名是**表级**的：同一个对象可以投影多张表（`favms` 既是根表
    `game.favms` 又被 `pilot_detail` 当数组元素引用），两张表的前缀不同
    （`favms_pilot_id` / `pilot_detail_pilot_id`），所以不能只算对象级列名。
    """
    idx: dict[str, tuple[dict, dict]] = {}
    for o in objects.values():
        for t in o["tables"]:
            idx[t["name"]] = (o, t)

    def walk(o: dict, t: dict, inherited: list[tuple[str, str]], depth: int = 0) -> None:
        if depth > 6 or t.get("_finalized"):
            return
        t["_finalized"] = True
        reserved = (set(FIXED_COLS) | set(t.get("key_extra") or [])
                    | {col for _, col in inherited})
        prefix = _table_prefix(t["parent_table"] or t["name"])
        t["columns"] = _table_columns(t.pop("columns_base", []), prefix, reserved)
        col_of = {c["member"]: c["column"] for c in t["columns"]}
        # 作用域是**表级**的：声明式共享实体（clan/cupteam）按世界一行，子表随父表。
        scope = list(t.get("scope") or SCOPE_ORDER)
        if t["shape"] == "root":
            # 列名优先查本表的列映射（成员可能因撞固定列被前缀化），查不到才退回
            # 成员名/蛇形名。**作用域名也要查**：`pilot_id` 这个成员在这里是
            # 「元素自己的身份」（落库列 `party_member_pilot_id`），直接当列名用会
            # 把它当成作用域列本身。
            own = [(n, col_of.get(n) or (n if n in SCOPE_ORDER else _snake(n)))
                   for n in (o.get("pk_members") or [])]
            # 成员名就叫 `pilot_id` 时默认它就是**作用域列本身**，不该在自键里重复。
            # 但它要是因与固定列撞名被前缀化（`party_member_pilot_id`），那个值就不是
            # 行主维度、而是元素自己的身份——按成员名一刀切会把它从键里丢掉，同队的
            # 多个成员于是互相覆盖。判据落在**列**上：列名与成员名不同 ⇒ 它是自键。
            own = [(m, c) for m, c in own if m not in SCOPE_ORDER or c != m]
            keys = scope + [m for m, _ in own]
            t["key_members"] = _uniq(keys + list(t.get("key_extra") or []))
            t["primary_key"] = _uniq(scope
                                     + [c for _, c in own]
                                     + list(t.get("key_extra") or []))
            down = own
        else:
            keys = scope + [m for m, _ in inherited]
            t["key_members"] = _uniq(keys + list(t.get("key_extra") or []))
            t["primary_key"] = _uniq(scope
                                     + [c for _, c in inherited]
                                     + list(t.get("key_extra") or []))
            down = inherited
        for link in t.get("links") or []:
            ci = idx.get(link.get("child_table") or "")
            if ci is not None:
                ci[1]["scope"] = list(scope)
                walk(ci[0], ci[1], down, depth + 1)

    for o in sorted(objects.values(), key=lambda z: z["id"]):
        for t in o["tables"]:
            if t["shape"] == "root":
                walk(o, t, [])
    for o in objects.values():
        for t in o["tables"]:
            t.pop("columns_base", None)
            t.pop("_finalized", None)
        o["links"] = [z for t in o["tables"] for z in t["links"]]


def _uniq(items: list[str]) -> list[str]:
    out: list[str] = []
    for x in items:
        if x not in out:
            out.append(x)
    return out


def build_table_graph(objects: dict[str, dict], m: "Model",
                      ov: dict | None = None) -> list[str]:
    """建**表图**（docs/05 §4.F）：按「父表 __ 成员名」递归展开。

    子表名用**成员名**（`bracket.nodes` → `game.bracket__nodes`），不用元素类型名
    （`bracket_node`）——旧 `plan.py` 就是这样命名的，手写面（
    `game.bracket__nodes` 在 `gm/dbapi_db_test.go`、`game.ms_rokaku__weapons` 在
    `lounge/msset_equipset_write_test.go`）与 GM 都按这个名字寻址，改名即破坏。

    * `element_composite_ref` → 数组 → 子表，键 += `elem_index`；
    * `composite_ref`         → 内嵌 → 1:1 子表，键 = 父键。

    **非 `PERSIST` 对象不建表**（docs/00 §3 / docs/05 §4.C）：`EVENT`（战斗/会话
    ephemeral）与 `TBD` 根在 DDL 里本就不存在，模型里也不该带一张「幻影表」——
    否则对象页与 `tables[]` 会显示一张库里没有的表，读的人分不清是「待建」还是
    「不建」。判据（disposition）在 `_project_base` 里已按 object 级合并算好。

    一个对象可投影**多张表**：既是命令顶层 `array` 元素（根表），又被别的对象当
    数组元素引用（子表副本）。旧库对 `unlockw` 正是两张都建
    （`game.unlockw` + `game.ms_rokaku__weapons`）——但两张表装同一批行必然漂移，
    所以这类情况按 `_overrides.json.member_rows_in_root` 裁成**只留根表一张**，
    父记录里那几格降为指向根表的视图链接（docs/05 §4.G#4）。

    返回「旧表守恒」的缺口说明（`PERSIST` 声明没有对象承载的情况）。
    """
    ov = ov or {}
    owner: dict[str, str] = {}
    for oid, o in objects.items():
        for c in o["folded_composites"]:
            owner.setdefault(c, oid)

    for o in objects.values():
        o["tables"] = []
        o["links"] = []
    built: set[tuple[str, str]] = set()
    conservation: list[str] = []
    retired = retire_map(ov)

    def add_root(obj: dict, name: str) -> bool:
        if name in retired:
            return False
        if obj.get("disposition") != "PERSIST":
            return False
        key = (obj["id"], name)
        if key in built:
            return True
        built.add(key)
        t = {"name": name, "shape": "root", "parent": "", "parent_table": "",
             "via_member": "", "key_extra": [],
             # 作用域（`world_id[, pilot_id]`）：声明式共享实体只按世界一行。
             "scope": list(obj.get("scope") or SCOPE_ORDER),
             "columns_base": obj["columns"],
             "links": [], "child_tables": []}
        obj["tables"].append(t)
        if not obj.get("table"):
            obj["table"] = name
        expand(obj, t)
        return True

    def expand(obj: dict, table: dict, depth: int = 0) -> None:
        if depth > 6:
            return
        for x in obj["members"]:
            kind = x.get("link_kind") or ""
            composite = x.get("link_composite") or ""
            if not kind:
                continue
            coid = owner.get(composite)
            if not coid:
                continue
            child_obj = objects[coid]
            # 子对象非 PERSIST（EVENT/TBD）：它的列本来就不落库，别建空壳子表，
            # 也别登记链接——否则父表会多一张没有任何列的子表。
            if child_obj.get("disposition") != "PERSIST":
                continue
            # 「行在别人的根表里」（`_overrides.json.member_rows_in_root`）：父记录里
            # 这几格只是定长线形上的**平铺视图**，行本身以元素自己的行键存在 `coid` 的
            # 根表里。这里不建 `父表__成员名` 副本（同一批行两张表必然漂移），改记一条
            # 指向根表的视图链接。
            mr = member_root_of(obj["id"], x["name"])
            if mr:
                target = f"game.{_stem_of(child_obj)}"
                table["links"].append({
                    "member": x["name"],
                    "column": x.get("column") or _snake(x["name"]),
                    "kind": kind,
                    "composite": composite,
                    "view_of_root": target,
                    "root_object": coid,
                    "count": _array_count(x.get("wire_type") or ""),
                    "length": x.get("length"),
                    "evidence_va": x.get("evidence_va", ""),
                })
                obj.setdefault("view_rows", []).append({
                    "member": x["name"],
                    "column": x.get("column") or _snake(x["name"]),
                    "root_object": coid,
                    "root_table": target,
                    "from_table": table["name"],
                    "count": _array_count(x.get("wire_type") or ""),
                    "evidence_va": x.get("evidence_va", ""),
                    "reason": mr.get("reason", ""),
                })
                continue
            name = f"{table['name']}__{_snake(x['name'])}"
            key = (child_obj["id"], name)
            if key in built:
                # 同对象同表名只建一次；链接仍要登记
                table["links"].append(_link(x, kind, composite, coid, name))
                child = next(t for t in child_obj["tables"] if t["name"] == name)
                table["child_tables"].append(name)
                expand(child_obj, child, depth + 1)
                continue
            built.add(key)
            child = {
                "name": name, "shape": "array" if kind == "array" else "nested",
                "parent": obj["id"], "parent_table": table["name"],
                "via_member": x["name"],
                "key_extra": ["elem_index"] if kind == "array" else [],
                # 子表随父表作用域：`clan__members` 也按世界一行。
                "scope": list(table.get("scope") or SCOPE_ORDER),
                "columns_base": child_obj["columns"],
                "links": [], "child_tables": [],
            }
            child_obj["tables"].append(child)
            table["links"].append(_link(x, kind, composite, coid, name))
            table["child_tables"].append(name)
            expand(child_obj, child, depth + 1)

    # 根表：形态为 root 的对象各建一张（命令顶层 array 元素 / 无人引用的线布局）
    for o in sorted(objects.values(), key=lambda z: z["id"]):
        if o.get("shape") != "root":
            continue
        add_root(o, f"game.{_stem_of(o)}")

    # 旧表守恒（docs/05 §4.F）：`schema/_meta/legacy_evidence.json`（冻结的旧表声明+旧库实况，
    # 由 `tools/freeze_legacy.py` 生成）里声明为 PERSIST 的每一张旧表，都必须在新模型里有同名
    # 根表 `game.<tbl 去前缀>`。
    #
    # 为什么读**冻结快照**而不是直接读 `_legacy_tables/`：这一门问的是「旧库那一堆表有没有
    # 静默丢」，而旧库按「无兼容」口径已经删干净了，证据只剩模型内的这一份快照。快照还顺手
    # 补了 `tbl_pilot` 的 disposition 缺口——它自己没写 `table_disposition`，只在注册表里写着
    # PERSIST，直接读表文件会让这一门**静默跳过 pilot**（快照的 `disposition_source` 记着出处）。
    #
    # 旧库就是按这些**人工声明**建的表，手写面（`store.ListBlockDetailRows`、
    # `store.NewBlockDetailRow`）与 GM 都按名寻址；而「形态」是从线引用推出来的
    # （嵌套结构算 child/nested），单靠形态会把「既有独立表、又被别的对象内嵌」
    # 的对象（`beginner_challenge_info` = `game.beginner_challenge_info` +
    # `game.pilot_detail__beginner_challenge_info`）的独立表静默丢掉。
    #
    # 要退役一张旧表，必须在 `_overrides.json.retire_tables` 里显式登记理由——
    # 不许静默丢表（`batch_02_fold` 的「不丢行、不合并」口径）。
    for stem, node in sorted(legacy_declared(m).items()):
        lt = node.get("declaration") or {}
        if str(lt.get("disposition") or "") != "PERSIST":
            continue
        tid = lt.get("id") or f"tbl_{stem}"
        name = f"game.{_snake(stem)}"
        if name in retired:
            continue
        ent = lt.get("entity_ref") or ""
        oid = next((o["id"] for o in objects.values() if o["id"] == ent), "")
        if not oid:
            oid = next((o["id"] for o in objects.values()
                        if ent in o["folded_composites"]), "")
        if not oid:
            conservation.append(f"{tid}: 旧表声明 PERSIST，但没有对象承载 {ent!r}")
            continue
        if not add_root(objects[oid], name):
            # 旧库声明 PERSIST、对象却判成非 PERSIST：两边口径冲突，**必须报出来**
            # 让人去认（改 disposition 还是退休旧表），不许静默丢表。
            o = objects[oid]
            conservation.append(
                f"{tid}: 旧库声明 PERSIST，但承载对象 {oid} 的 disposition="
                f"{o.get('disposition')}（不建表）——需人工对齐")

    # 列名/行键（表级）：与生成器固定列同名的成员在这里前缀化，见 `_finalize_tables`。
    _finalize_tables(objects)
    return conservation


def legacy_declared(m: Model | None = None) -> dict[str, dict]:
    """冻结的旧表证据 `schema/_meta/legacy_evidence.json` → `{表干: node}`。

    旧库按「无兼容」口径删掉后，旧表的**声明**（disposition/entity_ref/唯一键列序/列清单）
    只存在于这份快照里；守恒门与站点都从这里读。缺文件时直接失败并给出重跑命令——
    不允许退回「读 `_legacy_tables/` 目录」：那正是会静默漏掉 `tbl_pilot` 的旧路径。
    """
    path = SCHEMA / "_meta" / "legacy_evidence.json"
    if not path.is_file():
        raise FileNotFoundError(
            f"缺旧库冻结证据 {path}——先跑 python tools/freeze_legacy.py")
    return json.loads(path.read_text(encoding="utf-8")).get("tables") or {}


def retire_map(ov: dict) -> set[str]:
    """`_overrides.json.retire_tables` → 允许退役（不建根表）的旧表名集合。"""
    out: set[str] = set()
    for it in ov.get("retire_tables") or []:
        if isinstance(it, dict) and it.get("table"):
            out.add(str(it["table"]))
        elif isinstance(it, str):
            out.add(it)
    return out


def _link(x: dict, kind: str, composite: str, coid: str, child_name: str) -> dict:
    return {
        "member": x["name"],
        "column": x.get("column") or _snake(x["name"]),
        "kind": kind,
        "composite": composite,
        "child_object": coid,
        "child_table": child_name,
        "count": _array_count(x.get("wire_type") or ""),
        "length": x.get("length"),
        "evidence_va": x.get("evidence_va", ""),
    }


def _project_base(m: Model, objects: dict[str, dict], obj: dict) -> None:
    """就地补上 DDL 投影：表名 / 线体 / 键 / 不落库成员（反向覆盖门）。

    表名按形态分派（docs/05 §4.F）：
      * `root`   → `game.<旧表名或对象名>`；
      * `child`  → `game.<父表>__<对象名>`，行键 = 父键 + `elem_index`；
      * `inline` → **不建表**，成员前缀化内联进父表。
    """
    mems = obj["members"]
    persist = [x for x in mems if x["lifetime"] == "PERSIST"]
    if obj.get("disposition_override"):
        # 人工分类订正优先于成员默认（战斗 ephemeral 的复合体导入时常带 PERSIST）。
        obj["disposition"] = obj["disposition_override"]
    else:
        obj["disposition"] = "PERSIST" if persist else (
            "EVENT" if any(x["lifetime"] == "EVENT" for x in mems) else "TBD")
    shape = obj.get("shape") or "root"
    # 表名：锚点旧表名优先（保住 GM/手写面），否则按对象 id 新生成。
    # 真正的建表在 build_table_graph（跨对象、按成员名递归），这里只落对象级摘要。
    #
    # 非 PERSIST（EVENT/TBD）对象**不建表**：库里没有这张表，模型里也不该写一个
    # 表名，否则对象页/`tables[]` 会像在说「有一张待建的表」。要持久化战斗数据是
    # B6 的另一轮工作（docs/05 §9），入口写在 `no_table_reason` 上。
    if shape == "root" and obj["disposition"] != "PERSIST":
        obj["table"] = ""
        # 不建表的**欠账**要写在对象上（站点/报告直接展示）：人工给了 disposition
        # 理由的（`_overrides.json.disposition.<oid>.reason`）原样带上——那句子里写的
        # 是「等谁写、缺哪列、行为什么可派生」，比任何默认文案都有用。
        why = str(obj.get("disposition_reason") or "").strip()
        obj["no_table_reason"] = (
            f"disposition={obj['disposition']}（不建表）："
            + (why if why else
               "EVENT/TBD 的持久化见 docs/05 §4.C / §9 的 B6 入口"))
    else:
        obj["table"] = f"game.{_stem_of(obj)}" if shape == "root" else ""
    # 线体：**锚点表声明的实体复合体优先**，否则持久化视图里最长的那个。
    # 口径与首选取处一致（`body_view`），这里重取一次是幂等的：`apply_overrides`
    # 可能改了成员 lifetime，落库线体要跟着变；宽度也要重新对齐（`resolve_member_widths`）。
    view = body_view(m, obj)
    obj["wire_body"] = view
    resolve_member_widths(m, obj)
    # 键：scope 恒为 (world_id, pilot_id)（行主不变量），own 为 pk_members；
    # 子表把**顶层父行的键**抄下来再接 `elem_index`（口径同旧 plan.py `_inherit_keys`：
    # 否则一名机师两台机体的 `weapons[3]` 会互相覆盖）。
    # 「行在别人的根表里」的数组成员不算父对象的孩子：父记录里那几格只是线形平铺
    # 视图（docs/05 §4.G#4），不落一张自己 keyed 的表。
    children = [x["name"] for x in mems
                if x.get("element_composite_ref")
                and not member_root_of(obj["id"], x["name"])]
    nested = [x["name"] for x in mems if x.get("composite_ref")]
    own = list(obj.get("pk_members") or [])
    # 作用域恒为 `(world_id, pilot_id)`（行主不变量，docs/05 §6.1）——除了**声明式
    # 根对象**：跨机师共享的实体（`clan` / `cupteam`）按世界一行，带 `pilot_id`
    # 等于给每个机师复制一份战队，是错的。scope 由声明给出，落地到表与唯一索引。
    scope = list(obj.get("scope") or SCOPE_ORDER)
    # 反向覆盖门：每个非 PERSIST / padding 成员都要有理由
    excluded = []
    for x in mems:
        if x.get("ignored_reason"):
            excluded.append({"member": x["name"],
                             "reason": f"人工登记不落库：{x['ignored_reason']}",
                             "evidence_va": x.get("evidence_va", "")})
        elif x["lifetime"] != "PERSIST":
            excluded.append({"member": x["name"],
                             "reason": f"lifetime={x['lifetime']}",
                             "evidence_va": x.get("evidence_va", "")})
        elif x["role"] == "padding" or x.get("memory_only"):
            excluded.append({"member": x["name"],
                             "reason": "padding/memory_only",
                             "evidence_va": x.get("evidence_va", "")})
    obj["columns_excluded"] = excluded
    # 落库列清单（P4 的生成器直接消费）：字段名 → 列名（可被人工订正改写）。
    # **排除复合体链接**（`avatar` / `favms[720]` / `unlockw[3]` …）：它们是子表
    # 指针，不是本表的列；混进来会让生成器既建列又建子表。
    obj["columns"] = [
        {"member": x["name"],
         "column": x.get("column") or _snake(x["name"]),
         "role": x["role"],
         "wire_type": x["wire_type"],
         # `synthetic`：不在**任何**线复合体里的列（锚点表带来的兄弟字段，如
         # `pilot.slot`、`equip_set.equip_set_slot`）。线结构体没有这个成员，
         # 值只能由调用方显式传——生成器据此把它当**外部行键**而不是"从结构体取"。
         "synthetic": bool(x.get("anchor_column")) or not x.get("views"),
         # 含义与地址级出处也一起带下去：生成器对 `synthetic` 列走的是兜底路径
         # （复合体里没有这个成员，取不到 MemberShape），没有这两项，DDL 的列注释
         # 就只剩「行键/兄弟字段」，GM 从表注释里再也读不到这一列是什么。
         "meaning": x.get("meaning", ""),
         "evidence_va": x.get("evidence_va", ""),
         "pk": x["name"] in (obj.get("pk_members") or [])
         or x["name"] in SCOPE_ORDER}
        for x in persist
        if x["role"] != "padding" and not x.get("memory_only")
        and not x.get("ignored_reason")
        and not x.get("link_kind")
    ]
    obj["columns_expected"] = len(obj["columns"])
    # tables/keys 由 build_table_graph 在**所有**对象都准备好列之后统一建；
    # 这里先给 `keys` 一个可依赖的骨架（primary_key 稍后由表图补全）。
    obj["keys"] = {
        "scope": scope,
        "own": own,
        "inherited": _inherited_keys_of(objects, obj.get("parent") or "")
        if shape in ("child", "nested") else [],
        "primary_key": [],
        "pk_kind": obj.get("pk_kind", ""),
        "children": children,
        "nested": nested,
        "child_key": ["elem_index"],
    }


def build_roles_doc(objects: dict) -> dict:
    """角色词表 + 角色 → PG/Go 类型映射（L3 契约，P4 由 plan.py 消费）。"""
    _PG = {"u64": "BIGINT", "u32": "BIGINT", "u16": "SMALLINT", "u8": "SMALLINT",
           "i64": "BIGINT", "i32": "INTEGER", "i16": "SMALLINT", "i8": "SMALLINT"}
    _GO = {"u64": "uint64", "u32": "uint32", "u16": "uint16", "u8": "uint8",
           "i64": "int64", "i32": "int32", "i16": "int16", "i8": "int8"}
    counts = collections.Counter(x["role"] for o in objects.values()
                                 for x in o["members"])
    return {
        "note": "L3 角色闭集与类型映射；由 tools/derive_homing.py 生成",
        "generated": today(),
        "roles": {
            "identity": "对象自己的记录号 → PK/唯一键",
            "scope": "作用域（world_id/pilot_id）→ PK 前缀（行主不变量）",
            "slot": "槽位 → PK 一部分",
            "ref": "指向别的对象的身份 → FK",
            "counter": "驱动同结构数组条数 → 普通列",
            "flag": "布尔/位域 → BOOLEAN 或 SMALLINT",
            "timestamp": "游戏内时刻/期限 → 普通列",
            "attribute": "兜底标量/文本/原生数组 → 普通列",
            "padding": "对齐补位 → 不落库",
            "payload": "语义未定的定长块 → 整型数组（禁 BYTEA）",
        },
        "role_counts": dict(counts),
        "wire_to_pg": _PG,
        "wire_to_go": _GO,
        "opaque_pg": {"8": "BIGINT[]", "4": "INTEGER[]",
                      "2": "SMALLINT[]", "1": "SMALLINT[]"},
    }


# ------------------------------------------------------- 关联（FK）


def resolve_relations(objects: dict[str, dict]
                      ) -> tuple[list[dict], list[dict], list[dict], list[dict],
                                 list[dict]]:
    """汇总 role=ref / scope 的 FK，并把无解引用登记为悬空。

    `game.*` 外键只认 `fk_target`。主数据（`cfg.*` / `srv.*`）、战斗期句柄、
    已归类的模型外目标另开集合，不混进 `relations[]`——它们不是服务器写的表间关联。
    """
    relations: list[dict] = []
    dangling: list[dict] = []
    master: list[dict] = []
    runtime: list[dict] = []
    categorized: list[dict] = []
    for oid, o in objects.items():
        for fkrow in o.get("declared_fks") or []:
            relations.append({
                "from": fkrow["from"], "to": fkrow["to"], "kind": "fk",
                "basis": fkrow.get("basis", ""),
                "evidence_va": fkrow.get("evidence_va", ""),
                "declared": True,
            })
        for x in o["members"]:
            role = x.get("role")
            if role == "scope":
                relations.append({
                    "from": f"{oid}.{x['name']}",
                    "to": CROSS_SCHEMA_TARGET[norm(x["name"])],
                    "kind": "scope_fk",
                    "evidence_va": x.get("evidence_va", ""),
                })
            elif role == "ref":
                tgt = x.get("fk_target")
                kind = x.get("ref_kind") or ""
                if tgt:
                    relations.append({
                        "from": f"{oid}.{x['name']}", "to": tgt, "kind": "fk",
                        "basis": x.get("ref_basis", ""),
                        "evidence_va": x.get("evidence_va", ""),
                    })
                elif kind == "master":
                    master.append({
                        "from": f"{oid}.{x['name']}",
                        "to": x.get("master_target") or "",
                        "basis": x.get("ref_basis", ""),
                        "evidence_va": x.get("evidence_va", ""),
                    })
                elif kind in ("runtime", "dangling"):
                    # 都不是 game.* 外键：runtime 是本场内存句柄；dangling 是人工
                    # 裁决过、目标在本轮模型之外的引用（类别见 ref_category）。
                    row = {
                        "from": f"{oid}.{x['name']}",
                        "kind": kind,
                        "basis": x.get("ref_basis", ""),
                        "evidence_va": x.get("evidence_va", ""),
                    }
                    if kind == "dangling":
                        row["category"] = x.get("ref_category", "")
                        categorized.append(row)
                    else:
                        runtime.append({
                            "from": row["from"], "basis": row["basis"],
                            "evidence_va": row["evidence_va"]})
                else:
                    dangling.append({
                        "from": f"{oid}.{x['name']}",
                        "reason": "引用目标未解析（见 unresolved.md §3）",
                        "evidence_va": x.get("evidence_va", ""),
                    })
    return relations, dangling, master, runtime, categorized


# ------------------------------------------------------- 人工订正（复核批次产物）


def load_overrides() -> dict:
    """人工裁决（P2 复核批次的产物）。**必须被 emit 保住**，不能被重跑清掉。"""
    p = HOMING / "_overrides.json"
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  WARN _overrides.json 解析失败：{e}", file=sys.stderr)
        return {}


def apply_overrides(objects: dict[str, dict], ov: dict) -> list[str]:
    """把人工裁决叠到推导结果上。返回订正过程中发现的问题（拼错的名字等）。"""
    notes: list[str] = []

    for name, spec in (ov.get("pk") or {}).items():
        o = objects.get(name)
        if not o:
            notes.append(f"pk 订正指向不存在的对象 {name!r}")
            continue
        mem = {x["name"] for x in o["members"]}
        bad = [c for c in spec if c not in mem]
        if bad:
            notes.append(f"{name}: pk 订正指定了不存在的成员 {bad}")
        keep = [c for c in spec if c in mem]
        if keep:
            o["pk_members"] = keep
            o["pk_kind"] = "override"
            o["is_root"] = True
            for x in o["members"]:
                if x["name"] in keep and x["role"] in ("ref", "attribute"):
                    # 带 `fk_target` 的成员**保持 role=ref**：它既是行键的一部分、又指向
                    # 另一张表（`party_member.party_id` → `party.party_id`）。改成
                    # identity 后 `resolve_relations` 就不再发这条外键（它只看 role）。
                    if x.get("fk_target"):
                        continue
                    x["role"] = "identity"

    # 作用域订正：默认每个对象按 `(world_id, pilot_id)` 一行（行主不变量）。**共享实体
    # 的元素表**是例外——`party_member` / `party_member_stat` 的行是「某队的某个成员」，
    # 主语是队伍不是读方机师：带上读方 `pilot_id` 等于给每个机师复制一份成员表，
    # 而元素自己的身份列（成员机师 + 所属队伍）才是唯一键。写法：
    # `{"party_member": ["world_id"]}`。**只允许在作用域维度里取子集**，不许新增维度。
    for oid, scope in (ov.get("scope") or {}).items():
        if str(oid).startswith("_"):
            continue
        o = objects.get(oid)
        if o is None:
            raise SystemExit(f"_overrides.json.scope: 模型里没有对象 {oid!r}")
        bad = [str(s) for s in scope if str(s) not in SCOPE_ORDER]
        if bad:
            raise SystemExit(f"_overrides.json.scope.{oid}: 不是作用域维度 {bad}")
        if not scope:
            raise SystemExit(f"_overrides.json.scope.{oid}: 不能为空（行主不变量至少 "
                             "要有 world_id）")
        o["scope"] = [str(s) for s in scope]

    for key, role in (ov.get("role") or {}).items():
        x, o = _find_member(objects, key)
        if x is None:
            notes.append(f"role 订正找不到 {key!r}")
            continue
        if role not in ROLES:
            notes.append(f"role 订正给了未知角色 {role!r} @ {key}")
            continue
        x["role"] = role
        if role != "ref":
            x.pop("fk_target", None)

    for key, tgt in (ov.get("fk") or {}).items():
        x, o = _find_member(objects, key)
        if x is None:
            notes.append(f"fk 订正找不到 {key!r}")
            continue
        x["role"] = "ref"
        x["fk_target"] = str(tgt)
        x["ref_basis"] = "人工订正"

    for key, reason in (ov.get("ignore") or {}).items():
        x, o = _find_member(objects, key)
        if x is None:
            notes.append(f"ignore 订正找不到 {key!r}")
            continue
        x["ignored_reason"] = str(reason)

    # 列名订正：字节模型字段名 → 旧库列名（手写面按旧列名寻址，不能改名）。
    # 例：`item.inv_place` → `slot`（现网 UNIQUE `uq_game_item_world_pilot_slot`
    # 与 `store/shop_buy.go` 都用 `slot`）。
    for key, col in (ov.get("colname") or {}).items():
        x, o = _find_member(objects, key)
        if x is None:
            notes.append(f"colname 订正找不到 {key!r}")
            continue
        x["column"] = str(col)

    # 对象级 disposition 订正：改的是**分类**，不是键形状。用于「自动导入时随了
    # 默认 `PERSIST`、其实按 docs/00 §3 属战斗/会话 ephemeral」的对象——它们不该
    # 有表，也不该来抢行键。改完由 `_project_base` 重算，DDL 自然不再收这张表。
    for oid, spec in (ov.get("disposition") or {}).items():
        if str(oid).startswith("_"):
            continue
        o = objects.get(oid)
        if o is None:
            notes.append(f"disposition 订正指向不存在的对象 {oid!r}")
            continue
        # 两种写法：`"EVENT"`，或 `{"as": "EVENT", "reason": "…"}`（理由要留档）。
        if isinstance(spec, dict):
            disp = str(spec.get("as") or spec.get("disposition") or "")
            reason = str(spec.get("reason") or "")
        else:
            disp, reason = str(spec), ""
        if disp not in DISPOSITIONS:
            notes.append(f"disposition 订正给了未知值 {disp!r} @ {oid}")
            continue
        o["disposition_override"] = disp
        if reason:
            o["disposition_reason"] = reason

    # 「无身份根」的两类裁决：只是把结论**记在对象上**（供站点与未决报告分栏），
    # 不改键形状。校验它们仍然指着一个真的无身份根——不然裁决已经过期，
    # 留着会掩盖新长出来的缺口。
    decided_one, decided_nw = pk_gap_decisions()
    # 「已并表退场」的 id 不算过期裁决：`no_writer` 这一栏记的是「历史上判过 0 CS 写方」
    # 这件事，对象被 `fold` 折进宿主后它本身就不存在了（`block_detail` → `pilot`）。
    # 区别对待「并表」与「写错名字」，否则每次跑引擎都会刷一屏假警告。
    fold_host: dict[str, str] = {}
    for g in ov.get("fold") or []:
        if isinstance(g, dict):
            for c in g.get("composites") or []:
                fold_host[str(c)] = str(g.get("as") or "")
    for tag, table in (("singleton", decided_one), ("no_writer", decided_nw)):
        for oid, reason in table.items():
            o = objects.get(oid)
            if o is None:
                if oid in fold_host:
                    continue
                notes.append(f"{tag} 裁决指向不存在的对象 {oid!r}")
                continue
            if o.get("pk_members"):
                notes.append(f"{tag} 裁决的对象 {oid} 已有自己的行键，裁决已过期")
                continue
            o[f"{tag}_reason"] = reason

    # 词干级引用裁决（`ref_stem`）：在本轮 `assign_roles` 里已经被 `_stem_verdict`
    # 消费。这里只做两件收尾——校验格式，以及检出**已过期**的裁决（词干改名/字段
    # 消失后没人再问它）。过期的裁决留着会让人以为「这词干已经判过了」。
    _KINDS = {"master", "fk", "runtime", "notref", "dangling"}
    for stem, spec in (_REF_STEM or {}).items():
        kind = str(spec.get("kind") or "")
        if kind not in _KINDS:
            notes.append(f"ref_stem 裁决 {stem!r} 的 kind 未知：{kind!r}")
        if kind in ("master", "fk") and not str(spec.get("target") or "").strip():
            notes.append(f"ref_stem 裁决 {stem!r} 是 {kind} 却没写 target")
        if kind == "master" and not str(spec.get("target") or "").startswith(
                ("cfg.", "srv.")):
            notes.append(f"ref_stem 裁决 {stem!r} 的 master 目标不是 cfg./srv.："
                         f"{spec.get('target')!r}")
        if kind == "fk" and "." not in str(spec.get("target") or ""):
            notes.append(f"ref_stem 裁决 {stem!r} 的 fk 目标没有 `<对象>.<列>` 形状："
                         f"{spec.get('target')!r}")
        if not str(spec.get("reason") or "").strip():
            notes.append(f"ref_stem 裁决 {stem!r} 没写理由（不臆造是硬要求）")
        if stem not in _REF_STEM_HITS:
            notes.append(f"ref_stem 裁决 {stem!r} 本轮没有任何字段命中（已过期？）")

    return notes


def _find_member(objects: dict, key: str) -> tuple[dict | None, dict | None]:
    oname, _, mname = key.partition(".")
    o = objects.get(oname)
    if not o:
        return None, None
    x = next((m for m in o["members"] if m["name"] == mname), None)
    return x, o


def recompute_ref_notes(objects: dict[str, dict]) -> list[dict]:
    """重扫「role=ref 且**真未决**」→ 未决。

    主数据（`cfg.*`）与战斗期句柄虽然也没有 `fk_target`，但**已经解释清楚了**
    （`ref_kind` = master / runtime），不能算「判不了」，否则又会虚报一批引用。
    `notref`（名字以 id 结尾但不是引用）与 `dangling`（人工裁决过、目标在本轮模型
    之外）同样有归宿，也不算未决。人工订正过的自动消失。
    """
    out = []
    for oid, o in objects.items():
        for x in o["members"]:
            if x.get("role") != "ref" or x.get("fk_target"):
                continue
            if (x.get("ref_kind") or "") in (
                    "master", "runtime", "self", "notref", "dangling"):
                continue
            out.append({"object": oid, "field": x["name"],
                        "reason": x.get("ref_basis") or "引用目标未解析",
                        "evidence_va": x.get("evidence_va", "")})
    return out


def explained_refs(objects: dict[str, dict]
                   ) -> tuple[list[dict], list[dict], list[dict]]:
    """主数据 / 战斗期句柄 / 已归类悬空（都不是缺口），供 unresolved.md 分栏展示。"""
    master: list[dict] = []
    runtime: list[dict] = []
    dangling: list[dict] = []
    for oid, o in objects.items():
        for x in o["members"]:
            if x.get("role") != "ref":
                continue
            k = x.get("ref_kind") or ""
            row = {"object": oid, "field": x["name"],
                   "basis": x.get("ref_basis", ""),
                   "evidence_va": x.get("evidence_va", "")}
            if k == "master":
                row["target"] = x.get("master_target", "")
                master.append(row)
            elif k == "runtime":
                runtime.append(row)
            elif k == "dangling":
                row["category"] = x.get("ref_category", "")
                dangling.append(row)
    return master, runtime, dangling


# ------------------------------------------------------- 落盘


def _clean_outputs() -> None:
    """只清引擎产出的文件；`_overrides.json` 等人工产物必须留下。

    Windows 上 `objects/` 目录本身可能被别的进程（编辑器索引、`rg`/`findstr` 之类）
    按句柄占住，`shutil.rmtree` 会在**删完里面的文件之后**才在最后一步 `rmdir`
    上抛 `WinError 32`——整轮重跑就此半途而废，且模型已处于只删不写的破损状态。
    所以这里逐个删文件，目录删不掉就留着（只要它里面是空的，本轮重建照样干净）。
    """
    d = HOMING / "objects"
    if d.is_dir():
        for p in d.iterdir():
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
            else:
                p.unlink(missing_ok=True)
        try:
            d.rmdir()
        except OSError:
            pass
    for name in ("fields.jsonl", "relations.json", "roles.json",
                 "summary.json", "unresolved.md"):
        p = HOMING / name
        if p.exists():
            p.unlink()


def split_relations(objects: dict[str, dict],
                    relations: list[dict]) -> tuple[list[dict], list[dict]]:
    """按**源对象是否建表**把 `relations` 分两桶（docs/05 §9.9）。

    `relations[]` 在站点上画的是「表间外键」，而 `DERIVED`/`EVENT`/`CONFIG`/`TBD`
    的对象**没有表**（`table == ""`）——它们的成员引用照旧留在线条里、仍然是证据，
    但**不可能**成为 DDL 外键：库里没有源表。混在 `relations[]` 里会让「外键」
    这一栏包含一批永远建不出来的边（本批退役 35 张表后，59 条里有 29 条如此）。

    所以：源对象 `disposition == "PERSIST"` → 留在 `relations[]`；否则移进
    `wire_refs[]`，并补 `source_object` / `source_disposition` / `reason`
    说明「为什么它只是线上引用」。**一条都不丢**（两桶之和 == 输入长度），
    守卫按这一点断言。
    """
    live: list[dict] = []
    wire: list[dict] = []
    for r in relations:
        src = str(r.get("from", "")).split(".")[0]
        o = objects.get(src)
        if o is not None and o.get("disposition") == "PERSIST":
            live.append(r)
            continue
        row = dict(r)
        row["source_object"] = src
        row["source_disposition"] = (o or {}).get("disposition") or "no_object"
        row["reason"] = (
            f"源对象 {src} 判 {row['source_disposition']}，不建表（"
            + (str((o or {}).get("no_table_reason") or "")
               or "见 _overrides.json.disposition")
            + "）——这条引用只在线体里成立，库里没有源表可建外键")
        wire.append(row)
    return live, wire


def emit(objects: dict[str, dict], relations: list[dict], dangling: list[dict],
         metrics: dict, unresolved: list[str], master: list[dict] | None = None,
         runtime: list[dict] | None = None) -> None:
    master = master or []
    runtime = runtime or []
    rel_live, wire_refs = split_relations(objects, relations)
    _clean_outputs()
    (HOMING / "objects").mkdir(parents=True, exist_ok=True)

    for oid, o in objects.items():
        (HOMING / "objects" / f"{oid}.json").write_text(
            json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (HOMING / "relations.json").write_text(
        json.dumps({
            "note": "由 tools/derive_homing.py 从字节级模型推导；每条带 evidence_va",
            "generated": today(),
            # 只收**源表存在**的边：站点/DDL 都把这一栏当外键看。
            "relations": rel_live,
            # 源对象不建表（DERIVED/EVENT/CONFIG/TBD）的引用：仍是线体证据，
            # 但库里没有源表 ⇒ 建不出外键，单列免被误读成「缺了一批外键」。
            "wire_refs": wire_refs,
            "dangling": dangling,
            # 主数据引用（cfg.* 静态配置）与战斗期句柄：**不是** game.* 外键，
            # 单列以免被误读成「缺了一批外键」（见 docs/05 §4.E）。
            "master_refs": master,
            "runtime_refs": runtime,
            # 已归类悬空：目标不在本轮模型内（世界级实体/本地表资源/值对象），
            # 逐词干裁决写在 `_overrides.json.ref_stem`（见 docs/05 §9.2）。
            "categorized_refs": explained_refs(objects)[2],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (HOMING / "roles.json").write_text(
        json.dumps(build_roles_doc(objects), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    # 归位表：一行一个 (对象, 字段) 实例
    with (HOMING / "fields.jsonl").open("w", encoding="utf-8") as fh:
        for oid, o in sorted(objects.items()):
            for x in o["members"]:
                land = x["lifetime"] == "PERSIST" and x["role"] != "padding" \
                    and not x.get("memory_only")
                fh.write(json.dumps({
                    "object": oid,
                    "domain": o["domain"],
                    "field": x["name"],
                    "wire_type": x["wire_type"],
                    "length": x["length"],
                    "lifetime": x["lifetime"],
                    "views": x["views"],
                    "role": x["role"],
                    "is_pk": x["name"] in (o.get("pk_members") or []),
                    "table": o["table"] if land else "",
                    "column": (x.get("column") or _snake(x["name"])) if land else "",
                    "fk_target": x.get("fk_target", ""),
                    "writer_count": len(o["writes"]),
                    "reader_count": len(o["reads"]),
                    "evidence_va": x.get("evidence_va", ""),
                    "memory_only": bool(x.get("memory_only")),
                }, ensure_ascii=False) + "\n")

    cov = coverage(objects)
    cat_refs = explained_refs(objects)[2]
    root_persist = sum(
        1 for o in objects.values()
        if o.get("is_root") and o["disposition"] == "PERSIST")
    n_persist = sum(1 for o in objects.values()
                    for x in o["members"] if x["lifetime"] == "PERSIST")
    summary = {
        "generated": today(),
        "objects": len(objects),
        "objects_root": cov["objects_root"],
        "objects_value": cov["objects_value"],
        "objects_persist": sum(1 for o in objects.values()
                               if o["disposition"] == "PERSIST"),
        "composites_folded": sum(len(o["folded_composites"]) for o in objects.values()),
        "members_total": sum(len(o["members"]) for o in objects.values()),
        "members_persist": sum(1 for o in objects.values()
                               for x in o["members"] if x["lifetime"] == "PERSIST"),
        "members_event": sum(1 for o in objects.values()
                             for x in o["members"] if x["lifetime"] == "EVENT"),
        "members_tbd": sum(1 for o in objects.values()
                           for x in o["members"] if x["lifetime"] == "TBD"),
        "columns_expected": sum(o.get("columns_expected", 0)
                                for o in objects.values()),
        "roles": dict(collections.Counter(
            x["role"] for o in objects.values() for x in o["members"])),
        "relations": len(rel_live),
        "relations_by_kind": dict(collections.Counter(
            r["kind"] for r in rel_live)),
        # 源对象不建表的引用（见 split_relations）
        "wire_refs": len(wire_refs),
        "wire_refs_by_kind": dict(collections.Counter(
            r["kind"] for r in wire_refs)),
        "master_refs": len(master),
        "runtime_refs": len(runtime),
        "ref_categorized": len(cat_refs),
        "ref_categories": dict(collections.Counter(
            r["category"] for r in cat_refs)),
        "dangling": len(dangling),
        "ref_unresolved": len(metrics.get("ref_notes") or []),
        "coverage": cov,
        "anchors": metrics["anchors"],
        "gates": {
            "composites_all_folded": not cov["composites_missing"],
            "root_persist_objects": root_persist,
            "roots_without_pk": len(cov["roots_without_pk"]),
            "roots_singleton": len(cov.get("roots_singleton") or []),
            "roots_no_writer": len(cov.get("roots_no_writer") or []),
            "non_persist_tables": len(cov.get("non_persist_tables") or []),
            "columns_with_va": n_persist - cov["members_without_va"],
            "members_with_ref_only": cov["members_without_va"]
            - cov["members_without_any_evidence"],
            "members_with_no_evidence": cov["members_without_any_evidence"],
            "dangling_fk": len(dangling),
            "master_refs": len(master),
            "runtime_refs": len(runtime),
            "categorized_refs": len(cat_refs),
            "unresolved_refs": len(metrics.get("ref_notes") or []),
            "unlinked_layout_twins": len(metrics.get("twins") or []),
            "twins_reviewed": int(metrics.get("twins_reviewed") or 0),
        },
    }
    (HOMING / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    write_unresolved(objects, dangling, cov, unresolved, metrics)


def _snake(name: str) -> str:
    s = re.sub(r"[^0-9a-zA-Z]+", "_", name or "").strip("_").lower()
    s = re.sub(r"_+", "_", s)
    if s and s[0].isdigit():
        s = "f_" + s
    return s[:60] or "f"


def twin_key(cids: list[str]) -> str:
    """孪生组的稳定键（`_overrides.json.twin_verdicts` 用它当 key）。

    排序后 `+` 连接——与 `layout_twins` 的分组签名同源，改线布局不影响键。
    """
    return "+".join(sorted(cids))


def layout_twins(m: Model, objects: dict[str, dict],
                 reviewed: set[str] | None = None) -> list[list[str]]:
    """线布局逐字节同形、但没有 `layout_same_as` 连起来的复合体（折叠候选）。

    `favms` 与 `favms_add` 就是这种：66B / 18 成员 / 名字逐个相同，却分属两个对象。
    引擎**不擅自合并**——这是业务判断；只登记成候选供人工拍板（docs/05 §9 风险 1）。

    `reviewed` 是 `_overrides.json.twin_verdicts` 里**已逐组裁决过**的组键
    （`twin_key`）——裁决过的组不再报（它们是「判过了」，不是「没判」，口径同
    `singleton`/`no_writer` 两个桶）。`fold` 裁决的组本来就折成一个对象、自然不进清单。
    """
    sig: dict[tuple, list[str]] = collections.defaultdict(list)
    for cid, c in m.composites.items():
        names = tuple(sorted(norm(x.get("name") or "")
                             for x in c.get("members") or []))
        sig[(c.get("length"), names)].append(cid)
    owner: dict[str, str] = {}
    for oid, o in objects.items():
        for cid in o["folded_composites"]:
            owner[cid] = oid
    twins = []
    for _key, cids in sig.items():
        if len(cids) < 2:
            continue
        if len({owner.get(c) for c in cids}) < 2:
            continue        # 已折在同一对象里
        grp = sorted(cids)
        if reviewed and twin_key(grp) in reviewed:
            continue        # 人工逐组裁决过（twin_verdicts），不再当未决候选
        twins.append(grp)
    return sorted(twins)


def _gap_reason(v: dict) -> str:
    """已知缺口（不是引擎失职）：来源复合体未完成分解，或成员名就是占位符。"""
    if _is_placeholder(v.get("name") or ""):
        return "字节模型里的占位成员（待从 protocol 补取）"
    st = {s for s in (v.get("statuses") or set()) if s}
    if st and "complete" not in st:
        return f"来源复合体未完成分解（status={'/'.join(sorted(st))}）"
    return ""


def pk_gap_decisions() -> tuple[dict[str, str], dict[str, str]]:
    """`_overrides.json` 里对「无自身身份列的 PERSIST 根」的两类人工裁决。

    返回 `(已裁决单行, 暂无写入方)`：对象 id → 理由。

    这两个桶**不是**「没定」而是「定过了」，所以从 `roots_without_pk`（未决）
    里移出来单列——否则 40 条未决里混着 25 条早有旧库背书的结论，守卫每跑一次
    都要重看一遍同样的清单。

      * `singleton`  —— 判为**每个作用域一行**（旧库 UNIQUE 逐列一致，或语义上
        就是一个机师一份的偏好/状态）。DDL 键形状**不变**，仍 `(world_id, pilot_id)`。
      * `no_writer`  —— 判为**服务端当前没有写入方**（0 个 CS 写命令，只被 SC 读
        下发）。键形状在「无写入方」下不可能丢行，但**接入写入方前必须先定身份列**，
        所以理由里记清欠账，不留白。
    """
    ov = load_overrides()
    one = {str(k): str(v) for k, v in (ov.get("singleton") or {}).items()
           if not str(k).startswith("_")}
    nw = {str(k): str(v) for k, v in (ov.get("no_writer") or {}).items()
          if not str(k).startswith("_")}
    return one, nw


def coverage(objects: dict[str, dict]) -> dict:
    all_c = {c["id"] for c in load_dir("composites")}
    folded = {c for o in objects.values() for c in o["folded_composites"]}
    roots = {oid: o for oid, o in objects.items() if o.get("is_root")}
    # 只有「根对象」才需要自己的行键；`EVENT`/`TBD` 根不建表（§4.C），
    # 把它们的行键算进未决会虚高指标——单列出来看。
    persist_roots = {oid: o for oid, o in roots.items()
                     if o.get("disposition") == "PERSIST"}
    decided_one, decided_nw = pk_gap_decisions()
    # 「无自身身份列」= 没有自己的行键，**不看有没有 scope 列**：scope 只在
    # 「确定单行」时才够用（docs/05 §4.E），而 news/comment 这种「SC 当顶层数组
    # 下发」的对象正因带 scope 逃过了上一版守卫（数组元素却按单行建表 = 静默压行）。
    gap = sorted(oid for oid, o in persist_roots.items()
                 if not o.get("pk_members"))
    return {
        "composites_total": len(all_c),
        "composites_folded": len(folded),
        "composites_missing": sorted(all_c - folded),
        "objects_root": len(roots),
        "objects_value": len(objects) - len(roots),
        "roots_persist": len(persist_roots),
        "roots_event_or_tbd": len(roots) - len(persist_roots),
        # 值对象由父行定位，豁免；EVENT/TBD 不建表，豁免。
        # 三个缺口集合**互斥**：已裁决单行 / 暂无写入方 / 仍未决。
        "roots_singleton": [oid for oid in gap if oid in decided_one],
        "roots_no_writer": [oid for oid in gap if oid in decided_nw],
        "roots_without_pk": [oid for oid in gap
                             if oid not in decided_one and oid not in decided_nw],
        # 幻影表门：非 PERSIST（EVENT/TBD）对象不得带任何表——库里不建，模型里
        # 也不许写。`build_table_graph` 已按 disposition 挡掉，这里断言它真的挡住了。
        "non_persist_tables": sorted(
            t["name"] for o in objects.values()
            if o.get("disposition") != "PERSIST"
            for t in o.get("tables") or []),
        "objects_no_table": sorted(
            oid for oid, o in objects.items()
            if o.get("is_root") and o.get("disposition") != "PERSIST"),
        "members_without_va": sum(
            1 for o in objects.values() for x in o["members"]
            if not x.get("evidence_va")),
        # 无 VA 但有 (命令 + 子程序 + README 章节) 定位 → 软缺口，可追溯
        "members_without_any_evidence": sum(
            1 for o in objects.values() for x in o["members"]
            if not x.get("evidence_va") and not x.get("evidence_ref")),
        # 无任何出处、但**已知**是模型缺口（占位成员 / 未完成分解）→ 不算失职
        "members_known_gap": sum(
            1 for o in objects.values() for x in o["members"]
            if not x.get("evidence_va") and not x.get("evidence_ref")
            and x.get("known_gap")),
        # 真正的失职：无出处且不是已知缺口
        "members_unjustified": sum(
            1 for o in objects.values() for x in o["members"]
            if not x.get("evidence_va") and not x.get("evidence_ref")
            and not x.get("known_gap")),
    }


def write_unresolved(objects: dict[str, dict], dangling: list[dict],
                     cov: dict, unresolved: list[str], metrics: dict) -> None:
    L: list[str] = [
        "# 字段归位 · 未决清单",
        "",
        "> 由 `tools/derive_homing.py` 生成。**只列引擎判不了的**，供人工批次裁决；",
        "> 每条都带推理依据，不做臆造。裁决结果写回 `homing/_overrides.json` 后重跑。",
        "",
        f"生成日期：{today()}",
        "",
        "## 1. 未折入任何对象的复合体",
        "",
    ]
    if cov["composites_missing"]:
        L += ["| 复合体 | 线长 | 可能的去处 |", "|---|---|---|"]
        for cid in cov["composites_missing"]:
            L.append(f"| `{cid}` | | 需人工判定 |")
    else:
        L.append("（无：132 个复合体全部折入对象）")
    L += ["", "## 2. 无身份（PK）的根对象（仍未决）", "",
          "根对象（有作用域列/有旧表锚点）却没有自己的行键：只能退回 "
          "`(world_id, pilot_id)` 单行，多条记录会互相 upsert 覆盖。", "",
          "下面只列**没定**的；已裁决定性的两类见 §2b/§2c。", ""]
    if cov["roots_without_pk"]:
        L += ["| 对象 | 域 | 成员数 | 线视图 |", "|---|---|---|---|"]
        for oid in cov["roots_without_pk"]:
            o = objects[oid]
            L.append(f"| `{oid}` | {o['domain']} | {len(o['members'])} | "
                     f"{', '.join(o['folded_composites'])} |")
    else:
        L.append("（无）")
    L += ["", "## 2b. 已裁决：单行（每个作用域一行）", "",
          "裁决为「一个机师（或一个作用域）一行」。DDL 键形状**不变**，仍是 "
          "`(world_id, pilot_id)`；结论与依据记在 `_overrides.json.singleton`。", ""]
    if cov.get("roots_singleton"):
        L += ["| 对象 | 依据 |", "|---|---|"]
        for oid in cov["roots_singleton"]:
            L.append(f"| `{oid}` | {objects[oid].get('singleton_reason', '')} |")
    else:
        L.append("（无）")
    L += ["", "## 2c. 已裁决：暂无写入方（键待定）", "",
          "在**写侧**（CS）没有任何写入方，只被 SC 读下发。没有写入方就不可能丢行，"
          "所以不阻塞；但接入写入方之前必须先定身份列，理由逐条记在 "
          "`_overrides.json.no_writer`。", ""]
    if cov.get("roots_no_writer"):
        L += ["| 对象 | 依据 |", "|---|---|"]
        for oid in cov["roots_no_writer"]:
            L.append(f"| `{oid}` | {objects[oid].get('no_writer_reason', '')} |")
    else:
        L.append("（无）")
    L += ["", "## 3. 引用未解析（`X_id` 指不到唯一对象）", "",
          "`X_id` 形式的成员已判为 `ref`，但对象名索引给不出**唯一**目标，"
          "且不属于下面 §3b/§3c 两类。多为「一族派生表都叫 clan」这类需要业务拍板的情况。", ""]
    ref_notes = metrics.get("ref_notes") or []
    if ref_notes:
        L += ["| 对象 | 字段 | 原因 | 证据 VA |", "|---|---|---|---|"]
        for r in ref_notes:
            L.append(f"| `{r['object']}` | `{r['field']}` | {r['reason']} | "
                     f"`{r['evidence_va']}` |")
    else:
        L.append("（无）")
    mrefs, rrefs, drefs = explained_refs(objects)
    L += ["", "## 3b. 主数据引用（`cfg.*` 静态配置，**不是** `game.*` 外键）", "",
          "这些 `X_id` 指向 `cfg` schema 的静态配置表（表在客户端/工具侧，服务器不写）。"
          "按 §4.E 口径，它们**不出 `relations.json` 的 `relations[]`**，"
          "单列在 `master_refs`。目标表有多候选的仍需人工点定。", ""]
    if mrefs:
        L += ["| 对象 | 字段 | 候选目标 | 依据 | 证据 VA |", "|---|---|---|---|---|"]
        for r in mrefs:
            L.append(f"| `{r['object']}` | `{r['field']}` | `{r['target']}` | "
                     f"{r['basis']} | `{r['evidence_va']}` |")
    else:
        L.append("（无）")
    L += ["", "## 3c. 战斗期实体句柄（本场内存，不落库）", "",
          "只在 battle 命令里出现的 `*ent_id`：指向本场战斗内存里的实体，"
          "**不落任何表**，故无所谓外键。", ""]
    if rrefs:
        L += ["| 对象 | 字段 | 证据 VA |", "|---|---|---|"]
        for r in rrefs:
            L.append(f"| `{r['object']}` | `{r['field']}` | `{r['evidence_va']}` |")
    else:
        L.append("（无）")
    L += ["", "## 3d. 已归类：引用目标不在本轮模型（保留普通列）", "",
          "这些 `X_id` 已逐词干裁决（`_overrides.json.ref_stem`）：**目标不是一个"
          "可以指过去的表**，所以既不是 `game.*` 外键、也不是 cfg 主数据。"
          "它们照常落列（无 FK 约束），类别用来区分「模型缺对象」与「本来就不是引用」。"
          "类别：`world_entity` 跨机师共享实体（战队/杯赛队伍/锦标赛/队伍）、"
          "`local_table` 本地表资源（BGM 包/图标）、`value_object` 值对象内的编号"
          "（赛程节点/留言）、`master_candidate` 有候选 cfg 表但键名不符、"
          "`notref` 名字以 id 结尾而非引用。", ""]
    if drefs:
        L += ["| 对象 | 字段 | 类别 | 依据 | 证据 VA |", "|---|---|---|---|---|"]
        for r in sorted(drefs, key=lambda r: (r["category"], r["object"], r["field"])):
            L.append(f"| `{r['object']}` | `{r['field']}` | `{r['category']}` | "
                     f"{r['basis']} | `{r['evidence_va']}` |")
    else:
        L.append("（无）")
    L += ["", "## 4. 生命周期 TBD 的字段", ""]
    tbd = [(oid, x) for oid, o in objects.items() for x in o["members"]
           if x["lifetime"] == "TBD"]
    if tbd:
        L += ["| 对象 | 字段 | 线类型 | 线视图 |", "|---|---|---|---|"]
        for oid, x in tbd:
            L.append(f"| `{oid}` | `{x['name']}` | `{x['wire_type']}` | "
                     f"{', '.join(x['views'])} |")
    else:
        L.append("（无）")
    L += ["", "## 5. 对象边界待人工拍板", "",
          "折叠链把以下对象合成了一个业务对象；若业务上应拆分，请在此登记。", "",
          "| 对象 | 折入的线布局 | 线长 | 锚点 |", "|---|---|---|---|"]
    for oid, o in sorted(objects.items()):
        if len(o["folded_composites"]) > 1:
            L.append(f"| `{oid}` | {', '.join(o['folded_composites'])} | "
                     f"{', '.join(str(v['length']) for v in o.get('views', []))} | "
                     f"`{o['anchored_by'] or '-'}` |")
    L += ["", "## 6. 同名成员跨线形宽度差异（已定宽，非未决）", "",
          "同一业务字段在不同 `wire_form` 里编码宽度可以不同。DDL 的列宽跟**落库线体**"
          "（`wire_body`，见 docs/05 §4.F）走，其余线形的宽度记在下面——"
          "**列宽必须装得下每一条线形**，所以这是核对清单而不是未决项："
          "若某行的宽度大于列宽，`_survey_homing.py` 的「列宽装得下每条线形」不变量会报红。", ""]
    variants = [(oid, x) for oid, o in objects.items() for x in o["members"]
                if x.get("wire_variants")]
    if variants:
        L += ["| 对象 | 字段 | 落库线体 | 列宽（已定） | 其它线形 |", "|---|---|---|---|---|"]
        for oid, x in sorted(variants, key=lambda kv: (kv[0], kv[1]["name"])):
            others = ", ".join(
                f"`{vid}` {v.get('wire_type') or '?'}"
                f"({v.get('length')}B)"
                for vid, v in sorted(x["wire_variants"].items()))
            o = objects[oid]
            L.append(f"| `{oid}` | `{x['name']}` | `{o.get('wire_body') or '-'}` | "
                     f"{x.get('wire_type')}（{x.get('length')}B） | {others} |")
    else:
        L.append("（无）")
    L += ["", "## 7. 值对象（无独立行键，由父行定位）", "",
          "以下对象没有自己的行键、也没有作用域列——它们是嵌在别的对象里的值对象，"
          "**不单独建表**，列内联到父表。", ""]
    vals = sorted(oid for oid, o in objects.items() if not o.get("is_root"))
    if vals:
        L += ["| 对象 | 成员数 | 出处线布局 |", "|---|---|---|"]
        for oid in vals:
            o = objects[oid]
            L.append(f"| `{oid}` | {len(o['members'])} | "
                     f"{', '.join(o['folded_composites'])} |")
    else:
        L.append("（无）")
    L += ["", "## 8. 同形线布局（折叠候选）", "",
          "逐字节同形（线长 + 成员名序列完全一致）却分属不同对象的复合体。"
          "引擎不擅自合并（`layout_same_as` 只说明布局相同、不说明是同一业务对象；"
          "P2 复核批次 `batch_02_fold` 的裁决是保守不折叠），请人工判定，"
          "裁决写进 `_overrides.json.twin_verdicts`（`fold` / `keep` + 理由），"
          "守卫 18 会校验裁决与引擎状态一致。", ""]
    twins = metrics.get("twins") or []
    ov_tv = {str(k): v for k, v in (load_overrides().get("twin_verdicts") or {}).items()
             if not str(k).startswith("_") and isinstance(v, dict)}
    L += [f"### 8.1 未裁决（{len(twins)} 组）", ""]
    if twins:
        L += ["| 同形组 | 线长 | 成员数 |", "|---|---|---|"]
        for grp in twins:
            c0 = next((load(SCHEMA / "composites" / f"{c}.json") for c in grp), {})
            L.append(f"| {', '.join('`' + c + '`' for c in grp)} | "
                     f"{c0.get('length')} | {len(c0.get('members') or [])} |")
    else:
        L.append("（无）")
    kept = {k: v for k, v in ov_tv.items() if str(v.get("verdict")) == "keep"}
    folded = {k: v for k, v in ov_tv.items() if str(v.get("verdict")) == "fold"}
    L += ["", f"### 8.2 已裁决·不折（{len(kept)} 组）", "",
          "同形只说明元素字段相同；下面每组都有「折了会丢行/丢列/改行主」或"
          "「都不建表、折叠不改 DDL」的具体理由。", "",
          "| 同形组 | 裁决 | 理由 |", "|---|---|---|"]
    if kept:
        for k, v in kept.items():
            L.append(f"| {', '.join('`' + c + '`' for c in k.split('+'))} | keep | "
                     f"{v.get('reason')} |")
    else:
        L.append("| （无） | | |")
    L += ["", f"### 8.3 已裁决·折叠（{len(folded)} 组）", "",
          "折成一个对象（表只留一张，另一张在 `retire_tables` 登记退场）。", "",
          "| 同形组 | 折成 | 理由 |", "|---|---|---|"]
    if folded:
        for k, v in folded.items():
            L.append(f"| {', '.join('`' + c + '`' for c in k.split('+'))} | "
                     f"`{v.get('as')}` | {v.get('reason')} |")
    else:
        L.append("| （无） | | |")
    L += ["", "## 9. 有定位但无地址级 VA 的成员", "",
          "这些成员有 `命令 + 子程序 + README 章节` 但没记到地址级 `evidence_va`。"
          "证据在，不阻塞归位，但**不满足 §8「指回 VA」的严格口径**——"
          "要么补 VA（走 IDA 批次），要么接受按 `evidence_ref` 追溯。", ""]
    no_va = [(oid, x) for oid, o in sorted(objects.items()) for x in o["members"]
             if not x.get("evidence_va") and x.get("evidence_ref")]
    grouped: dict[str, int] = collections.Counter(o for o, _ in no_va)
    if no_va:
        L += ["| 对象 | 无 VA 成员数 | 示例字段 |", "|---|---|---|"]
        for oid, cnt in sorted(grouped.items(), key=lambda kv: -kv[1]):
            fields = [x["name"] for o, x in no_va if o == oid][:4]
            L.append(f"| `{oid}` | {cnt} | {', '.join('`' + f + '`' for f in fields)} |")
    else:
        L.append("（无）")
    L.append("")
    (HOMING / "unresolved.md").write_text("\n".join(L), encoding="utf-8")


# ------------------------------------------------------- 报告


def report(m: Model, objects: dict[str, dict], relations: list[dict],
           dangling: list[dict], cov: dict, metrics: dict,
           master: list[dict] | None = None,
           runtime: list[dict] | None = None) -> None:
    master = master or []
    runtime = runtime or []
    n_mem = sum(len(o["members"]) for o in objects.values())
    print(f"命令        : {len(m.commands)}")
    print(f"复合体      : {len(m.composites)}  → 折入 {cov['composites_folded']}"
          f"（缺 {len(cov['composites_missing'])}）")
    print(f"实体        : {len(m.entities)}")
    print(f"对象(L2)    : {len(objects)}"
          f"（根 {cov['objects_root']} / 值 {cov['objects_value']}）")
    print(f"字段(L3)    : {n_mem}")
    roles = collections.Counter(x["role"] for o in objects.values()
                                for x in o["members"])
    print("角色分布    : " + ", ".join(f"{k}={v}" for k, v in roles.most_common()))
    life = collections.Counter(x["lifetime"] for o in objects.values()
                               for x in o["members"])
    print("生命周期    : " + ", ".join(f"{k}={v}" for k, v in life.most_common()))
    rel_live, wire_refs = split_relations(objects, relations)
    print(f"关联(FK)    : {len(rel_live)}（悬空/歧义 {len(dangling)}）"
          "——只含源对象建表的边")
    print(f"线上引用    : {len(wire_refs)}（源对象不建表：DERIVED/EVENT/CONFIG/TBD，"
          "见 relations.json.wire_refs）")
    print(f"主数据引用  : {len(master)}（cfg.*/srv.* 静态配置，非 game.* 外键）")
    print(f"战斗期句柄  : {len(runtime)}（本场内存实体，不落库）")
    print(f"模型外引用  : {len(explained_refs(objects)[2])}"
          "（人工归类：世界级实体/本地表资源/值对象/候选主数据，保留普通列）")
    print(f"根对象无 PK : {len(cov['roots_without_pk'])} 仍未决"
          f"（已裁决定性：单行 {len(cov.get('roots_singleton') or [])}"
          f" + 暂无写入方 {len(cov.get('roots_no_writer') or [])}；"
          f"PERSIST 根 {cov.get('roots_persist')}，"
          f"EVENT/TBD 根 {cov.get('roots_event_or_tbd')} 不建表）")
    print(f"非 PERSIST 幻影表 : {len(cov.get('non_persist_tables') or [])}（必须为 0）")
    print(f"无 VA 成员  : {cov['members_without_va']}"
          f"（其中完全无出处 {cov['members_without_any_evidence']}）")
    if metrics.get("twins"):
        print(f"同形未折叠  : {len(metrics['twins'])} 组"
              f"（已裁决 {metrics.get('twins_reviewed')} 组：`_overrides.json.twin_verdicts`）")
    if cov["composites_missing"]:
        print("未折入      : " + ", ".join(cov["composites_missing"][:20]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="落 schema/homing/")
    ap.add_argument("--report", action="store_true", help="只统计")
    args = ap.parse_args()

    m = Model()
    objects, unresolved, metrics = build(m)
    relations, dangling, master, runtime, cat_refs = resolve_relations(objects)
    cov = coverage(objects)
    report(m, objects, relations, dangling, cov, metrics, master, runtime)
    if args.write:
        emit(objects, relations, dangling, metrics, unresolved, master, runtime)
        print(f"\n已写入 {HOMING}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
