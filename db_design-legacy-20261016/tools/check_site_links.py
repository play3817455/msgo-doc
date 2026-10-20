#!/usr/bin/env python3
"""站点死链检查（`site/**/*.html`）——`build_site.py` 生成后自检，也可单独跑。

为什么需要它：站点是**生成物**，页面的存在性由模型（对象 / 表 / 实体 / 命令）决定。
模型裁剪掉一个对象后，别的页面里指向它的 `<a href>` 会**静默变成死链**——HTML 不会报错，
浏览者才发现。这个脚本把「谁链了不存在的页」列出来，并把**出处**（引用方页面 + 链接文本）
一起打出来，便于回生成器里修，而不是手改 HTML（手改下次生成就被覆盖）。

现实战绩：2026-09 这次扫出 930 条死链 / 922 个目标，两个根因——
① 915 条是「原始证据切片」按 `schema/commands/_verify/<id>.json` 直接当 href 用，
   站点根下根本没有 `commands/_verify/`（那目录 1830 个文件 / 113MB，不随站点发布）；
② 15 条是名字被归位库收编（evflag3 / ms_rokaku / equip_set / ms_set 的协议实体页已裁）
   或配对名与真实命令 id 差一个 `_r` 后缀。两类都在生成器侧修（见 build_site.py 的
   `repo_file_html` / `ref_page_html` / `fmt_pair`），本脚本负责把它们盯住。

用法
====
  python tools/check_site_links.py              # 人类可读
  python tools/check_site_links.py --quiet      # 只在有死链时输出（CI，有则退出码 1）
  python tools/check_site_links.py --top 10     # 每个目标最多列 10 个引用方（默认 5）
  python tools/check_site_links.py --exclude '\\.json$'   # 只看页面级死链

判据
====
  * 只查站内链接：`href` 去掉 `#fragment`/`?query` 后取路径；`http(s)://` / `mailto:` /
    `javascript:` / `data:` / `tel:` 跳过。
  * 目标存在性按**站点内文件表**判：`a/b.html` 相对引用方所在目录做**词法**归一化；
    `/x/y.html` 从站点根解析；目录形式的引用（`foo/`）等价于 `foo/index.html`。
  * 归一化后跑到站点外的路径（`../…`）**不当死链**：那是仓库内文件链接（如
    `../../../db_design/schema/commands/_verify/*.json`、`.go` 源码），
    站点是 `file://` 打开的，指向仓库原件是刻意的（见 `build_site.repo_file_html`）。
  * `#anchor` 只核页面存在，不核锚点（锚点由页面自身保证）。
"""

from __future__ import annotations

import argparse
import collections
import html.parser
import posixpath
import re
import sys
import urllib.parse
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SITE = TOOLS.parent / "site"

SKIP_SCHEMES = ("http://", "https://", "mailto:", "javascript:", "data:", "tel:")


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for k, v in attrs:
            if k == "href" and v:
                self._href = v
                self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join("".join(self._text).split())))
            self._href = None
            self._text = []


def target_rel(page_rel: str, href: str) -> str | None:
    """站内 href → 期望存在的站点相对路径（posix）；外链 / 空链 / 站外返回 None。"""
    raw = href.strip()
    if not raw or raw.startswith("#"):
        return None
    if raw.lower().startswith(SKIP_SCHEMES):
        return None
    path = urllib.parse.unquote(urllib.parse.urlsplit(raw).path)
    if not path:
        return None
    if path.startswith("/"):
        rel = posixpath.normpath(path.lstrip("/"))
    else:
        rel = posixpath.normpath(posixpath.join(posixpath.dirname(page_rel), path))
    if rel == ".." or rel.startswith("../"):
        return None
    if path.endswith("/"):
        rel = f"{rel}/index.html"
    return rel


def run(site: Path = SITE, exclude: str = "", top: int = 5, quiet: bool = False) -> int:
    """扫全站；返回 0（无死链）/ 1（有死链）/ 2（站点不存在）。"""
    if not site.is_dir():
        print(f"缺站点目录 {site}（先跑 python tools/build_site.py）")
        return 2

    pages = sorted(site.rglob("*.html"))
    existing = {p.relative_to(site).as_posix() for p in site.rglob("*") if p.is_file()}
    dead: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    n_links = 0
    for page in pages:
        page_rel = page.relative_to(site).as_posix()
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        for href, text in parser.links:
            rel = target_rel(page_rel, href)
            if rel is None:
                continue
            n_links += 1
            if rel not in existing:
                dead[rel].append((page_rel, text))

    if exclude:
        rx = re.compile(exclude)
        dead = {k: v for k, v in dead.items() if not rx.search(k)}

    head = f"站点 {len(pages)} 页 / {n_links} 条站内链接"
    if exclude:
        head += f"（已排除 /{exclude}/）"
    if not dead:
        if not quiet:
            print(f"OK  {head}，无死链")
        return 0

    total = sum(len(v) for v in dead.values())
    print(f"FAIL  {head}：{total} 条死链，指向 {len(dead)} 个不存在的目标")
    for tgt, refs in sorted(dead.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print(f"\n  目标不存在：{tgt}   （{len(refs)} 条引用）")
        for page_rel, text in refs[:top]:
            print(f"     ← {page_rel}   链接文本：{text[:60]!r}")
        if len(refs) > top:
            print(f"     … 其余 {len(refs) - top} 条省略")
    print("\n修法：改**生成器**（build_site.py / build_homing_site.py / build_cfg_site.py）里"
          "产生该链接的地方，别手改 site/ 里的 HTML——下次生成会被覆盖。")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--exclude", default="",
                    help="正则：目标路径命中则不报（例：--exclude '\\.json$' 只看页面级死链）")
    args = ap.parse_args()
    return run(SITE, args.exclude, args.top, args.quiet)


if __name__ == "__main__":
    sys.exit(main())
