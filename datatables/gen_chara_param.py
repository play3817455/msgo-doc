# -*- coding: utf-8 -*-
"""
gen_chara_param.py —— 生成 `msma/msma_settings.csv`（CHARA_PARAM，表ID 4，下载序 4）的**内容**。

产出：`server/datafiles/msma_msma_settings.csv`

★ 本表是**机体参数主表**（64 个读取列 / CSV 位置 0..91）。本次只填**能确证的两列**：
    col0 = 模型ID（= 練度ID，主键）
    col5 = 名称（str）← `unpackdat/settings/favms_ok_list.csv` 的**日文原名**（真实、可追溯）
  其余列**留空（=0）**，原因见下「双阻塞」——不猜。

列语义（`sub_582390` + `datatables/01-列注释/04-4-CHARA_PARAM.md`；内存偏移见 topics/16 §2.2）：
  col0 u32 +0 模型ID ｜ col1/col2 i64 ｜ col3 u32 ｜ col4 enum RANK1..RANK5（`sub_580610`）
  col5 str +36 名称 ｜ col6 str +92 说明 ｜ col7/col8 enum ｜ col9..col34 多为 u32 数值
  col36/col37 float 系数 ｜ col48/col49 enum ｜ col56..col79 文本 ｜ col83/85/86/88/89/90/91 u32

⛔ 双阻塞（本次不填数值的原因，已写进 `04-填充日志.md`）：
  1. **列绑定未证实**：CHARA_PARAM 的 64 列 ↔ 语义（装甲/推进/载重/…）**没有静态证据链**——
     UI 文本不在 exe（在 `unpackdat/settings/str_table.txt`），也没有"属性ID → 行偏移"的中枢表
     （129 条 `MS_*` 属性枚举的值表 `dword_D7D15C` **只被转换函数自己引用**）。
  2. **数值无桥**：`unpackdat/codex/data/units.json`（699 台）的机体名是**中文**，机体名册是**日文**
     ⇒ 名称交集仅 **2/699**，`units.js` 也无日文名字段 ⇒ **无法把 codex 的 armor/speed/boost/payload
     落到正确的練度ID 上**。
  ⇒ 解锁路线见日志；本生成器**已把列与来源解耦**，解锁后只需在此登记映射并重跑。

用法：python gen_chara_param.py [--check]
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SETTINGS = os.path.join(ROOT, 'unpackdat', 'settings')
OUT = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_settings.csv')

COLS = 6                 # 写到 col5 为止
NAME_COL = 5             # col5 = 名称（str）


def load_ms_list():
    """机体名册：練度ID → 機体名（favms_ok_list.csv）。

    · 源文件有 2 行**缺分隔逗号** ⇒ 用"前导数字=ID，其余=名"兜底；
    · 源文件有 4 条**完全重复行** ⇒ 按唯一 ID 去重（700 行 → 696 个唯一 ID）。
    """
    path = os.path.join(SETTINGS, 'favms_ok_list.csv')
    out, seen = [], set()
    for line in open(path, encoding='utf-8', errors='replace').read().splitlines():
        line = line.lstrip('\ufeff')
        if not line.strip() or line.lstrip()[0] == '#':
            continue
        parts = line.split(',')
        if len(parts) >= 2 and parts[0].strip().isdigit():
            pair = (parts[0].strip(), parts[1].strip())
        else:
            head = ''
            for ch in line:
                if ch.isdigit():
                    head += ch
                else:
                    break
            if not head or head == line:
                continue
            pair = (head, line[len(head):].lstrip('.．・ '))
        if pair[0] in seen:
            continue
        seen.add(pair[0])
        out.append(pair)
    return out


def render(ms_list):
    head = [
        '#模型ID,,,,,名称,',
        '# ===== msma/msma_settings.csv （CHARA_PARAM / 表ID 4 / 下载序 4 / CCharaParamTable / 读取函数 sub_582390）=====',
        '# 本表 = ★机体参数主表★（HP/装甲/推进/载重…主数值），行键 = 模型ID（= 練度ID）。',
        '# 列语义（详见 datatables/01-列注释/04-4-CHARA_PARAM.md；内存偏移见 reverse-login-chain/formats/README §五）：',
        '#   col0  = 模型ID（主键）｜ col4 = 类别枚举 RANK1..RANK5 ｜ col5 = ★名称★（str）｜ col6 = 说明（str）',
        '#   col1/2=i64 ｜ col3/9..34 多为 u32 数值 ｜ col36/37=float 系数 ｜ col48/49=枚举 ｜ col56..79=文本 ｜ col83..91=u32',
        '# 本次填充（"有内容"层）：',
        '#   col0 ← 練度ID（unpackdat/settings/favms_ok_list.csv，696 个唯一 ID，与 msma_model / weapon_set 同源同序）',
        '#   col5 ← 機体名（同上，日文原名，真实值）',
        '#   ★其余列一律留空（= 0）：列↔语义绑定未证实 + codex 数值无桥 ⇒ 按项目铁律「不把推断伪装成结论」不猜。',
        '# ⛔ 阻塞与解锁路线见 datatables/04-填充日志.md（下载序 4 记录）。',
        '# 生成：python datatables/gen_chara_param.py（%d 行）' % len(ms_list),
    ]
    lines = list(head)
    for ms_id, name in ms_list:
        f = [''] * COLS
        f[0] = ms_id
        f[NAME_COL] = name.replace(',', '・')   # 不引入引号转义（解析器行为未验证）
        lines.append(','.join(f) + ',')
    return '\r\n'.join(lines) + '\r\n'


def self_check(text):
    b = text.encode('utf-8')
    ok = True
    if b.startswith(b'\xef\xbb\xbf'):
        print('!! 带 BOM'); ok = False
    if b.count(b'\n') != b.count(b'\r\n'):
        print('!! 存在非 CRLF 换行'); ok = False
    body = [x for x in text.split('\r\n') if x and not x.startswith('#')]
    if [x for x in body if not x.endswith(',')]:
        print('!! 数据行缺尾逗号'); ok = False
    if not body:
        print('!! 无数据行'); ok = False
    print('自检：BOM 无 ✓ / CRLF ✓ / UTF-8 ✓ / 尾逗号 ✓' if ok else '自检：失败 ✗')
    print('数据行 %d，注释行 %d' % (len(body), text.count('\r\n#') + 1))
    return ok


def main():
    ms = load_ms_list()
    text = render(ms)
    if '--check' in sys.argv:
        if os.path.exists(OUT):
            self_check(open(OUT, encoding='utf-8', newline='').read())
        else:
            print('目标文件不存在')
        return 0
    with open(OUT, 'wb') as f:
        f.write(text.encode('utf-8'))
    print('机体 %d 台 → 已写 %s' % (len(ms), OUT))
    self_check(text)
    for l in [x for x in text.split('\r\n') if x and not x.startswith('#')][:3]:
        print('   ' + l)
    return 0


if __name__ == '__main__':
    sys.exit(main())
