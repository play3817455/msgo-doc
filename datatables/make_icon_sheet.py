# -*- coding: utf-8 -*-
"""make_icon_sheet.py —— 把 interface/icon/battle/b/b<C>...dds 拼成带标签的联系表（供看图识机）。

图标命名：`b` + <C 4位> + <??2位> + <??2位>.dds —— 与资源目录的 C 号对应。
用法：python datatables/make_icon_sheet.py <输出png> <C号...>
      例：python datatables/make_icon_sheet.py _sheet.png 0101 0202 2840 2850
"""
import glob
import io
import os
import re
import sys

from PIL import Image, ImageDraw

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON = os.path.join(ROOT, 'unpackdat', 'interface', 'icon', 'battle', 'b')


def main():
    out = os.path.abspath(sys.argv[1])
    cs = sys.argv[2:]
    allf = sorted(os.listdir(ICON)) if os.path.isdir(ICON) else []
    print('battle/b 图标共 %d 个' % len(allf))
    tiles = []
    for c in cs:
        fs = [f for f in allf if re.match(r'^b' + c + r'\d+\.dds$', f)]
        print('  C=%s → %d 个图标：%s' % (c, len(fs), fs[:5]))
        for f in fs[:4]:
            try:
                tiles.append((c, f, Image.open(os.path.join(ICON, f)).convert('RGBA')))
            except Exception as e:
                print('    跳过 %s（%s）' % (f, e))
    if not tiles:
        print('无可用图标')
        return 1
    tw = max(t[2].width for t in tiles)
    th = max(t[2].height for t in tiles) + 16
    cols = min(8, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGBA', (cols * tw, rows * th), (30, 30, 40, 255))
    d = ImageDraw.Draw(sheet)
    for i, (c, f, im) in enumerate(tiles):
        x, y = (i % cols) * tw, (i // cols) * th
        sheet.paste(im, (x, y), im)
        d.text((x + 2, y + im.height + 2), '%s %s' % (c, f[1:5]), fill=(255, 255, 0, 255))
    sheet.save(out)
    print('已写 %s  （%dx%d，%d 块）' % (out, sheet.width, sheet.height, len(tiles)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
