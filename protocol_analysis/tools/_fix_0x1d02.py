"""一次性修补：SC-0x1D02 pilots 元素 = pilot 复合体（159B / 24 成员）。

原记录把元素记成 38B / 7 成员：`sub_B06980` 只读到第 7 个成员就停手，并把打印器
`sub_B08AD0` 的其余成员判成「不在线上」。逐指令读完整函数后成员对位如下（写侧
`sub_B06360` 的 pilot 159B 写入器同序同偏移，互为对照）：

  0x00 u32 pilot_id | 0x04 char[25] name | 0x1D i8 troops | 0x1E i8 level
  0x1F i8 mil_class | 0x20 u16 byword | 0x24 u32 cmdr_fame | 0x28/0x2A/0x2C u16 三项胜率
  0x30 u32 level_point | 0x34 avatar 18B | 0x4C u32 clan_id | 0x50 char[31] clan_name
  0x6F/0x70/0x71 i8 徽章三项 | 0x74 u32 cupteam_id | 0x78 char[31] cupteam_name
  0x98/0x9C/0xA0/0xA4/0xA8 u32 accum_point/rank/base_accump/req_accump/penalty

合计线上 159B（内存跨度 0xAC，槽步进 0xB0=176）——与 db_design 的 `pilot` 复合体逐字吻合。
"""

import csv
import io
import pathlib

DIR = pathlib.Path(__file__).resolve().parents[1] / "commands" / "SC-0x1D02-lounge-channellobby_members_get_r"

HEADER = ["序号", "偏移", "长度", "线类型", "字段名", "含义", "用途", "取值或枚举", "证据VA", "置信度"]

ROWS = [
    ["0", "-", "2", "u16", "opcode", "命令号", "分发器 switch 选择子", "0x1D02", "0xB57660", "确证"],
    ["1", "0", "4", "u32", "is_simple", "是否简略模式",
     "经 `vt[0x148]`；日志 `is_simple=`", "-", "0xB57544|0xB576B6", "确证"],
    ["2", "4", "4", "u32", "world_client_num", "本大区在线客户端数",
     "经 `vt[0x148]`；日志 `world_client_num=`", "-", "0xB57581|0xB576E0", "确证"],
    ["3", "8", "4", "u32", "pilots_num", "成员条目数 N",
     "上限 `cmp ebx,800h`（2048）；驱动数组；经 `vt[0x148]`", "0..2048", "0xB57597|0xB575C0", "确证"],
    ["4", "12", "159", "array<pilot>", "pilots",
     "频道大厅成员列表（元素 = `pilot` 复合体 24 成员 / 线上 159B；缓冲槽步进 `0xB0`=176）",
     "数组基址经 `vt[0x148]`；日志 `pilots={…}`（打印器 `sub_B08AD0` 即 pilot 24 成员）",
     "元素线长 159 / 槽 176",
     "0xB575EF(元素读取器 sub_B06980 = pilot 读取器)|0xB575D2(sub_B41310 0xB0/槽)|0xB575FB(循环步进 0xB0)",
     "确证"],
]


def main() -> None:
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows([HEADER] + ROWS)
    path = DIR / "fields.csv"
    path.write_text("\ufeff" + buf.getvalue(), encoding="utf-8")
    print(path.read_text(encoding="utf-8-sig"))


if __name__ == "__main__":
    main()
