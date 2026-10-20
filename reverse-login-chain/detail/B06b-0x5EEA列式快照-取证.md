# B06b · `entity_snapshot_splitdelta`(0x5EEA) **列式快照** —— 服务端可直接照抄的线格式

> 2026-09-15 IDA 实测（case 0xB193EA..0xB1A460，闸门 `push 62h`=98，`alloc=0x9FC4`）。
> **这是"别人看到别人动"的推荐实现路径**：与压缩版 `0xBAE4` 解压后同构（同由 `sub_AA2640` 列式装配器消费），但**不需要任何编解码器**。

## 1. 数组原语（全部 byte-exact 反汇编）

| 助手 | 语义 | 用途 |
|---|---|---|
| `sub_B41470(&p, &cur)` | `*p = *cur`（取指针）; `cur += 4` | u32 字段 |
| `sub_B413B0(&p, &cur)` | 同上但 `cur += 2` | u16 字段 |
| `sub_B41460` / `sub_B05E30` | 取 1 字节并前进 1 | u8 字段 |
| **`sub_B05E40(&p, &cur, n)`** | `*p = cur; cur += 2*n` | **u16 数组（n 个）** |
| **`sub_B05EA0(&p, &cur, n)`** | `*p = cur; cur += 1*n` | **u8 数组（n 个）** |
| `sub_B02DD0/B02DF0/B06230` | 真正读值：u32 / u16 / u8 | 标量 |

⇒ 该报文的数组是**"每列自带 count"** 的列式（SoA）结构，客户端只记列指针（懒解析），实际装配交给 `sub_AA2640` 一族。

## 2. ★线格式（服务端照此拼包即可）

```
u32 frame_count            // B1943E
u32 remain_msec            // B19469(取指针)+B19478
── 下面 31 列，每列都是： { u32 count ; count × 元素 }  （count 各自独立，可为 0）
```
| # | 列名 | 元素宽 | # | 列名 | 元素宽 |
|---|---|---|---|---|---|
| 1 | `ent_id[]` | **u16** | 17 | `spbit_l[]` | u8 |
| 2 | `dirty_bits[]` | **u16** | 18 | `spbit_h[]` | u8 |
| 3 | `pos_real_x[]` | u16 | 19 | `spbit_hh[]` | u8 |
| 4 | `pos_real_y[]` | u16 | 20 | `spbit2[]` | **u16** |
| 5 | `pos_real_z[]` | u16 | 21 | `hp_percent[]` | u8 |
| 6 | `pos_diff_x[]` | **u8** | 22 | `hp_percent_shield[]` | u8 |
| 7 | `pos_diff_y[]` | **u8** | 23 | `down_power[]` | **u16** |
| 8 | `pos_diff_z[]` | **u8** | 24 | `equip_index[]` | u8 |
| 9 | `dir[]` | **u8** | 25 | `score1[]` | **u16** |
| 10 | `target_real_x[]` | u16 | 26 | `water_index[]` | u8 |
| 11 | `target_real_y[]` | u16 | 27 | `score2[]` | **u16** |
| 12 | `target_real_z[]` | u16 | 28 | `layer_index[]` | u8 |
| 13 | `target_diff_x[]` | **u16** | 29 | `score3[]` | **u16** |
| 14 | `target_diff_y[]` | **u16** | 30 | `rideon_ent_id[]` | **u16** |
| 15 | `target_diff_z[]` | **u16** | 31 | `lockon_ent_id[]` | **u16** |
| 16 | `spbit_ll[]` | u8 | | | |

**实测列序（`sub_B05E40`=u16 列 / `sub_B05EA0`=u8 列 的调用地址序）**：
```
u16 u16 u16 u16 u16 | u8 u8 u8 u8 | u16 u16 u16 u16 u16 u16 | u8 u8 u8 u8
| u16 | u8 u8 | u16 | u8 | u16 | u8 | u16 | u8 | u16 u16 u16
```
与上表逐项对齐（共 **31 列**，与 dump 字段名个数完全一致 ✓✓）。

## 3. 与 44B 逐条快照的字段映射（服务端"同一份世界状态"两种投影）

| 44B 条目字段 | 对应的 splitdelta 列 |
|---|---|
| `ent_id` | 列1 `ent_id[]`（**同一索引即同一实体**，所有列按下标对齐） |
| `pos_x/pos_y/pos_z` | 列3/4/5 `pos_real_*`（差分走列6/7/8） |
| `dir` | 列9 `dir[]`（差分后 1 字节） |
| `target_x/y/z` | 列10/11/12（差分 13/14/15） |
| `special_bits`(u32) | 列16-19 `spbit_ll/l/h/hh`（4×u8 = 32 位拆分！） |
| `special_bits2` | 列20 `spbit2[]` |
| `hp_percent` / `hp_percent_shield` | 列21 / 列22 |
| `down_power` | 列23 |
| `equip_index` | 列24 |
| `score1/2/3` | 列25 / 27 / 29 |
| `water_index` / `layer_index` | 列26 / 列28 |
| `rideon_ent_id` / `lockon_ent_id` | 列30 / 列31 |
| — | 列2 `dirty_bits[]` = 该实体的"变化掩码"（**纯 splitdelta 独有**） |

⇒ ★印证了 B06 的结论：**`dirty_bits`（u16）就是写进 44B 槽 `0x2A` 的字段**（槽内偏移 0x2A-0x2B），所以 `0x568A` 全量快照根本没有它。

## 4. 服务端落地配方（推荐 MVP）
1. 每帧（节拍 = `game_begin.snapshot_int_msec`）构造：
   - `frame_count` 单调递增；`remain_msec` 本帧剩余毫秒；
   - 31 列，**每列 count 各自填**（只发变化的实体 → count 小、带宽低；全量时所有列 count = N 且下标对齐）。
2. `dirty_bits` 填 **`0xFFFF`**（★不再是"暂不确定"的兜底，而是有据的正确值：31 列 > 16 位 ⇒ 非逐列掩码；消费端只看"非 0"与 `& 0x7000` 两门，语义 = 全字段刷新）；
   - 与之配套：**全列 count=N（全量）** ⇒ 整体行为等价于"全量快照"，无需压缩、无位映射风险。
3. 坐标/朝向沿用 44B 那套量化：`世界坐标 = s16 × K`（`K = *(dword_11E3EA8+0x1C230)`）；差分列 `pos_diff_*` 为 1 字节小差值。
4. 若客户端不买账（例如必须 `0xBAE4`），再考虑 zlib/LZP 编码（内容 = 本表同一份字节流）。

## 5. 待验证/待办
- [ ] `dirty_bits` 的**位↔分组映射**（**不阻塞**，见 §4.2）：★**结构性定论——它不可能是"一列一位"**：本快照共 **31 列**，`dirty_bits` 仅 **u16=16 位**，装不下 30 个非自身列 ⇒ 必为**分组/事件位**；客户端消费端只显式测 **`& 0x7000`**（B06 §2.2）⇒ **服务端恒填 `0xFFFF`** 即同时满足"非 0 有效门"与"0x7000 被置位"，语义等于"全字段刷新"。
  真正要做 delta 时：在 `0x486A2F test word ptr [edi+2Ah],7000h` 取真机值，再按 `sub_AA2640` 的参数表反推分组。
- [ ] `pos_diff_*` / `dir` / `target_diff_*` 的**量化精度**（1 字节差分 vs 绝对值的选择条件）。
- [ ] `0x5EEA` 的 `frame_count/remain_msec` 与 `0x568A` 是否**共用同一条时间轴**（`sub_4401D0`）。
