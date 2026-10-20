#!/usr/bin/env python3
"""`srch_res` 的 15 个线序占位成员改名为 `clan_search_hit` 的语义名。

判据：**两个复合体的读取器是同一个函数 `sub_B45BA0`**（两侧 json 的 `reader` 字段相同），
线长 114B、逐偏移逐类型完全一致，连 `oracle_fix.py` 逐出的内存对齐修正都逐条相同。
所以 `wNN_*` 只是「打印器没有名字时的线序占位」，真名就在同读取器的基座里。

为什么必须改：`_overrides.json.fold` 把 `srch_res` 折进 `clan_search_hit` 后，
`derive_homing` 按**成员名**做并集——占位名对不上真名，就会折出 15 个 `lifetime=TBD`
的幻影列（实测 30 成员）。改名后并集才是干净的 15 列。

本脚本只改名，不动 offset/length/wire_type/wire_sources/evidence_va（VA 是同一个读取器
里的指令地址，对两边都成立）。
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPS = ROOT / "schema" / "composites"

# offset → 语义名（取自 schema/composites/clan_search_hit.json，同偏移同名同型）
RENAME = {
    0: "clan_id",
    4: "emb_base",
    5: "emb_parts1",
    6: "emb_parts2",
    7: "clan_name",
    38: "level",
    39: "offer_body",
    70: "leader_name",
    95: "member_num",
    99: "member_max",
    103: "offer_is_active",
    104: "clan_kind",
    105: "active_time_bits",
    109: "play_style",
    110: "capture_unlock_num",
}

TITLE = "战队搜索元素 srch_res（= clan_search_hit，114B 线 / 120B 槽）"

NOTE = (
    "**本元素与 `clan_search_hit` 是同一个结构体**：读取器同为 `sub_B45BA0`"
    "（同一段代码解出来的就是同一种行），线长 114B、槽步进 120B（`sub_B417A0` 申请 "
    "`0x78`/槽，末尾 6B 行内填充），逐偏移逐类型一致 —— 4+1+1+1+31+1+31+25+4+4+1+1+4+1+4。"
    "差别只在协议字段名（本命令 `SC-0x7ED3-clan_search_sortfilter_get_r` 叫 `srch_res[]`，"
    "`SC-0xD467`/`SC-0xDA04` 叫 `search_res[]`：筛选/排序搜索 vs 关键词搜索，同一张结果表）"
    "与调用点是否传打印器（本命令不传，客户端只入库不外显）。"
    "成员名取自同读取器的基座 `clan_search_hit`（原先是 `wNN_类型` 占位）；两边的成员 "
    "`evidence_va` 是同一条读取器里的同一批指令地址，逐条相同。"
    "行身份/落库见 `homing/_overrides.json.fold`（折到 `clan_search_hit`，`game.srch_res` 不建）。"
)


def main() -> int:
    path = COMPS / "srch_res.json"
    comp = json.loads(path.read_text(encoding="utf-8"))

    hit = json.loads((COMPS / "clan_search_hit.json").read_text(encoding="utf-8"))
    by_off = {m.get("offset"): m for m in hit.get("members") or []}

    renamed = 0
    for m in comp.get("members") or []:
        off = m.get("offset")
        want = RENAME.get(off)
        if not want:
            raise SystemExit(f"srch_res: 偏移 {off} 没有改名映射，先对一遍基座")
        base = by_off.get(off)
        if base is None:
            raise SystemExit(f"srch_res: 基座 clan_search_hit 没有偏移 {off} 的成员")
        for k in ("length", "wire_type"):
            if m.get(k) != base.get(k):
                raise SystemExit(
                    f"srch_res@{off}: {k} 不一致（{m.get(k)!r} vs {base.get(k)!r}）——不是同线形，停")
        if m["name"] != want:
            old = m["name"]
            m["name"] = want
            m["meaning"] = f"同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 {old}"
            for ws in m.get("wire_sources") or []:
                if ws.get("field_name") == old:
                    ws["field_name"] = want
            renamed += 1
        m["disposition"] = "PERSIST"

    comp["title"] = TITLE
    comp.setdefault("evidence", {})["note"] = NOTE
    path.write_text(json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"srch_res: 改名 {renamed} 条成员，disposition → PERSIST（TBD 清零）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
