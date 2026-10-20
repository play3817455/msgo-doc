# 未决问题 / 反例 / 关联 —— SC-0x1365-battle-game_begin

## 1. 存疑点（已标 `?`）

| # | 项 | 现状 | 待补证据 |
|---|---|---|---|
| 1 | `vt[0xEC]` 业务定名 | 只知槽号 `0xEC`，**23 个实参**（实参序已逐条记录，见 README §3 / asm.md E12） | 虚表填充点（battle 客户端对象构造处） |
| 2 | `snapshot_res_msec` 语义 | 名称含 `res`（resend? resolution?）；与 `snapshot_int_msec` 的区别未交叉 | 服务端业务实现 / 客户端快照代码 |
| 3 | `sudden_type` 枚举 | 突发事件类型；取值表未交叉 | `datatables/` 突发事件表 |
| 4 | `is_disable_conq_sp` / `is_room_suspend` 取值 | 只知 1 字节；业务为布尔 | UI 判定分支 |
| 5 | `mapgimmicks` 成员语义 | 成员名全部来自打印器（`sub_B0AEA0`），**枚举/单位**（如 `route_number`、`local_ctrl_id`）未交叉 | `datatables/` 机关表 + `0x1159` 增量更新文档 |
| 6 | `respawn_posts.name` | `char[13]` 定长（无长度前缀、无 NUL 语义保证） | 与 UI 显示点对照；注意 13 字节非 4 字节对齐 |
| 7 | `config`/`progress` 的 slot 与 span | claim 分别 40 / 64，但结构体成员只用到 34 / 46 ⇒ 槽尾部为**未用填充**（reader 不读） | 若后续命令使用槽内其余字节则应复核 |

## 2. 反例 / 易错点（★本批最大一条）

- **机器草案严重漏读**：`draft-wire.md` 只抽到 13 个定长字段（46 字节）并在 `0xB0FE43 call sub_B418C0`（结构体预留）处**停止扫描**，完全漏掉 `config`/`progress`/3 组数组/`bgm_desc`/`mission_phase` 共 10 个顶层字段位。**容量 0x2806 反推立刻暴露这一点**（13 字段只占 46 字节，离 10246 差 10200）。
- **结构体 claim（槽步进/跨度）≠ 线长**（本条 5 处）：
  | 结构/元素 | claim（槽） | 线长（reader 实际消费） |
  |---|---|---|
  | `config` | `0x28 = 40`（`sub_B418C0`） | **34**（`sub_B077B0`） |
  | `progress` | `0x40 = 64`（`sub_B05ED0`） | **46**（`sub_B07880`） |
  | `respawn_posts` 元素 | `0x50 = 80`（`sub_B05F20`） | **58**（`sub_B079A0`） |
  | `mapgimmicks` 元素 | `0xBC = 188`（`sub_B05F50`） | **52**（`sub_B07BD0`） |
  | `bgm_desc` | `0x14 = 20`（`sub_B41740`） | **14**（`sub_B07E00`） |
  ⇒ 容量按左列算：`0x2806 = 46 + 40 + 64 + 4 + 50×80 + 4 + 32×188 + 20 + 4 + 11×4 + 4`（**精确相等**）。
- **复合读取器必须整函数扫描**（本批 3 处命中，全部因「失败出口 `retn` 之后还有成功路径」）：
  - `sub_B077B0`：失败出口 `0xB07862`，成功路径自 `0xB0786B` 起再读 `[edi+0x24]`（u32）⇒ 线长 30→**34**。
  - `sub_B07880`：失败出口 `0xB0797E`，成功路径自 `0xB07987` 起再读 `[edi+0x2C]`（u32）⇒ 线长 42→**46**。
  - `sub_B079A0`：失败出口 `0xB07ADC`，成功路径自 `0xB07AE5` 起再读 `[edi+0x3C]`（u32）⇒ 线长 54→**58**。
  - `sub_B07BD0`：失败出口 `0xB07CD0`/`0xB07D85`，成功路径从 `0xB07CD9`（2 次 u16 循环）与 `0xB07D8C`（`[edi+0x32]`）继续 ⇒ 线长 **52**。
  - `sub_B07E00`：无分支收窄，线长 **14**（`1+4+4+4+1`）。
- 数组**无独立「空跳过」字段**：`N == 0` 时数组占 0 字节，闭合校验随之成立（循环 `test ebx,ebx / jbe`）。
- 三个计数上限来自块内 `cmp`：`32h`(50)、`20h`(32)、`0Bh`(11) —— 这三个数字是**复核容量公式的关键交叉证据**。

## 3. 关联

- `../SC-0x1159-battle-game_mapgimmick_update/`（`0x1159`）：`mapgimmicks` 的**增量更新版**（4+7N vs 本命令 4+52N，注意两者元素结构完全不同：`0x1159` 元素仅 3 成员）。
- `../SC-0x243B-battle-game_btlfield_change/`（`0x243B`）：`btlfield` 的切换通知。
- `../SC-0x1113-battle-game_script_play/`（`0x1113`）：开局脚本播放。
- `../SC-0x0C5F-battle-commander_candidacy_start/`（`0x0C5F`）：指挥官选举，通常在 `game_begin` 前后。
- 计数器 `[esi+0xC40]`（64 位）每收一条 +1。
