# -*- coding: utf-8 -*-
"""
gen_chara_model.py —— 生成 `msma/msma_model.csv`（CHARA_MODEL，表ID 5，下载序 5）的**内容**。

产出：`server/datafiles/msma_msma_model.csv`

★ 本表 = ★机体模型与外观表★（模型/体型/外观资源 ID；主键 = u64 模型ID）。
  本次只填**能确证的键**：
    col0 = 模型ID（i64，= 練度ID）← `unpackdat/settings/favms_ok_list.csv`
  其余列留空（=0）。

  ★顺带修口径：既有文件只有 **698 行**（旧解析漏掉了名册里 2 行"缺逗号"的条目），本脚本统一为
    **696 个唯一 ID**（4 条完全重复行已去重），与 `msma_settings.csv` / `msma_weapon_set.csv` 完全对齐。

列语义（`sub_571380`；内存偏移见 reverse-login-chain/formats/README §五 与 topics/16 §2.3）：
  col0 i64 +0 模型ID ｜ col1..col5/col7..col9/col11/col15/col37/col42/col51/col53 = float
  col6/col12..col14 = bool ｜ col16..col31 = u32×16（2×8 循环，内存步长 8 交错）
  col26/27/28/30/48/49/50 = 枚举（`sub_402310`/`sub_571290`，文本类）｜ col54 = bool ｜ col55 = 枚举 ｜ 其余 u32

⛔ 为什么不填数值：CHARA_MODEL 的数值/枚举列**没有任何可回溯来源**——
  `unpackdat/chara/`（118230 个文件）是**模型/贴图/动画**资源（实测其 2118 个 CSV 全是
  摄像机、JOINT 骨架、motionlist 之类），不含机体参数；codex 的机体数值又有**中文名/日文名无桥**的问题
  （见 `04-填充日志.md` 下载序 4 记录）。⇒ 按项目铁律不猜。

用法：python gen_chara_model.py [--check]
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SETTINGS = os.path.join(ROOT, 'unpackdat', 'settings')
OUT = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_model.csv')


def load_ms_list():
    """机体名册：練度ID → 機体名（同 gen_chara_param.py：兜底 2 处缺逗号 + 去重 4 处重复）"""
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
        '#ID,',
        '# ===== msma/msma_model.csv （CHARA_MODEL / 表ID 5 / 下载序 5 / CCharaTable / 读取函数 sub_571380）=====',
        '# 本表 = ★机体模型与外观表★；主键 = 模型ID（u64，= 練度ID）。',
        '# 列语义（详见 datatables/01-列注释/05-5-CHARA_MODEL.md）：col0=i64 模型ID；col1..15 多为 float/bool；',
        '#   col16..31 = u32×16（2×8 循环，内存步长 8 交错）；col26/27/28/30/48/49/50 = 枚举；col54=bool；其余 u32。',
        '# 本次填充：col0 ← 練度ID（unpackdat/settings/favms_ok_list.csv，696 个唯一 ID）。',
        '#   ★其余列一律留空（=0）：chara/ 全是模型/贴图/动画资源（其 2118 个 CSV 为摄像机/骨架/motionlist），',
        '#     不含机体参数；codex 数值又有"中文名 ↔ 日文名无桥"问题 ⇒ 不猜（见 04-填充日志.md）。',
        '# 口径：696 行 = 名册 700 行去 4 条完全重复（旧文件 698 行 = 漏了 2 行"缺逗号"条目）。',
        '# 生成：python datatables/gen_chara_model.py（%d 行）' % len(ms_list),
    ]
    lines = list(head)
    for ms_id, _name in ms_list:
        lines.append(ms_id + ',')
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
    return 0


if __name__ == '__main__':
    sys.exit(main())
