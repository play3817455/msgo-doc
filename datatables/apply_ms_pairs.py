# -*- coding: utf-8 -*-
"""apply_ms_pairs.py —— 把 iconmatch 页面手工对照的导出，装配成「可下发给客户端」的数据。

一条链，四步；默认只走到「①分类校验」为止（dry-run），想动盘要显式 --apply/--ship：

  ① 分类校验    ms_wiki_pairs.json → 新增 / 一致 / 冲突 / 待定(lid 空) / 可疑
  ② 写名字层    names/模型号映射-页面.csv        ← 全量重写、可累加、来源=页面
  ③ 重建全集    names/练度ID-モデルID-全集.csv  （调 build_model_id_map.py）
  ④ 出下发表    server/datafiles/lounge/msma/*.csv（--ship 才做，调 gen_msma_machine.py）

★★为什么不在 datafiles 里手工加行★★
  那四张表（msma_model / msma_settings / msma_rental / msma_battle_detail）是 gen_msma_machine.py
  里**全量重写**的产物（读 names/ms_wiki_pairs.json + 客户端名册 favms_ok_list.csv 重建）。
  手工 append 的行下次一生成就没了 ⇒ 本脚本**从不**直接改 datafiles，累加只发生在 names/ 这一层。

★★冲突不自动改判★★
  練度ID 在表里已经有别的モデルID ⇒ 说明两边必有一边错，只报告、不写；
  要 --force 才写（写进去优先级最高，会盖掉 人工/合并/补充/自动 各表的旧值）。

★分批（按系列）
  --series 01    只处理 B 段 = 01 的系列（一族一族推，边界最清楚）
  --limit 20     先做 20 台（排序 = 系列 → 練度ID，结果稳定可复现）
  报告里永远打印「每个系列 已定/总数」，用来决定下一批做哪个系列。

★练度ID→モデルID 是 1:1，而 モデルID→練度ID 是 1:N
  （换装/形态、联邦-吉翁各占一个 モデルID 都会共用同一个 モデルID ⇒ 台台不同是正常的）

用法:
  python datatables/apply_ms_pairs.py                   # dry-run，只看报告
  python datatables/apply_ms_pairs.py --series 01       # 只看/只做 B 段 01
  python datatables/apply_ms_pairs.py --limit 20        # 先做 20 台
  python datatables/apply_ms_pairs.py --apply           # 落盘：写 页面.csv + 重建 全集.csv
  python datatables/apply_ms_pairs.py --apply --ship    # 再生成三张下发表（自动 .bak_truth 备份）
  python datatables/apply_ms_pairs.py --report 批次.md   # 报告另存一份
"""
import argparse
import io
import json
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAMES = os.path.join(HERE, "names")
PAGE_CSV = os.path.join(NAMES, "模型号映射-页面.csv")
FULL_CSV = os.path.join(NAMES, "练度ID-モデルID-全集.csv")
AUTH_CSV = os.path.join(NAMES, "chara目录-ID清单.csv")
CODES_CSV = os.path.join(NAMES, "chara模型代号-逐形态.csv")
LIDNAME_CSV = os.path.join(NAMES, "机体名对照表.csv")
SHIP_DIR = os.path.join(ROOT, "server", "datafiles", "lounge", "msma")
SHIP_FILES = ("msma_model.csv", "msma_settings.csv", "msma_rental.csv", "msma_battle_detail.csv")

# 页面上「导出 JSON」默认落到浏览器下载目录 ⇒ 常见位置都找一遍
PAIRS_GUESS = [
    os.path.join(ROOT, "iconmatch", "ms_wiki_pairs.json"),
    os.path.join(ROOT, "iconmatch", "data", "ms_wiki_pairs.json"),
    os.path.join(ROOT, "ms_wiki_pairs.json"),
    os.path.join(os.path.expanduser("~"), "Downloads", "ms_wiki_pairs.json"),
    os.path.join(os.path.expanduser("~"), "Desktop", "ms_wiki_pairs.json"),
]

# 现有各来源表（用来显示"这个練度ID 现在是谁认领的"）；mid 所在列见最后一列
PROV_TABLES = [
    ("人工", "模型号映射-人工.csv", 0, 2),
    ("合并", "模型号映射-合并.csv", 0, 1),
    ("补充", "模型号映射-补充.csv", 0, 1),
    ("自动", "模型号映射-自动.csv", 0, 1),
    ("初版", "模型号映射-初版.csv", 0, 2),
    ("机体总表", "机体总表.csv", 0, 33),
]

PAGE_HEAD = "#練度ID,モデルID,WIKI机体名,中文名,日文名,内部代号,资源目录,来源,"


# ── 小工具 ──
def rows(path):
    if not os.path.exists(path):
        return []
    L = io.open(path, encoding="utf-8-sig", errors="replace").read().splitlines()
    return [x for x in L if x.strip() and not x.lstrip().startswith("#")]


def cell(line, i):
    p = line.split(",")
    return p[i].strip() if i < len(p) else ""


def read_text(path):
    return io.open(path, encoding="utf-8-sig", errors="replace").read()


def write_crlf(path, lines):
    """落盘口径：UTF-8 无 BOM + CRLF（与 gen_msma_truth.py / fix_datafiles.py 一致）。"""
    io.open(path, "w", encoding="utf-8", newline="").write("\r\n".join(lines) + "\r\n")


def nrows(path):
    return len(rows(path))


def nbytes(path):
    return os.path.getsize(path) if os.path.exists(path) else 0


def is_mid(s):
    return len(s) == 9 and s.isdigit()


def is_lid(s):
    return len(s) == 7 and s.isdigit()


# ── 载入 ──
def find_pairs(cli):
    if cli:
        if not os.path.exists(cli):
            die("找不到 --pairs 指定的文件：%s" % cli)
        return cli
    for p in PAIRS_GUESS:
        if os.path.exists(p):
            return p
    die("找不到 ms_wiki_pairs.json。\n"
        "  先在页面 http://localhost:8777/ms_match.html 点「导出 JSON」，\n"
        "  或用 --pairs <路径> 指定（常见位置：\n    %s）" % "\n    ".join(PAIRS_GUESS))


def load_pairs(path):
    """→ (pairs, meta, items)；兼容页面「导出 JSON」与「导出 CSV」。"""
    if path.lower().endswith(".csv"):
        out = []
        for l in read_text(path).splitlines():
            if is_mid(cell(l, 0)):
                out.append({"mid": cell(l, 0), "wiki": cell(l, 3), "lid": cell(l, 4)})
        return out, {"exported": "(来自 CSV)"}, []
    try:
        d = json.loads(read_text(path))
    except Exception as e:
        die("JSON 解析失败：%s\n  %s" % (path, e))
    return d.get("pairs") or [], d.get("meta") or {}, d.get("items") or []


def load_auth():
    return set(cell(l, 0) for l in rows(AUTH_CSV) if is_mid(cell(l, 0)))


def load_code_dir():
    """モデルID → (内部代号, 资源目录)。"""
    out = {}
    for l in rows(CODES_CSV):
        mid = cell(l, 0)
        if is_mid(mid):
            out[mid] = (cell(l, 5), cell(l, 6))
    return out


def load_lid_names():
    """練度ID → {jp, cn, type, fac}（机体名对照表.csv：0=練度ID 1=日文名 2=中文名 6=类别 21=阵营）。"""
    out = {}
    for l in rows(LIDNAME_CSV):
        lid = cell(l, 0)
        if is_lid(lid):
            out[lid] = {"jp": cell(l, 1), "cn": cell(l, 2), "type": cell(l, 6), "fac": cell(l, 21)}
    return out


def load_current():
    """練度ID → モデルID（现在真正会下发的那份）。"""
    out = {}
    for l in rows(FULL_CSV):
        lid, mid = cell(l, 0), cell(l, 1)
        if is_lid(lid) and is_mid(mid):
            out[lid] = mid
    return out


def load_page_prev():
    """上次写进 页面.csv 的结论（累加用：本次导出只含最新一批，不能把旧结论冲掉）。"""
    out = {}
    for l in rows(PAGE_CSV):
        lid, mid = cell(l, 0), cell(l, 1)
        if is_lid(lid) and is_mid(mid):
            out[lid] = {"mid": mid, "wiki": cell(l, 2), "cn": cell(l, 3),
                        "jp": cell(l, 4), "code": cell(l, 5), "dir": cell(l, 6)}
    return out


def load_prov():
    """練度ID → [(来源标签, モデルID)]。"""
    out = {}
    for tag, fn, c_lid, c_mid in PROV_TABLES:
        for l in rows(os.path.join(NAMES, fn)):
            lid, mid = cell(l, c_lid), cell(l, c_mid)
            if is_lid(lid) and is_mid(mid):
                out.setdefault(lid, []).append((tag, mid))
    return out


# ── ①分类 ──
def classify(pairs, auth, cur, prev, series_want):
    """返回 (接受, 冲突, 待定, 可疑, 系列过滤掉的条数)。"""
    seen_lid_mid = {}       # lid → mid（本批内部查重）
    accept, conflict, todo, sus = [], [], [], []
    skipped_series = 0

    for p in pairs:
        mid = (p.get("mid") or "").strip()
        lid = (p.get("lid") or "").strip()
        wiki = (p.get("wiki") or "").strip()
        if not mid:
            continue
        if series_want and not in_series(mid, series_want):
            skipped_series += 1
            continue
        rec = {"mid": mid, "lid": lid, "wiki": wiki, "note": (p.get("note") or "").strip(),
               "code": p.get("code") or "", "dir": p.get("dir") or ""}

        if not lid:
            todo.append(dict(rec, why="練度ID 还没填" + ("（有名字：%s）" % wiki if wiki else "（名字也没填）")))
            continue
        if not is_lid(lid):
            sus.append(dict(rec, why="練度ID 不是 7 位数字"))
            continue
        if not is_mid(mid):
            sus.append(dict(rec, why="モデルID 不是 9 位数字"))
            continue
        if mid not in auth:
            sus.append(dict(rec, why="モデルID 不在权威树 chara目录-ID清单.csv 里（查不到资源目录）"))
            continue

        if lid in seen_lid_mid and seen_lid_mid[lid] != mid:
            conflict.append(dict(rec, why="同一批里 %s 被两行填成了 %s / %s" % (lid, seen_lid_mid[lid], mid),
                                 old=seen_lid_mid[lid], from_page=False))
            continue
        seen_lid_mid[lid] = mid

        old = prev.get(lid, {}).get("mid") or cur.get(lid)
        if old is None:
            accept.append(dict(rec, kind="new"))
        elif old == mid:
            accept.append(dict(rec, kind="same", old_from=("页面.csv" if lid in prev else "已有表")))
        else:
            if lid in prev:
                src = "上次写进 页面.csv"
            else:
                hits = ["%s:%s" % (t, m) for t, m in PROV_SRC.get(lid, []) if m == old]
                src = "、".join(hits) if hits else "已有映射表"
            conflict.append(dict(rec, old=old, src=src, from_page=lid in prev))

    return accept, conflict, todo, sus, skipped_series


def in_series(mid, want):
    """系列 = モデルID 的 B 段（mid[1:3]）；也接受 "A/B" 形式（如 01/01 吉姆一族）。"""
    for w in want:
        w = w.strip()
        if not w:
            continue
        if "/" in w:
            a, b = w.split("/", 1)
            if mid[0].zfill(2) == a.zfill(2) and mid[1:3] == b.zfill(2):
                return True
        elif mid[1:3] == w.zfill(2):
            return True
    return False


PROV_SRC = {}


# ── 批次排序 & 系列统计 ──
def series_of(mid):
    return "%s/%s" % (mid[0].zfill(2), mid[1:3])


def series_report(universe, cur, prev, accept):
    """每个系列：台数 / 已定（页面上填了 7 位練度ID）/ 本批新增 / 例（第一个有名字的）。"""
    st = {}
    for mid, wiki, lid in universe:
        d = st.setdefault(series_of(mid), {"n": 0, "done": 0, "ex": ""})
        d["n"] += 1
        if is_lid(lid):
            d["done"] += 1
        if not d["ex"] and wiki:
            d["ex"] = wiki
    for a in accept:
        d = st.setdefault(series_of(a["mid"]), {"n": 0, "done": 0, "ex": ""})
        if a["kind"] == "new":
            d["batch"] = d.get("batch", 0) + 1
    return st


# ── 子进程 ──
def run_script(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        print("  !! 缺脚本 %s（跳过）" % rel)
        return False
    print("  $ python %s" % rel)
    r = subprocess.run([sys.executable, p], cwd=ROOT, capture_output=True)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    for l in out.splitlines():
        print("    | %s" % l)
    if r.returncode != 0:
        print("  !! %s 退出码 %s" % (rel, r.returncode))
        return False
    return True


def diff_line(label, path, before_rows, before_bytes):
    after_rows, after_bytes = nrows(path), nbytes(path)
    d = after_rows - before_rows
    print("  %-34s %5d → %5d 行 (%+d)   %7d → %7d B" %
          (label, before_rows, after_rows, d, before_bytes, after_bytes))


class Tee:
    """让报告同时进终端和 --report 指定的文件。"""

    def __init__(self, stream, fh):
        self.stream, self.fh = stream, fh

    def write(self, s):
        self.stream.write(s)
        self.fh.write(s)
        return len(s)

    def flush(self):
        self.stream.flush()
        self.fh.flush()


def die(msg):
    print(msg)
    sys.exit(2)


# ── 主流程 ──
def main():
    ap = argparse.ArgumentParser(description="把 ms_match.html 的人工对照装配成可下发的数据（默认 dry-run）")
    ap.add_argument("--pairs", help="ms_wiki_pairs.json 路径（默认自动找 iconmatch/ 与下载目录）")
    ap.add_argument("--series", action="append", default=[],
                    help="只处理这个系列（モデルID 的 B 段，如 01；也可写 01/01）。可重复")
    ap.add_argument("--limit", type=int, default=0, help="本次最多纳入 N 条新增（按 系列→練度ID 排序）")
    ap.add_argument("--apply", action="store_true", help="落盘：写 names/模型号映射-页面.csv + 重建全集")
    ap.add_argument("--ship", action="store_true", help="并生成三张下发表到 server/datafiles（需 --apply）")
    ap.add_argument("--force", action="store_true", help="把「冲突」也一并写入（人工改判，慎用）")
    ap.add_argument("--report", help="把报告另存成一个 markdown/文本文件")
    args = ap.parse_args()

    if args.ship and not args.apply:
        die("--ship 要跟 --apply 一起用（不然 names 层没更新，gen_msma_truth 出来的表还是旧的）")
    if args.report:
        sys.stdout = Tee(sys.stdout, io.open(args.report, "w", encoding="utf-8", newline="\n"))

    path = find_pairs(args.pairs)
    pairs, meta, items = load_pairs(path)
    auth, code_dir, lid_names = load_auth(), load_code_dir(), load_lid_names()
    cur, prev = load_current(), load_page_prev()
    global PROV_SRC
    PROV_SRC = load_prov()

    print("=" * 78)
    print("源文件  : %s" % path)
    if meta.get("exported"):
        print("导出时间: %s   页面自报 filled=%s/%s" %
              (meta.get("exported"), meta.get("filled", "?"), meta.get("total", "?")))
    print("基线    : 全集 %d 条 ｜ 页面.csv %d 条 ｜ 权威モデルID %d 个 ｜ 名册 %d 台" %
          (len(cur), len(prev), len(auth), len(lid_names)))
    if args.series:
        print("系列过滤: %s" % ", ".join(args.series))
    print("=" * 78)

    accept, conflict, todo, sus, skip_series = classify(pairs, auth, cur, prev, args.series)

    # 排序：系列 → 練度ID（稳定可复现）
    accept.sort(key=lambda a: (series_of(a["mid"]), a["lid"], a["mid"]))
    newones = [a for a in accept if a["kind"] == "new"]
    if args.limit and args.limit > 0 and len(newones) > args.limit:
        dropped = newones[args.limit:]
        drop_ids = set(id(x) for x in dropped)
        accept = [a for a in accept if id(a) not in drop_ids]
        newones = newones[:args.limit]
        print("\n★--limit %d：本次只纳入前 %d 条新增，剩下 %d 条留到下一批"
              % (args.limit, args.limit, len(dropped)))
        for a in dropped[:15]:
            print("    （留批）%s → %s  %s" % (a["lid"], a["mid"], a["wiki"]))
        if len(dropped) > 15:
            print("    ...（共 %d 条留批）" % len(dropped))

    # ── ② 逐条报告 ──
    print("\n① 分类")
    print("  新增（可写）        %3d" % len(newones))
    print("  一致（表里同值）    %3d" % len([a for a in accept if a["kind"] == "same"]))
    print("  冲突（表里是别的）  %3d   ← 默认不写，--force 才改判" % len(conflict))
    print("  待定（練度ID 空）   %3d   ← 页面上还差最后一格" % len(todo))
    print("  可疑（格式/权威树） %3d" % len(sus))
    if skip_series:
        print("  （系列过滤掉 %d 条）" % skip_series)

    if conflict:
        print("\n② 冲突明细（練度ID 已经指向别的モデルID ⇒ 两边必有一边错，默认不写）")
        for c in sorted(conflict, key=lambda x: x["lid"]):
            print("  %s  现有 %s（%s） → 页面想填 %s   %s" %
                  (c["lid"], c["old"], c["src"], c["mid"], c["wiki"]))
            print("       %s → %s    ｜ %s → %s" %
                  (c["old"], code_dir.get(c["old"], ("?", "?"))[1],
                   c["mid"], code_dir.get(c["mid"], ("?", "?"))[1]))
            if c["from_page"]:
                print("       ⚠️ 这个值是上次你自己写进 页面.csv 的 ⇒ 大概率是这次在页面上改主意了")

    if sus:
        print("\n③ 可疑（这 %d 条**不会**写进去，请在页面上修）" % len(sus))
        for s in sorted(sus, key=lambda x: x["mid"]):
            print("  mid %s  lid %-8s %s   %s" % (s["mid"], s["lid"] or "-", s["wiki"], s["why"]))

    if todo:
        print("\n④ 待定（有名字但没填練度ID）：%d 台" % len(todo))
        for t in sorted(todo, key=lambda x: (series_of(x["mid"]), x["mid"]))[:20]:
            print("  [%s] %s  %s" % (series_of(t["mid"]), t["mid"], t["wiki"] or "(无名)"))
        if len(todo) > 20:
            print("  ...（还有 %d 台，页面筛「未填/有动作」继续做）" % (len(todo) - 20))

    # 同一モデルID 被多台认领（正常，提醒一下别当 bug）—— 只看本批真正要写进去的
    multi_lid = {}
    for a in accept:
        multi_lid.setdefault(a["mid"], [])
        if a["lid"] not in multi_lid[a["mid"]]:
            multi_lid[a["mid"]].append(a["lid"])
    share = {m: v for m, v in multi_lid.items() if len(v) > 1}
    if share:
        print("\n⑤ 本批里同一个モデルID 被多台机体共用（换装/形态，属正常）")
        for m in sorted(share)[:10]:
            print("  %s ← %s" % (m, " ".join(share[m])))

    # ── ③ 批次内容 ──
    print("\n⑥ 本批新增明细（%d 条）" % len(newones))
    if not newones:
        print("  （没有新增）")
    by_series = {}
    for a in newones:
        by_series.setdefault(series_of(a["mid"]), []).append(a)
    for s in sorted(by_series):
        v = by_series[s]
        print("  [系列 %s] %d 台" % (s, len(v)))
        for a in v:
            cd = code_dir.get(a["mid"], ("", ""))
            nm = lid_names.get(a["lid"], {})
            print("     %s → %s  %-22s %s %s%s" %
                  (a["lid"], a["mid"], a["wiki"] or "(无名)",
                   cd[0] or "?", cd[1] or "?",
                   "  表内名:%s" % (nm.get("cn") or nm.get("jp") or "?") if nm else "  ⚠️名册里没这个練度ID"))

    # ── ④ 系列进度 ──
    universe = [(it.get("mid", ""), (it.get("wiki") or "").strip(), (it.get("lid") or "").strip())
                for it in items if is_mid(it.get("mid", ""))]
    if not universe:
        universe = [(p["mid"], (p.get("wiki") or "").strip(), (p.get("lid") or "").strip()) for p in pairs]
    st = series_report(universe, cur, prev, accept)
    print("\n⑦ 系列进度（从这挑下一批做哪个系列）")
    print("  系列    台数  已定  未定  本批新增  例")
    for s in sorted(st):
        d = st[s]
        print("  %-7s %4d  %4d  %4d  %6d    %s" %
              (s, d["n"], d["done"], d["n"] - d["done"], d.get("batch", 0), d["ex"]))

    # ── ⑤ 落盘 ──
    if not args.apply:
        print("\n（dry-run：没有改任何文件。确认无误后加 --apply；要一起出三张下发表再加 --ship）")
        return 0

    merged = dict(prev)
    written = list(newones)
    if args.force:
        written += conflict
    for a in written:
        nm = lid_names.get(a["lid"], {})
        cd = code_dir.get(a["mid"], ("", ""))
        merged[a["lid"]] = {"mid": a["mid"], "wiki": a["wiki"], "cn": nm.get("cn", ""),
                            "jp": nm.get("jp", ""), "code": cd[0], "dir": cd[1]}

    print("\n⑧ 落盘")
    snap = {}
    for label, p in [("names/模型号映射-页面.csv", PAGE_CSV), ("names/练度ID-モデルID-全集.csv", FULL_CSV)]:
        snap[p] = (label, nrows(p), nbytes(p))

    lines = [PAGE_HEAD]
    for lid in sorted(merged, key=lambda x: (len(x), x)):
        v = merged[lid]
        lines.append(",".join([lid, v["mid"], v.get("wiki", ""), v.get("cn", ""), v.get("jp", ""),
                               v.get("code", ""), v.get("dir", ""), "页面"]) + ",")
    write_crlf(PAGE_CSV, lines)
    print("  写了 %s（%d 条，本次结论 %d 条）" % (os.path.basename(PAGE_CSV), len(merged), len(written)))

    if not run_script(os.path.join("datatables", "build_model_id_map.py")):
        print("  !! 全集重建失败 ⇒ 先别 ship")
        return 1
    for pth in snap:
        label, r0, b0 = snap[pth]
        diff_line(label, pth, r0, b0)

    if args.ship:
        snap2 = {}
        for fn in SHIP_FILES:
            p = os.path.join(SHIP_DIR, fn)
            snap2[p] = (fn, nrows(p), nbytes(p))
        print("\n⑨ 生成下发表（会先自动 .bak_machine 备份）")
        ok = run_script(os.path.join("datatables", "gen_msma_machine.py"))
        for pth in snap2:
            label, r0, b0 = snap2[pth]
            diff_line(label, pth, r0, b0)
        if ok:
            mm = os.path.join(SHIP_DIR, "msma_model.csv")
            if nrows(mm) != snap2[mm][1]:
                print("  ⚠️ msma_model.csv 行数变了（%d → %d）：gen_msma_machine 写的是 P235 口径"
                      % (snap2[mm][1], nrows(mm)))
                print("     （行键 col0 = 練度ID、モデルID 在 col71/72）。盘上原来那份是 1 行的旧形态，")
                print("     换口径会一并改变客户端预请求的 chara 目录集合 ⇒ 想保持 1 行就别加 --ship。")
            print("  ★下发口径：客户端重登即会重新下载（hashval 恒 0，无缓存跳过）")
    else:
        print("\n（没加 --ship ⇒ 只更新了 names/ 层，server/datafiles 未动）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
