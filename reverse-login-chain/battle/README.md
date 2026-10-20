# 战服（battle）逆向 · 工作区索引

> 目标：把 `_proto_battle_client`（战斗服协议）**全部交互摸清**，产出可直接照着写 Go 战服的总表 + 义务清单。
> 方法沿用登录链：**脚本批量提取（可重跑）+ 机器可验证判据 + 逐条 detail 文档 + 每条结论带 VA**。

## 一、先读这四份

| 文档 | 内容 |
|---|---|
| `../detail/B01-战服连接与命中处理-取证.md` | **战斗连接怎么建**（3 个 VCE 会话 / TCP / 同一 helper）+ **服务器回的伤害怎么被客户端用掉**（血条/伤害数字） |
| `../detail/B02-战服交互全流程-时序与义务.md` | **全交互生命周期**：S1 握手 → S2 房间 → S3 开局出击 → S4 同步 → S5 开火 → S6 命中伤害 → S7 得分胜负，含服务端义务清单 |
| `../formats/battle-交互总表.md` | **287 条全表**（205 S→C + 92 C→S）：ID / 闸门 / 体长 / 参数数 / 处理者 impl / 解析序列 / 字段序，并按 S1..S11 分组 |
| `../formats/battle-体长线索.md` | **体长判据与结论**（143/205 已三重验证为定长） |
| `../detail/B15-战服引导门控链-取证.md` | ★★**连上战斗服后的"顺序铁律"**：`0xA5DA → 0x1365 → [0xE041 ⇒ 三连] → [0xE650 ⇒ 0x86B2]`；三道门（`app+416220` / 会话状态 3\|4 / `app+114268&4`）、状态步 vtable、已落地的 Go 引导代码 |

辅助：`../formats/battle-报文总表.md`（字段序 + MVP 清单）、`battle_protocol_raw.json` / `battle_bodylen.json` / `battle_handlers.json`（机读）、`../formats/_battle_case_trace.txt`（逐指令解析轨迹）。

## 二、怎么重跑（IDA MCP，任意会话）

```
py_exec_file  f:\9ymsgo\9you\reverse-login-chain\tools\dump_battle_protocol.py    # 报文/字段/ID/闸门
py_exec_file  f:\9ymsgo\9you\reverse-login-chain\tools\battle_bodylen.py          # 体长（依赖上一份 JSON）
py_exec_file  f:\9ymsgo\9you\reverse-login-chain\tools\battle_handlers.py         # 处理者/参数数/解析序列/分组
py_exec_file  f:\9ymsgo\9you\reverse-login-chain\tools\dump_battle_case_trace.py  # 需要的报文的逐指令轨迹
```

## 三、已固化的关键常量（写代码直接用）

| 项 | 值 |
|---|---|
| 收包分发器 | `sub_B0CC20`（0xB0CC20..0xB317DF） |
| `CGVOProtoBattle` vtable | **0xEED7AC**（分发器在 **+0x54**；auth 0xEED714、lounge 0xEEDB6C 同布局） |
| 战斗协议对象 | `dword_1201A64`（ctor `sub_BAAE90`，会话字段 **+16576**） |
| 连接 helper | `sub_AF7130`：`mgr->vt[24](session,host,port,30000,0)`；battle 包装 = `sub_AF7400`（调用者 `sub_440080`） |
| 解析读取器 | `sub_B02DD0`=u32 ｜ `sub_B02DF0`=u16 ｜ `sub_B06230`=u8 ｜ `sub_B02BA0`=有界 NUL 串 ｜ `sub_B41470/B413B0/B05E30`=取指针(0B) ｜ `sub_B418C0/B05ED0/B05EE0`=跳读(40/64/516) ｜ `sub_B077B0/B07880/B08160`=复合 |
| dump 助手（类型线索） | `sub_B03580`=i32 ｜ `sub_B032A0`=i16/u16 ｜ `sub_B03420`=2B ｜ `sub_B08500`=i64 ｜ `sub_B0C1F0`=u8 |
| 线程/节拍门 | `game_begin.snapshot_int_msec / snapshot_res_msec`（B13） |
| 坐标量化因子 | `app+0x1C230`（`sub_AFBE40` 用它缩放 3 个坐标） |
| ★引导顺序铁律 | `0x34A9→0xDE24` ⇒ `0xF24B→0xA5DA` ⇒ `0x1365` ⇒ `0xE041⇒0x9951/0x1E2F/0xAB6F` ⇒ `0xE650⇒0x86B2`（B15） |
| ★进战场三道门 | ① `app+416220`（**只由 `0xA5DA` 的 `sub_448FE0` 置 1**）② `sub_AF7070()`＝战斗服会话状态 ∈ {3,4} ③ `(app+114268 & 4) == 0` |
| 战场就绪判据 | `sub_43F7F0` = `app[416220] && sub_AF7070()` |
| 状态步 vtable（tick 恒在 **+0x08**） | `CGameStateStepUpdateLoginBattle` = `0xD68474` → `sub_440080`；`CGameStateStepUpdateGameBegin` = `0xD684EC` → `sub_440520`（用 `0xA5DA` 的 `mission_id` 调 `sub_629120` 加载任务） |
| `0xA5DA` 处理链 | `vt+0x70 = sub_BA8C20 → sub_AFAB40 → sub_448FE0(app, 20 参)`；`sub_BA8C20` 另写 `proto+16584 = (result>=0)` |

## 四、进度（详见 `workqueue.json`）

| 项 | 标题 | 状态 |
|---|---|---|
| B01 | 战服连接方式与命中处理链 | ✅ done |
| B02 | 全交互时序与义务 | ✅ done |
| B03 | `authenticate_r`(0xA5DA) 20 字段 + 21 参映射 | ✅ done（`B03…` + `B15` §1） |
| B04 | `game_begin`(0x1365) 23 参 + **4 并列数组** | ✅ done（`B04…` + `B15` §2） |
| B05 | `msma_spawn_*` 出击族 | 🟢 大半 done（`B15` §8/§16/§17：`0x86B2`=**变长 18+len(串)+1**、`0x7B52` 体 u32、`0xFEBB→0xE5FC→0x7621` 触发链已定并落地；`0x8DE4`/`0x640D` 语义与线布局已定案（§16.3/§16.6）⇒ **已发**；剩 `0x61AF btlroom_enter` 请求体） |
| B06 | 实体快照（含 `zbuff` 压缩流） | ✅ done（`B06`+`B06b`：压缩非阻塞、列式 31 列、`dirty_bits` 定案） |
| B07 | 开火族 44 条（`weapon_fire__*`） | 🟡 partial（普通射击**不广播**已定案；逐条转发条件待补） |
| B08 | 命中/伤害/死亡族 | 🟢 核心闭环已落地（`hit_from`/`shield`/`dead`/`wait_update`/`reborn`，见 `B15` §16）；剩 `body_region` 系数口径与 `optbits` 位定义 |
| B09 | 得分/进度/胜负 12 条 | 🟢 计分闭环已落地（`0x844B kill_count_update` + `0x8D59 score_update` 与 `0x9105 dead` 同批下发；`0xD1B3`=`sub_447450` 逐条 40B 出击点进度、MVP 可不发；见 `B15` §17.6）；剩 `reason` 字段语义 |
| B10 | 指挥官/战术 40 条 | ⬜ todo |
| B11 | NPC AI 托管 18 条 | 🟢 托管链路已通（`B15` §19.1：`0xB463 install`+`0xB604 resume` 已发 ⇒ 靶机会跑；另 5 条 S→C 指令编码器已落；C→S 上报 3 条只记日志）；剩 `0xA39E change_movetype`(5B/3参) 参数序与 `set_fire_point` 的编排策略 |
| B12 | 载具/道具/演出 20 条 | ⬜ todo |
| B13 | 战斗循环 tick 模型 | 🟡 partial（快照流启动时机 = `0x2CAB`，节拍 = `0x1365.snapshot_int_msec`，已落地 `0x5EEA` 列式；见 `B15` §10） |
| B14 | 服务端 MVP 与验收判据 | 🟢 已能"进战场 + 出击 + 同步 + **打**"：引导 3/4/5 步（`B15` §6）、S5 伤害/死亡/复活（§16）、计分（§17.6）、**场上靶机**（§18：`0x717D`+`0xE4DB`，没有它命中全判 `Missed`）；剩 `0x61AF` 请求体与多客户端广播 |
| **B15** | **战服引导门控链（顺序铁律 + 每道门）** | ✅ done（规划外新增，避免与 B09 撞号） |

## 五、铁律（沿用登录链）
1. ID/字段/体长**必须有 VA 或脚本产物支撑**，不许猜。
2. 体长以「解析读取器字节数 == 客户端 alloc」为准（三重验证）。
3. 字段名取 **dump 串原文**。
4. 每轮先重跑三个脚本，保证三份产物一致。
5. 服务端结论 → `server\docs\MEMORY.md`；客户端/协议结论 → `.codebuddy\memory\YYYY-MM-DD.md`。
