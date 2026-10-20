# -*- coding: utf-8 -*-
"""make_unit_icon_sheet.py —— 按**模型坐标**取机体图标，拼成带标签联系表（供看图识机）。

★图标的键 = モデルID（10 位 = kind0 + A1 + B2 + C4 + NN2），与资源目录一一对应：
    interface/icon/item/d/d0<A><BB><CCCC><NN>.dds   （大图）
    interface/icon/item/s/s0<A><BB><CCCC><NN>.dds   （小图）
  ⇒ **每个 chara 目录都能取到它自己的图标**，看图即可判"这个目录是哪台机体"（无需读模型）。

用法：
  python datatables/make_unit_icon_sheet.py out.png 01/01/0202 01/01/2850 ...   # 目录
  python datatables/make_unit_icon_sheet.py out.png --series 0101               # 某系列全部未配目录
  python datatables/make_unit_icon_sheet.py out.png --series 0101 --all         # 含已配（标签带*）
选项：
  --size s|d      小图/大图（默认 d）
  --cols N        每行块数（默认 10）
  --scale N       放大倍数（默认 3）
"""
import glob
import io
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ICON = os.path.join(ROOT, 'unpackdat', 'interface', 'icon', 'item')


def read(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8-sig', 'cp932', 'utf-8', 'latin1'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode('latin1')


def rows(p):
    return [[f.strip() for f in l.rstrip(',').split(',')]
            for l in read(p).replace('\r\n', '\n').split('\n')
            if l.strip() and not l.lstrip().startswith('#')]


def used_dirs():
    used = {}
    for fn, tag in (('模型号映射-合并.csv', 'join'), ('模型号映射-补充.csv', '补充'), ('模型号映射-人工.csv', '人工')):
        p = os.path.join(HERE, 'names', fn)
        if not os.path.exists(p):
            continue
        for f in rows(p):
            if len(f) > 1 and re.fullmatch(r'\d{7}', f[0] or '') and re.fullmatch(r'\d{9}', f[1] or ''):
                v = int(f[1])
                used[(v // 10**8, (v // 10**6) % 100, (v // 100) % 10000)] = (f[0], f[2] if len(f) > 2 else '', tag)
    return used


def icon_path(pre, a, b, c, nn=1):
    return os.path.join(ICON, pre, '%s0%1d%02d%04d%02d.dds' % (pre, a, b, c, nn))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    out = os.path.abspath(args[0])
    rest = args[1:]
    pre = 's' if '--size' in rest and rest[rest.index('--size') + 1] == 's' else 'd'
    cols = int(rest[rest.index('--cols') + 1]) if '--cols' in rest else 10
    scale = int(rest[rest.index('--scale') + 1]) if '--scale' in rest else 3
    show_all = '--all' in rest
    used = used_dirs()

    items = []
    if '--map' in rest:
        # 校验收口模式：读 mapping csv（練度ID,モデルID,机体名,代号,资源目录,来源）逐条出图
        mp = rest[rest.index('--map') + 1]
        for f in rows(os.path.join(HERE, mp)):
            if len(f) > 2 and re.fullmatch(r'\d{9}', f[1] or ''):
                v = int(f[1])
                items.append((v // 10**8, (v // 10**6) % 100, (v // 100) % 10000, f[2]))
    elif '--series' in rest:
        s = rest[rest.index('--series') + 1]
        for f in rows(os.path.join(HERE, 'names', 'chara模型代号.csv')):
            if len(f) < 5:
                continue
            a, b, c = int(f[0]), int(f[1]), int(f[2])
            if '%02d%02d' % (a, b) != s:
                continue
            if not show_all and (a, b, c) in used:
                continue
            items.append((a, b, c, f[3]))
    else:
        for d in [x for x in rest if not x.startswith('--')]:
            m = re.match(r'^(?:chara/)?(\d+)/(\d+)/(\d+)$', d)
            if m:
                a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
                items.append((a, b, c, ''))

    tiles = []
    i0 = int(rest[rest.index('--from') + 1]) if '--from' in rest else 0
    n_lim = int(rest[rest.index('--count') + 1]) if '--count' in rest else 10 ** 9
    items = items[i0:i0 + n_lim]
    for a, b, c, code in items:
        p = icon_path(pre, a, b, c)
        tag = '%02d%02d%04d' % (a, b, c)
        if not os.path.exists(p):
            tiles.append((tag, code, None, False))
            continue
        try:
            im = Image.open(p).convert('RGBA')
            tiles.append((tag, code, im, (a, b, c) in used))
        except Exception as e:
            print('  跳过 %s (%s)' % (tag, e))
            tiles.append((tag, code, None, False))

    ok = [t for t in tiles if t[2] is not None]
    if not ok:
        print('无可用图标（%d 条缺失）' % len(tiles))
        return 1
    cw = max(t[2].width for t in ok) * scale
    lab = 56
    ch = max(t[2].height for t in ok) * scale + lab
    rows_n = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGBA', (cols * cw, rows_n * ch), (25, 25, 35, 255))
    dr = ImageDraw.Draw(sheet)

    def fnt(px):
        for fp in ('C:/Windows/Fonts/msyhbd.ttc', 'C:/Windows/Fonts/msyh.ttc',
                   'C:/Windows/Fonts/msgothic.ttc', 'C:/Windows/Fonts/arialbd.ttf'):
            try:
                return ImageFont.truetype(fp, px)
            except Exception:
                continue
        return ImageFont.load_default()

    big_f, small_f = fnt(38), fnt(19)
    for i, (tag, code, im, done) in enumerate(tiles):
        x, y = (i % cols) * cw, (i // cols) * ch
        if im is not None:
            big = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
            sheet.paste(big, (x, y), big)
        else:
            dr.rectangle([x, y, x + cw - 2, y + ch - lab], fill=(80, 20, 20, 255))
        dr.rectangle([x, y + ch - lab, x + cw - 2, y + ch - 1], fill=(0, 0, 0, 255))
        dr.text((x + 4, y + ch - lab + 4), '#%d' % i, fill=(255, 60, 60, 255), font=big_f)
        dr.text((x + 78, y + ch - lab + 6), tag + ('*' if done else ''),
                fill=(120, 255, 120, 255), font=small_f)
        dr.text((x + 78, y + ch - lab + 32), (code or '')[:18], fill=(255, 230, 60, 255), font=small_f)
    sheet.convert('RGB').save(out)
    for i, (tag, code, im, done) in enumerate(tiles):
        print('  #%-2d %s%s  %s' % (i, tag, '*' if done else '', (code or '')[:40]))
    print('已写 %s （%d 块，%s，x%d）' % (out, len(tiles), pre, scale))
    return 0


if __name__ == '__main__':
    sys.exit(main())
