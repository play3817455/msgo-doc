# -*- coding: utf-8 -*-
"""gen_weapon_pipeline.py —— 武器流水线（第一版：近接武器线）。

★三方对齐（见 重建进度.md §3）：
    unit 目录 → motionlist.csv 的 21xyy 组数（武器槽数）
              → attr/*.vra 的 mesh 名（武器外观：Saber_01/…）
              → wiki 同机体武器列表（名字 + 威力/射程… = #36 的 11 项）

★核心设计（由"ID = 实例"推出）：为**每台机体的每把武器各分配一个独立真实ID**
  （资源池里同一外观最多有 281 个可用 ID ⇒ 够分）⇒ 名字/数值互不冲突 ✓

本版范围：**近接（WRESTLE）武器**——因为本地 `settings/weapon_wrestle.csv` 提供了
  8 把武器的**真名**（ビームサーベル/ヒートホーク/…），可零猜测产出。

产出（全部追加/替换到 server/datafiles/lounge/）：
  msma/msma_weapon_set.csv   #1  col0=練度ID col2=武器ID col4=MAIN|EX col5=类别 col6=1 col28=CHINA
  item/item.csv              #65 col0=ID col2=名称 col4=WEAPON
  item/weapon_battle_detail.csv  #36 `属性名,键(武器ID字符串),值`
  item/weapon_settings.csv   #37 col0=武器ID col21=功能分类(52值) col32=属性

用法：python datatables/gen_weapon_pipeline.py            # 只出报告
      python datatables/gen_weapon_pipeline.py --apply    # 写入四张表（含备份 + 方言自检）
"""
import collections
import csv
import glob
import io
import os
import re
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UD = os.path.join(ROOT, 'unpackdat')
DF = os.path.join(ROOT, 'server', 'datafiles', 'lounge')
W = os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv')


def rows_of(p):
    """读制表（跳过 # 行），返回 list[list[str]]"""
    out = []
    for l in open(p, encoding='utf-8', errors='replace').read().replace('\r\n', '\n').split('\n'):
        if not l.strip() or l.lstrip().startswith('#'):
            continue
        out.append(l.rstrip(',').split(','))
    return out


def main():
    apply = '--apply' in sys.argv

    # ── ① 机体三表：練度ID → (モデルID→unit目录)，練度ID → wiki页
    rid2model = {}
    for f in rows_of(os.path.join(HERE, 'names', '模型号映射-人工.csv')):
        if len(f) > 2 and f[2].strip():
            rid2model[f[0].strip()] = f[2].strip()
    rid2page = {}
    for f in rows_of(os.path.join(HERE, 'names', '机体名对照表.csv')):
        if len(f) > 28 and f[28].strip():
            rid2page.setdefault(f[0].strip(), f[28].strip())
    print('① 練度ID→モデルID %d 条；練度ID→wiki页 %d 条；交集 %d 台'
          % (len(rid2model), len(rid2page), len(set(rid2model) & set(rid2page))))

    # ── ② 资源池：按"资源目录"收集可用真实ID（近接系 = item/01|02|08）
    pool = collections.defaultdict(list)
    for f in rows_of(os.path.join(HERE, 'names', '物品ID全集.csv')):
        if len(f) > 3 and f[3] and int(f[3]) > 0:
            cat = f[2].split('/')[1]                 # item/<类>/<号>
            pool[cat].append(f[0])
    melee_ids = sorted(set(pool.get('01', []) + pool.get('02', []) + pool.get('08', [])),
                       key=lambda x: (len(x), x))
    print('② 近接可用真实ID（item/01|02|08）: %d 个' % len(melee_ids))

    # ── ③ wiki 武器（位置访问：0页面 3武器名 6射击模式 8威力 11射程距离 15红锁）
    WK = collections.defaultdict(list)
    for row in csv.reader([l for l in open(W, encoding='utf-8-sig', errors='replace').read().splitlines()
                           if l.strip() and not l.startswith('#')]):
        if len(row) > 11:
            WK[row[0]].append(row)
    print('③ wiki 机体页 %d' % len(WK))

    # ── ④ 逐台机体：取 wiki 武器列表 + 资源真实槽数（motionlist 的 21xyy 组数）
    SKIP_ROW = re.compile(r'模式|技能|必杀|burst|Burst')
    want = []
    for rid, model in sorted(rid2model.items()):
        page = rid2page.get(rid)
        if not page:
            continue
        m = re.match(r'^(\d)(\d{2})(\d{4})(\d{2})$', model)      # モデルID：1|B(2)|C(4)|NN(2)
        if not m:
            continue
        unit = os.path.join(UD, 'chara', m.group(1).zfill(2), m.group(2), m.group(3))
        if not os.path.isdir(unit):
            continue
        # ① wiki 武器行（剔除"模式/技能"行）
        rows = [r for r in WK.get(page, []) if r[3].strip() and not SKIP_ROW.search(r[3])]
        if not rows:
            continue
        # ② 资源侧真实槽数：motionlist 的 21xyy 分组数
        slots = 0
        ml = os.path.join(unit, 'motionlist.csv')
        if os.path.exists(ml):
            xs = set()
            for l in open(ml, encoding='utf-8', errors='replace'):
                f = l.strip().split(',')
                if f and f[0].isdigit() and 21000 <= int(f[0]) < 22000:
                    xs.add((int(f[0]) // 100) % 10)
            slots = len(xs)
        # ③ 资源侧外观件名（旁证）
        parts = []
        for p in glob.glob(os.path.join(unit, 'attr', '*.vra')):
            t = open(p, encoding='utf-8', errors='replace').read()
            parts += re.findall(r'\(name string[^"]*"([^"]+)"', t)
        want.append((rid, page, model, slots, rows, parts))

    print('④ 可分配武器的机体 **%d 台**（均有 wiki 武器列表）' % len(want))
    print('   （资源槽数 vs wiki 武器行数）样例：')
    for rid, page, model, slots, rows, parts in want[:10]:
        print('   %-9s %-20s 槽=%-3d wiki=%-3d  %s'
              % (rid, page[:20], slots, len(rows), [r[3][:16] for r in rows[:3]]))

    # ── ⑤ 分配：按 wiki 武器列表**逐把**分配独立真实ID（多槽）
    if not apply:
        print('（未写表；加 --apply 生效）')
        return 0
    # 武器类别（#1 col5，28 值）与功能分类（#37 col21，52 值）的判定
    def kind(name):
        n = name.lower()
        if re.search(r'saber|blade|sword|naginata|hammer|whip|军刀|剑|ナギナタ|鞭|锤', n):
            return 'WRESTLE', 'WRESTLE', 'MELEE'
        if re.search(r'shield|盾', n):
            return 'SHIELD', 'SHIELD', 'SHIELD'
        if re.search(r'machinegun|gatling|機関銃|机枪|机关炮|vulcan|バルカン', n):
            return 'MACHINEGUN', 'MACHINEGUN', 'GUN'
        if re.search(r'shotgun|散弾|霰弹', n):
            return 'SHOTGUN', 'SHOTGUN', 'GUN'
        if re.search(r'sniper|狙', n):
            return 'SNIPER_RIFLE', 'SNIPE', 'GUN'
        if re.search(r'missile|ミサイル|导弹|誘導弾', n):
            return 'MISSILE', 'MISSILE', 'GUN'
        if re.search(r'bazooka|バズーカ|火箭|榴弾砲', n):
            return 'BAZOOKA', 'BAZOOKA', 'GUN'
        if re.search(r'grenade|手榴弾|グレネード|投擲|ばくだん', n):
            return 'HAND_THROW', 'HAND_THROW', 'GUN'
        if re.search(r'mortar|迫撃', n):
            return 'TRENCH_MORTAR', 'TRENCH_MORTAR', 'GUN'
        return 'BEAM_RIFLE', 'BEAM', 'GUN'
    MODE2TRAJ = [('自动', 'GUN_RAPID'), ('三点', 'GUN_RAPID'), ('二点', 'GUN_RAPID'),
                 ('单发', 'GUN_SINGLE'), ('蓄力', 'GUN_SINGLE'), ('照射', 'GUN_RAPID'),
                 ('投掷', 'HAND_THROW'), ('开镜', 'SNIPE_BEAM')]
    NUMCOL = [(8, 'POWER'), (11, 'RANGE'), (9, 'STABILITY'), (10, 'RAPIDDELAY'),
              (13, 'RELOAD'), (14, 'LOCKON_CAM'), (15, 'HIGH_LOCKON')]
    it = iter(sorted(set(sum(pool.values(), [])), key=lambda x: (len(x), x)))
    rows1, rows65, rows36, rows37 = [], [], [], []
    nweap = 0
    for rid, page, model, slots, rows, parts in want:
        for i, r in enumerate(rows):
            try:
                wid = next(it)
            except StopIteration:
                print('!! ID 池用尽'); break
            name = r[3].strip()
            k5, k21, _ = kind(name)
            beam = re.search(r'ビーム|光束|beam|メガ|粒子', name, re.I) is not None
            traj = dict(MODE2TRAJ).get(r[6].strip(), 'NONE')
            if k21 == 'WRESTLE':
                traj = 'WRESTLE'
            if k21 == 'SHIELD':
                traj = 'SHIELD'
            rows1.append(','.join([rid, '', wid, '', 'MAIN' if i == 0 else 'EX', k5, '1']
                                  + [''] * 21 + ['CHINA']) + ',')
            rows65.append('%s,,%s,,WEAPON,' % (wid, name))
            for c, nm in NUMCOL:
                v = (r[c] if len(r) > c else '').strip()
                if v:
                    rows36.append('%s,%s,%s,' % (nm, wid, v))
            # col0=ID ｜ col1=0 ｜ col2=1（★P262：col2 门闩，0 ⇒ 装备组走活体分支崩）
            # col13=持握 ｜ col21=功能分类 ｜ col30=弹道 ｜ col32=属性
            grip = 'SHIELD' if k21 == 'SHIELD' else 'ONEHAND'
            rows37.append(','.join([
                wid, '0', '1'] + [''] * 10 + [grip] + [''] * 7 + [k21] + [''] * 8 + [traj] + ['']
                + ['BEAM' if beam else ('BLAST' if k21 == 'MISSILE' else 'SOLID')]) + ',')
            nweap += 1
    print('⑤ 分配：%d 台 × 武器 = **%d 把**（每把独立真实ID）' % (len(want), nweap))

    # ── ⑥ 落盘（保留注释头 + 追加，备份一次）
    def merge(path, newrows, keycols=1):
        """按前 keycols 列作键替换（长表 #36 用 keycols=2，避免误删同属性名的其它行）"""
        old = open(path, encoding='utf-8', errors='replace').read().replace('\r\n', '\n').split('\n') \
            if os.path.exists(path) else []
        head = [l for l in old if l.strip().startswith('#')]
        body = [l for l in old if l.strip() and not l.strip().startswith('#')]
        def key(l):
            return ','.join(l.split(',')[:keycols]).strip()
        # ★先删掉所有"将被写入的键"的旧行，再统一追加（同一键可有多行，不能被边加边删吃掉）
        newkeys = set(key(r) for r in newrows)
        body = [x for x in body if key(x) not in newkeys] + list(newrows)
        added = len(newrows)
        if not os.path.exists(path + '.bak'):
            shutil.copy2(path, path + '.bak')
        open(path, 'wb').write(('\r\n'.join(head + body) + '\r\n').encode('utf-8'))
        b = open(path, 'rb').read()
        ok = (not b.startswith(b'\xef\xbb\xbf')) and (b.replace(b'\r\n', b'').find(b'\n') < 0)
        print('   写 %-52s +%d 行 方言%s' % (os.path.relpath(path, ROOT), added, 'OK' if ok else 'FAIL'))
        return added

    print('⑤ 落盘：')
    merge(os.path.join(DF, 'msma', 'msma_weapon_set.csv'), rows1)
    merge(os.path.join(DF, 'item', 'item.csv'), rows65)
    merge(os.path.join(DF, 'item', 'weapon_battle_detail.csv'), rows36, 2)
    merge(os.path.join(DF, 'item', 'weapon_settings.csv'), rows37)
    print('★ 完成：%d 台机体各获得 1 把近接武器（独立真实ID + wiki 名 + 威力）' % len(rows1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
