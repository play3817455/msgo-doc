# -*- coding: utf-8 -*-
"""fix_datafiles.py —— 清理下发文件里的"孤立 CR"（`\\r\\r\\n` / 行内裸 `\\r`）。

★为什么：项目方言铁律 = UTF-8 无 BOM + **CRLF**；孤立 `\\r` 会破坏按行/按列的解析，
  而且"读 → 改写"会让它逐轮增生（每轮多一个 `,`）✗。
处理：`\\r\\n` 归一为 `\\n` ⇒ 删掉剩下的裸 `\\r` ⇒ 再用 `\\r\\n` 重新拼行。
用法：python datatables/fix_datafiles.py [--apply]
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DF = os.path.join(ROOT, 'server', 'datafiles')


def main():
    apply = '--apply' in sys.argv
    dirty = clean = 0
    for dp, dns, fns in os.walk(DF):
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            b = open(p, 'rb').read()
            lone = b.count(b'\r') - b.count(b'\r\n')
            if b.startswith(b'\xef\xbb\xbf'):
                print('  [BOM，跳过不碰] %s' % os.path.relpath(p, ROOT))
            if lone == 0:
                # ★只处理"孤立 CR"；仅 BOM 的文件不动（如 autoexec_sv.cfg，能正常登录）
                clean += 1
                continue
            dirty += 1
            n_crlf = b.count(b'\r\r\n')
            print('  [脏] %-58s 孤立CR=%d（其中 \\r\\r\\n=%d）'
                  % (os.path.relpath(p, ROOT), lone, n_crlf))
            if not apply:
                continue
            t = b.decode('utf-8', 'replace')
            t = t.replace('\r\n', '\n').replace('\r', '')
            open(p, 'wb').write(('\r\n'.join(t.split('\n'))).encode('utf-8'))
            b2 = open(p, 'rb').read()
            print('       → 已修复：孤立CR=%d ｜ BOM=%s'
                  % (b2.count(b'\r') - b2.count(b'\r\n'), b2.startswith(b'\xef\xbb\xbf')))
    print('扫描完成：干净 %d 个，%s %d 个' % (clean, '已修复' if apply else '待修复', dirty))
    return 0


if __name__ == '__main__':
    sys.exit(main())
