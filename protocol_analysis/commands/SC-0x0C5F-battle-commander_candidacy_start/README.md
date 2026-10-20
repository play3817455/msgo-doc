# SC-0x0C5F-battle-commander_candidacy_start

> 状态：`DONE`（2026-09-20，批次-4）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0C5F` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `commander_candidacy_start` |
| 名字字符串 | `)->_proto_battle_client::recv_commander_candidacy_start( `，引用点 `0xB0E7B1`（`push offset aProtoBattleCli_9`） |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0E708` .. `0xB0E879`（case 起始前导 `0xB0E701 push 0D6h`） |
| 错误码 | `0xD6`（`0xB0E76D push 0D6h` → `vt[0x64](1, 0xD6)`） |
| 关联命令 | 同族 `../SC-0xE12A-battle-commander_candidacy_end/`（`0xE12A`）、`../CS-0x6C48-battle-commander_candidacy_inbattle/`（`0x6C48`）；**无严格配对请求**（服务端主动开票通知） |

## 2. 结论摘要

- **报文体总长：定长 2 字节**（1 个 u16）。
- 长度校验：`0xB0E780 mov ebx,[esp+var_1B28]`（线游标）、`0xB0E784 cmp ebx,[esp+var_1B24]`（vs 报文末尾）、`0xB0E788 jnz loc_B0E766`（不等 ⇒ 报错）⇒ **整包精确消费完**。
- 声明容量 `push 2`（`0xB0E71D`）= **2 == 线长**（全定长 ⇒ 容量与线长强相等）。
- 是否分帧：否。
- 关键结论：唯一的 `remain_sec`（候选开始剩余秒数）交 `vt[0x29C]`（`0xB0E854` 取虚表项 / `0xB0E85D` 调用）；块内日志 `remain_sec=`（`0xB0E803`）。
- 「case 起始守卫」`sub_B05DA0`（`0xB0E708`，前导实参 `0xD6`）按命令号查 `[ebx+edi+18Dh]` 使能位并递增接收计数，**不是字段读取**（见 `asm.md` E0）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x0C5F` | `0xB0E7B1`（名字串引用点）；`0xB0E701 push 0D6h` | 确证 |
| 1 | 0 | 2 | u16 | `remain_sec` | 指挥官候选开始的剩余秒数 | 交 `vt[0x29C]`（唯一实参 `0xB0E85A push ecx`）；日志 `remain_sec=`（`0xB0E803`，十进制打印器 `sub_B032A0`） | `-`（倒计时秒数） | `0xB0E758`（`sub_B02DF0`）；槽预留 `0xB0E749`（`sub_B413B0`）；`0xB02E0B add [eax],2`；取值 `0xB0E7FF`（日志）/`0xB0E84F`（用途） | 确证 |
| — | 2 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB0E784`（`cmp`）、`0xB0E788`（`jnz`） | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB0E7B1` 落在 `sub_B0CC20` 的 case 块 `0xB0E708..0xB0E879` 内（全部错误路径用错误码 `0xD6`）。
2. 字段 = 「槽预留 `sub_B413B0`（u16）+ bounded 读取器 `sub_B02DF0`」一对，槽地址记在 `var_1B2C`。
3. 含义取自块内日志串 `remain_sec=`（`0xB0E803`，紧跟在 trace 串 ` (id:` 之后）。
4. 去向：`0xB0E84B mov eax,[var_1B2C]` → `0xB0E84F movzx ecx,word ptr [eax]` → `0xB0E854 mov edx,[edx+29Ch]` ⇒ `vt[0x29C](remain_sec)`。

### 4.2 长度闭合
- `2 = 2`；闭合点 `0xB0E784`/`0xB0E788` 要求「游标 == 末尾」✓
- 容量 2 == 线长（全定长 ⇒ 强相等）。

### 4.3 存疑点
见 `notes.md`（`vt[0x29C]` 槽名的业务定名、`remain_sec` 是否即 UI 倒计时源）。

## 5. 质量门自检

- [x] G1 字段表总长（2）与 `0xB0E784`/`0xB0E788` 的「游标 == 末尾」校验一致；容量 2 == 线长。
- [x] G2 线类型指回汇编 VA（`0xB0E758` + `0xB02E0B`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串 `remain_sec=`，用途追到 `vt[0x29C]`（`0xB0E85D`）。
- [x] G4 不确定项（`vt[0x29C]` 业务定名）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 同族命令 `0xE12A` / `0x6C48` 已在 §1 链接（本命令无严格配对请求）。
