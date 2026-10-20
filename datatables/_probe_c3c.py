# -*- coding: utf-8 -*-
import struct, math
d = {
 0xe0e780:1073741824, 0xd74fa8:1125515264, 0xd73338:1053609165, 0xd69a58:1120403456,
 0xe0e78c:1092616192, 0xe0ea4c:990057071, 0xe0ea54:948686693, 0xd68b84:1036831949,
 0xe0e778:1140457472, 0xd7a47c:939524352, 0xd675b4:1325400064, 0xd91af8:1056964608,
 0xe0ea50:0x3F06BCA2,
}
for k, v in d.items():
    print("0x%08X  u32=%-12d  float=%.9g" % (k, v, struct.unpack("<f", struct.pack("<I", v))[0]))
print()
print("连射白字 = trunc((2 - raw)*0.5263158*1500 + 0.4):")
for raw in (0.110657, 0.119523, 0.12458, 0.138523, 0.16638, 0.199323, 0.24999, 0.399457, 1.391257, 1.999257):
    disp = (2.0 - raw) * 0.5263158 * 1500 + 0.4
    print("   raw %.6f -> %.4f -> trunc %d" % (raw, disp, math.trunc(disp)))
print()
print("反推：sidecar 顯示值 -> raw（rapid_raw 的口径），再回代看是否可逆：")
_K = 0.5263158 * 1500
for disp in (1263, 1342, 1374, 1381, 1391, 1407, 1421, 1427, 1443, 1447, 1460, 1466, 1468, 1469, 1480, 1484, 1491, 480, 0):
    raw = 2.0 - (disp - 0.4) / _K
    back = math.trunc((2.0 - raw) * _K + 0.4)
    print("   disp %5d -> raw %.6f -> 回代 %d %s" % (disp, raw, back, "OK" if back == disp else "MISS"))
