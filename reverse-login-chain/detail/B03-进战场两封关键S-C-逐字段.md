# B03 · 进战场两封关键 S→C 逐字段：`authenticate_r`(0xA5DA) 与 `game_begin`(0x1365)

> 2026-09-15，IDA 实测（VA 全部给出）。判据：**解析读取器序列**（case 入口 → dump 头，按地址顺序）+ **dump 字段名**（客户端日志拼接，20/20 一一对应）
> + `alloc`（`push N; call vt[0x78]` = 解析缓冲/上行上限）+ 复合读取器反编译。
> 探针工具：`tools/battle_detail_trace.py` → `formats/_battle_detail_trace.txt`。

## 0. 读取器宽度表（本轮实测，写服务端直接用）
| 读取器 | 含义 | 线上字节 |
|---|---|---|
| `sub_B02DD0` | 读 u32 | 4 |
| `sub_B02DF0` | 读 u16 | 2 |
| `sub_B06230` | 读 u8 | 1 |
| `sub_B02BA0` | 读**有界 NUL 串**（参数 = cap） | len+1 |
| `sub_B41470` / `sub_B413B0` / `sub_B05E30` | 「取指针+占位」 | **0**（不占线上字节；由 137/143 例 alloc==Σ宽度 反证） |
| `sub_B418C0` / `sub_B05ED0` / `sub_B05EE0` | 「在解析结构体里预留 40 / 64 / 516 B」 | 0（其后紧跟的复合读取器才吃线上字节） |
| `sub_B077B0` | config 复合体 | **28**（见 §2） |
| `sub_B07880` | progress 复合体 | **46**（见 §2） |
| `sub_B08160` | extrarule_xwar_info 复合体 | **514**（见 §2） |

---

## 1. `recv_authenticate_r` = **0xA5DA** ｜ 闸门 3 ｜ 体长 = **636 + len(room_name)**

> ★★**2026-09-15 更正**：`config` 线上是 **34B**（不是 28B ✗，见 §2-a）⇒ 体长 base 630 → **636**。
> 依据 = 读取器 `sub_B077B0` 逐句（+4/+8 两处是 `*(_DWORD*)a1 = **a2; ++*a2`，**每次前进 4B**，不是 u8+u8 ✗），
> 旁证 = `0x1365` 解析轨迹里它前面紧跟 **`sub_B418C0`（预留 40B 结构体）= 34B 线 + 6B 对齐填充** ✓。
- handler：`vt+0x70 = sub_BA8C20 → sub_AFAB40 → sub_448FE0(app, 21 参)`（= **战场会话初始化**）
- 解析序列（按地址）：`B41470+B02DD0` ×2 → `push 49h; B02BA0` → `B41470+B02DD0` ×5 → `B05E30+B06230` → `B41470+B02DD0` → `B05E30+B06230` ×4 → `B418C0+B077B0` → `B05ED0+B07880` → `B413B0+B02DF0` → `B05E30+B06230` ×2 → `B05EE0+B08160`
- **dump 字段 20 个与解析项 20 个一一对应**（顺序一致）：

| # | 字段 | 线上类型/宽度 | 证据 |
|---|---|---|---|
| 1 | `result` | u32 | B02DD0 |
| 2 | `room_id` | u32 | B02DD0 |
| 3 | **`room_name`** | **NUL 串，cap 0x49(73)** | `push 49h; sub_B02BA0`（★此字段此前被工具漏掉，已修） |
| 4 | `mission_id` | u32 | B02DD0 |
| 5 | `extrule_id` | u32 | B02DD0 |
| 6 | `dc_node_id` | u32 | B02DD0 |
| 7 | `is_rankerbattle` | u32 | B02DD0 |
| 8 | `map_id` | u32 | B02DD0 |
| 9 | `is_vsclan` | u8 | B06230 |
| 10 | `comeback_stat` | u32 | B02DD0 |
| 11 | `is_playing` | u8 | B06230 |
| 12 | `is_netcafe` | u8 | B06230 |
| 13 | `team` | u8 | B06230 |
| 14 | `is_practice` | u8 | B06230 |
| 15 | `config` | **复合 34B** | B418C0+B077B0（§2-a） |
| 16 | `progress` | **复合 46B** | B05ED0+B07880（§2-b） |
| 17 | `expup_fgauge` | u16 | B02DF0 |
| 18 | `is_ev_caravan` | u8 | B06230 |
| 19 | `flag_wideuse` | u8 | B06230 |
| 20 | `extrarule_xwar_info` | **复合 514B** | B05EE0+B08160（§2-c） |

**字节核算**：4+4+(len+1)+4×5+1+4+1+1+1+1+**34**+46+2+1+1+514 = **636 + len(room_name)**。
`alloc = 734` ⇒ 上限 734，即 `len(room_name) ≤ 98`（实际串上限 73，符合）✓。

---

## 2. 三个复合读取器的精确布局（可复用）

### a) `sub_B077B0` — `config`（**线上 34B**；结构体 40B）
```
u16, u32, u32, u16, u32, u32, u32, u16, u32, u32    // 2+4+4+2+4+4+4+2+4+4 = 34
```
（注意第 2/3 项是**单字节**读入 4 字节槽）

### b) `sub_B07880` — `progress`（线上 46B）
```
u32, u32, u32, u32, u16, u16, u8, u8, u32, u32, u32, u32, u32, u32   // 16+4+2+24 = 46
```

### c) `sub_B08160` — `extrarule_xwar_info`（线上 514B）
```
u16  +  128 × u32        // 2 + 512 = 514（4 组 × 32 个）
```

---

## 3. `recv_game_begin` = **0x1365** ｜ 闸门 50 ｜ handler `vt+0xEC = sub_BA9120`（23 参）｜ alloc 0x2806(10246)
解析序列（按地址）：`B41470+B02DD0` ×6 → `B05E30+B06230` ×2 → `B41470+B02DD0` ×5 → `B418C0+B077B0`(config **34B**) → `B05ED0+B07880`(progress 46B) → **数组块** → `B41470+B02DD0` ×1 → `push 32h; B05D90`(业务回调)

| # | 字段 | 线上类型 | 备注 |
|---|---|---|---|
| 1 | `snapshot_int_msec` | u32 | **快照下发节拍** |
| 2 | `snapshot_res_msec` | u32 | 快照补发节拍 |
| 3 | `pos_factor` | u32 | 坐标量化因子（客户端存 `app+0x1C230`，`sub_AFBE40` 用它缩放坐标） |
| 4 | `map_id` | u32 | 地图 |
| 5 | `btlfield` | u32 | 战场/区域 |
| 6 | `clear_remain_msec` | u32 | 剩余时间/清场 |
| 7 | `is_disable_conq_sp` | u8 | 禁止占领 SP |
| 8 | `is_room_suspend` | u8 | 房间暂停 |
| 9 | `mission_id` | u32 | 任务 |
| 10 | `sudden_type` | u32 | 突发事件类型 |
| 11 | `sudden_bonus_target` | u32 | 突发事件目标 |
| 12 | `exp_min` | u32 | 经验下限 |
| 13 | `exp_max` | u32 | 经验上限 |
| 14 | `config` | 复合 **34B** | 同 §2-a |
| 15 | `progress` | 复合 **46B** | 同 §2-b |
| 16-19 | **数组块**：`respawn_posts[]` / `mapgimmicks[]` / `bgm_desc` / `missionunit_set[]` | 见下 | 与 dump 第 16~19 名对应（4 项共用一个复合解析块） |
| 20 | `mission_phase` | u32 | 任务阶段 |

**数组块（parse 段 0xB0FE94..0xB1004C 实测）**：
```
u32 count0            (上限 0x32 = 50，超了跳错误分支)
 count0 × {
    u32 a             (上限 0x20 = 32)
      a × { u32 ... }          // 内层还有 ≤0x0B(11) 的二级循环
 }
```
⇒ 结构 = **两级（或三级）嵌套表**：外层 ≤50 项，项内 ≤32 项，项内再 ≤11 项；dump 把它拆成 `respawn_posts[]`/`mapgimmicks[]`/`bgm_desc`/`missionunit_set[]` 四个名字。
⚠️ 剩余待办（B04 收尾）：把该块内**每一层的字段**（以及 `bgm_desc` 是串还是结构）逐个对齐到那 4 个名字；工具上再补一个"数组块逐层展开"的提取器。

**字节核算（不含数组块）**：6×4 + 2×1 + 5×4 + 28 + 46 + 4 = **124 + 数组块**；`alloc = 10246` ⇒ 数组块上限约 10KB（50×(32×…))。

---

## 4. 本轮顺带修好的工具问题（影响全表）
1. **dump 字段名有两种写法**：`field=` 与 `<值>" field="`；旧提取器只认第一种，**漏掉了所有字符串字段**（例：`authenticate_r.room_name`）。
   已修 `tools/dump_battle_protocol.py::scan_fields/field_name`（识别 `xxx="` 形态 + 分隔符 `"`/`,`/`=` 前后两种排布）⇒ **`authenticate_r` 由 19 字段补成 20 字段** ✓
2. 修好后**额外发现**：上行 `send_authenticate`(0xF24B) 的字段是
   `userid, world_id, pilot_id, room_id, `**`otp_battle`**`, is_comeback` ⇒ 印证"battle 变体带 OTP"（此前只从长度 21 vs 23 推断）✓
3. 三份总表已按新字段重生成：`battle-报文总表.md` / `battle-体长线索.md` / `battle-交互总表.md`。

## 5. 下一步
- **B04 收尾**：`game_begin` 数组块逐层字段 ↔ 4 个 dump 名；`bgm_desc` 定类型。
- **B06**：`entity_snapshot_splitdelta_compress`(0xBAE4) 的 `zbuff` 压缩流（handler `sub_BA9990`）——决定"能不能看到别人"。
- **B05**：`msma_spawn_*` 全族（出击流程）。
