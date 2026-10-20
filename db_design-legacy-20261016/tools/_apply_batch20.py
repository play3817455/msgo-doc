#!/usr/bin/env python3
"""批 20：两条「欠账」的收口。

欠账① `mshipbid_card` 缺上下文列 —— **现在有证据了，落地**：
  * 行的主语是**母舰战队（氏族）**，不是读方机师：
    - `CS-0x2A35-clan_mshipbid_response(pilot_id_applicant, is_ok, clan_kind)` 只带**申请者**，
      氏族由会话解析 —— 若行按读方机师分片，申请人（非族长）写下的那行，族长读列表时根本看不到，
      功能不成立；
    - `CS-0xCC9F-clan_mshipbid_request(clan_id, clan_kind)` 的 `clan_id` 是**入参**（`arg_0`，
      0xB9FD99）：客户端自己知道自身 clan_id，能当入参传出去的只能是**目标**氏族；
    - `SC-0xE69C-clan_mshipbid_request_r` 回 `mclan_id`/`mclan_name`（母舰战队 id/名）——
      把请求的目标氏族回显给客户端显示（若 `clan_id` 是自身氏族，回显自身名字没有意义）。
  ⇒ `scope=["world_id"]`（同 clan/cupteam/party），注入 `mclan_id` 进行键。
  * **原判「缺 `clan_id`/`ms_id`」半错**：`ms_id` 在整个入札族（4 CS + 4 SC）里**不存在**；
    被竞标的「母舰」是按**氏族 id**（`mclan_id`）标识的，不是 MS id。113B 卡里那个 `clan_id`
    是**申请人自己的**氏族，不能当行键。

欠账② `friend_histories` 的服务端写方 —— **订正来源，仍不落写方**（记进 reviewed）。

用法：python tools\\_apply_batch20.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
OV_PATH = TOOLS.parent / "schema" / "homing" / "_overrides.json"


def main() -> int:
    ov = json.loads(OV_PATH.read_text(encoding="utf-8"))

    # ---------------------------------------------------------------- ① mshipbid_card
    ov.setdefault("scope", {})["mshipbid_card"] = ["world_id"]

    ov.setdefault("inject_members", {})["mshipbid_card.mclan_id"] = {
        "wire_type": "u32",
        "meaning": "母舰战队 ID（入札列表归属的氏族；元素自身不带，写方在报文里点名）",
        "role": "ref",
        "fk_target": "clan.clan_id",
        "key": True,
        "evidence_va": "0xB9FD99",
        "basis": (
            "`SC-0xDB3F-clan_mshipbid_get_list_r` 的 `lpcard[]` 是**入札申请者卡列表**（113B，≤20），"
            "元素里只有申请者自己的身份（`pilot_id` + 他自己的 `clan_id`），没有「这份列表属于哪个氏族」。"
            "归属氏族的证据在写侧与配对命令上："
            "① `CS-0xCC9F-clan_mshipbid_request(clan_id, clan_kind)` —— `clan_id` 是**入参**"
            "（`arg_0`，写线 `0xB9FD99`；两个包装 `sub_63BC00`/`sub_696E00` 分别传 `clan_kind`=0/1，"
            "即「向这个氏族申请入札」）；"
            "② `SC-0xE69C-clan_mshipbid_request_r` 回 `mclan_id`+`mclan_name`（母舰战队 id/名），"
            "把请求目标回显给客户端显示；"
            "③ `CS-0x2A35-clan_mshipbid_response(pilot_id_applicant, is_ok)` 只带**申请者**、氏族由会话解析"
            "⇒ 行必须挂在氏族上：按读方机师分片的话，申请人写下的行族长看不见。"
            "不注入这一列，`(world_id, pilot_id=读方, mshipbid_card_pilot_id)` 会把**每个读方**的一份列表"
            "各存一套，且申请人与族长写的不是同一批行（同批 113B 族的行主问题，见 docs/05 §9.9.3）。"
        ),
    }

    ov.setdefault("writers", {})["mshipbid_card"] = {
        "commands": [
            "CS-0xCC9F-lounge-clan_mshipbid_request",
            "CS-0x2A35-lounge-clan_mshipbid_response",
            "CS-0x817C-lounge-clan_mshipbid_request_cancel",
        ],
        "evidence_va": "0xB9FD99 / 0x00EEC7EC / 0xEEC088",
        "reason": (
            "入札列表的写方都不带 113B 卡片结构（引擎「线体里带了这个复合体」的口径认不出来）："
            "`clan_mshipbid_request` 带 `clan_id`（目标氏族）+`clan_kind` ⇒ 建「我在该氏族的申请」那一行；"
            "`clan_mshipbid_response` 带 `pilot_id_applicant`+`is_ok` ⇒ 族长对某申请者行做保留/删除；"
            "`clan_mshipbid_request_cancel` 带 `clan_kind` ⇒ 申请人撤回自己那行（申请者由会话定）。"
            "行键 `(world_id, mclan_id, mshipbid_card_pilot_id)` 三列就位后，三条写方各自能定位单行。"
        ),
    }

    ov.setdefault("ref_stem", {})  # `mclan` 词干**不写**：见下方 reviewed 说明

    # ---------------------------------------------------------------- reviewed 记账
    ov.setdefault("reviewed", {})["batch_20_mshipbid"] = {
        "what": "mshipbid_card 的行主 = 入札列表归属的氏族（不是读方机师）：scope→[world_id]、注入 mclan_id 行键、点名三条 CS 写方",
        "why": (
            "batch_18 把它恢复成 PERSIST 时记的欠账是「缺 clan_id/ms_id」，"
            "本轮 IDA 取证把它改对了：**ms_id 不存在**（入札族里没有任何 MS id 字段），"
            "归属是**氏族 id**，且这个 id 在写侧报文里有（`CS-0xCC9F.clan_id` @0xB9FD99），"
            "不是「缺列」而是「行主判错了」——所以这次不是补一列凑合，而是把行主从读方改成氏族。"
            "**`ref_stem.mclan` 不写**：注入的成员在 `injected_members` 里已带 `fk_target`"
            "（`clan.clan_id`），词干裁决只作用于**线上已有的成员**，写 `mclan` 词干没有任何字段命中"
            "——`review_homing.py --verify` 会报「已过期」，属噪声。"
            "**`pk` 段必须同步改**：`pk` 订正一旦存在就整体替换 `pk_members`，"
            "注入列 `key: true` 的追加会被盖掉（`mshipbid_card` 的 `pk` 从 `[pilot_id]` 改成"
            "`[mclan_id, pilot_id]`），否则 `mclan_id` 只当普通列、唯一索引仍是「每读方一套列表」。"
        ),
        "evidence": [
            "CS-0xCC9F-lounge-clan_mshipbid_request：clan_id(u32)/clan_kind(u8)，clan_id 写线 @0xB9FD99（入参 arg_0）",
            "CS-0xCC9F 包装链 sub_63BC00(clan_kind=0) / sub_696E00(clan_kind=1) → sub_B004E0(a1,a2) → sub_B9FD10",
            "CS-0x2A35-lounge-clan_mshipbid_response：pilot_id_applicant/is_ok/clan_kind（族长的决定，申请者点名）",
            "CS-0x817C-lounge-clan_mshipbid_request_cancel：clan_kind（申请人撤回）",
            "SC-0xE69C-lounge-clan_mshipbid_request_r：mclan_id/mclan_name（目标氏族回显）",
            "SC-0xDB3F-lounge-clan_mshipbid_get_list_r：lpcard[≤20]（申请者卡列表）",
        ],
    }

    ov["reviewed"]["batch_20_friend_histories"] = {
        "what": "friend_histories 的服务端写方：来源订正为「跨世界好友登记」，并补一条缺失行键（对端世界 id）；本轮不落写方",
        "why": (
            "batch_18 把写方记成「战斗结束记一笔」是**猜的**。本轮取证："
            "① 读侧 `CS-0xE2B9-friend_history_get_xworld` 是**零负载请求**（`0xB9AEC3` 无报文体字段），"
            "响应 `SC-0x9F94` 回 `friend_histories[≤100]` + `block_widlist[≤100]`（`0xB6E98C`/`0xB6EA01`）；"
            "② IDA 里**同一个界面**（`sub_8BB900`，`L08Main`）连发四个请求："
            "`sub_42D7D0`(→`friend_list_get_detail` 0xA8C0)、`sub_42D7F0`、`sub_42D800`"
            "(→0xAFFEA0→`friend_history_get_xworld`)、`sub_42D830` ⇒ 「好友列表」与「跨世界好友履历」"
            "是**同一份好友关系**的两个视图（同一屏、同一 113B 卡、都 ≤100 条）；"
            "③ 跨世界那一半要按**对端所在世界**过滤（`block_widlist` 是屏蔽世界列表；"
            "`SC-0xE969-friend_xworld_search_r` 给出的对端世界里叫 `connet_world_id`），"
            "而 113B 卡里没有世界列 ⇒ 真要按行落库，还缺一列「对端世界 id」（注入前须先定谁提供）。"
            "结论：**行集不来自本世界任何表**（对端机师行不在本库），故维持 PERSIST；"
            "写方是好友登记的跨世界分支（`CS-0xBA4E-friend_list_mail_accept` / `CS-0xA30C-friend_list_remove`"
            "的对端异世界分支），不是战斗结算 —— 落地前先解决缺失的 `connet_world_id` 行键。"
        ),
        "evidence": [
            "CS-0xE2B9-lounge-friend_history_get_xworld：零负载（仅 opcode，容量 0x2）",
            "SC-0x9F94-lounge-friend_history_get_xworld_r：friend_histories[≤100] + block_widlist[≤100]",
            "sub_8BB900（L08Main 界面构造）：sub_42D7D0 / sub_42D7F0 / sub_42D800 / sub_42D830 四请求同屏",
            "sub_42D7D0 → 0xAFFE30 → 0xB9A8C0 = send_friend_list_get_detail",
            "sub_42D800 → 0xAFFEA0 → 0xB9AE00 = send_friend_history_get_xworld",
            "SC-0xE969-lounge-friend_xworld_search_r：connet_world_id（对端所在世界）",
        ],
    }

    OV_PATH.write_text(json.dumps(ov, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {OV_PATH}")
    print("  scope.mshipbid_card          =", ov["scope"]["mshipbid_card"])
    print("  inject_members               =", [k for k in ov["inject_members"] if not k.startswith("_")])
    print("  writers                      =", [k for k in ov["writers"] if not k.startswith("_")])
    print("  ref_stem                     = （不加 mclan：见 reviewed.batch_20_mshipbid）")
    print("  reviewed                     =",
          [k for k in ov["reviewed"] if k.startswith("batch_20")])
    return 0


if __name__ == "__main__":
    sys.exit(main())
