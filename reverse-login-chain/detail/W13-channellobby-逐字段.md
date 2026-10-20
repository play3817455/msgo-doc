# W13 · channellobby 报文族逐字段（0xA3B2 enter / 0xD377 members_get / 0xC475 scene_transition / 0xA64A script_play / 0x1D02 members_get_r）

> 工作项：`W13`（P1）｜ 判据：**4 条请求 + 全部应答的逐字段，且给出「客户端下一步动作」判据**
> 目标文件：`GundamOnline_CHINA_v15.exe`（基址 `0x400000`，已脱壳）
> 方法：IDA Pro MCP 反编译 3 个 send 函数 + 3 个包装 + 3 个触发者，反汇编 `sub_B51930` 内 2 个 case（`0x1D02`/`0xA64A`）
> 日期：2026-09-15 ｜ 上游 `nodes/09-进入游戏大厅.md`（0xA64A/0xD377 已定 ID）＋ `nodes/10-大厅白屏全链路汇编分析.md`（0xA64A 体格式）＋ `detail/W07-机师报文-逐字段.md`（159B 记录）＋ `detail/W12-记录结构-逐字段.md`（0xD377 请求体 4B）
> 标注：✅ 本轮反编译/反汇编直接确认 ｜ ★ 本轮新增/修正 ｜ ⚠️ 仍未定 ｜ 继承=沿用旧节点/W07（本轮未重取证据）

---

## 0. 一句话结论

频道大厅（30002，`_proto_lounge_client` 同一对象第二次连接）有 **3 条客户端主动请求 + 1 条服务端主动推送 + 1 条应答**，全族如下：

| 报文 | 方向 | 通知索引/门 | 体 | 应答 |
|---|---|---|---|---|
| `0xA3B2` `send_channellobby_enter` | C→S | 96 | **空（仅 2B ID）** | **无**（无 `recv_*_enter_r` 串） |
| `0xD377` `send_channellobby_members_get` | C→S | 97 | `u32 is_simple`（4B） | **`0x1D02`** |
| `0xC475` `send_channellobby_scene_transition` | C→S | 100 | `u32 destination`（4B） | **无**（无 `recv_*_scene_transition_r` 串） |
| `0x1D02` `recv_channellobby_members_get_r` | S→C | 98（`push 62h`） | `u32 is_simple \| u32 world_client_num \| u32 count(≤0x800) + count×159B` | — |
| `0xA64A` `recv_channellobby_script_play` | S→C | 99（`push 63h`） | `src(NUL串,cap65) \| u32 val1 \| u32 val2` | — |

★**核心结论**：① `0xA3B2`/`0xC475` 两条请求**没有对应应答**——全 IDB 只有 `recv_channellobby_script_play` 与 `recv_channellobby_members_get_r` 两个 recv 串（`find_regex "recv_channellobby"` 仅 2 命中），服务端对这族唯一的主动手段是**推 `0xA64A` 脚本**；② **`0x1D02` 体没有 `result` 字段**——总表 §2.4 H2 的 `u32 result` 是旧猜测 ✗，真字段名 = `is_simple`（回显请求）+ `world_client_num`（世界在线数）+ `count`；③ `0xD377` 的请求体 4B（`u32 is_simple`）已在 W12 定案，本轮复核其**总长 6B 含 2B ID**、门 `this[189]`=索引 97；④ `0xA64A` 字段名 = **`src`**（日志串 `src="…"`，不是"name"）。

---

## 1. 汇编逻辑

### 1.1 发送侧：send 函数 → 包装 → 触发者

```
sub_B8DBB0  send_channellobby_enter（体空，2B，门 this[188]=idx96，通知 idx 96）
   ↑ sub_AFEC70() 包装（无参）
        ↑ sub_43C630(app,a2)  —— 进大厅：清 this[114202]，发 enter

sub_B8DD40  send_channellobby_members_get（体 u32 is_simple，总6B，门 this[189]=idx97，通知 idx 97）
   ↑ sub_AFEC90(a1=is_simple) 包装
        ↑ sub_42D830(app,a2)  —— 轮询：要求 大厅就绪 this[114201] && 会话就绪 sub_AF6FB0() && !this[114202]

sub_B8DEF0  send_channellobby_scene_transition（体 u32 destination，总6B，门 this[192]=idx100，通知 idx 100）
   ↑ sub_AFECB0(a1=destination) 包装
        ↑ sub_433770(app,scene_id) —— 切场景：scene_id → destination 映射后发（25 个调用点，全 UI 层）
```

### 1.2 关键函数表

| 地址 | 身份 | 作用 |
|---|---|---|
| `sub_B8DBB0` | ★send_channellobby_enter | `*v3=-23630`=0xA3B2；`v3->vt[120](v3,2)` alloc **2B**；体空；通知 `v11(this,96,v3,2)` |
| `sub_B8DD40` | ★send_channellobby_members_get | `*v4=-11401`=0xD377；`*(u32*)(v4+2)=is_simple`；alloc **6B**；通知 `(this,97,v4,6)` |
| `sub_B8DEF0` | ★send_channellobby_scene_transition | `*v4=-15243`=0xC475；`*(u32*)(v4+2)=destination`；alloc **6B**；通知 `(this,100,v4,6)` |
| `sub_AFEC70`/`sub_AFEC90`/`sub_AFECB0` | 包装（`sub_AF6E50()` 取协议对象后转调） | 三函数均先 `if(!sub_AF6E50())return 0` |
| `sub_43C630` | ★enter 触发者 | `a2!=0` 时清 `this+114202` 再 `sub_AFEC70()` |
| `sub_42D830` | ★members_get 触发者（轮询） | `!this[114201] || !sub_AF6FB0() || this[114202]` ⇒ 拒；`this[114202]=1` 后发 |
| `sub_433770` | ★scene_transition 触发者 | `switch(scene_id)` → destination 映射 |
| `sub_06980` | 159B 大厅成员记录读取器（23 字段） | 复用创建机师的读取器（W07 §3.6） |

### 1.3 通知索引 / 门序号总表（channellobby 族）

| 索引 | 角色 | 证据 |
|---|---|---|
| 96 | send enter（门 `this[188]`=92+96） | `sub_B8DBB0` `if(!this[188])` |
| 97 | send members_get（门 `this[189]`） | `sub_B8DD40` `if(!this[189])` |
| 98 | recv members_get_r 门（`0x1D02`） | case `push 62h` @`0xB574ED` = 97+1 ✓ |
| 99 | recv script_play 门（`0xA64A`） | case `push 63h` @`0xB7061C`（纯服务端推，不与 send 配对） |
| 100 | send scene_transition（门 `this[192]`） | `sub_B8DEF0` `if(!this[192])` |
| 101 | recv scene_transition_r 门（**无此 handler**） | 100+1，但全 IDB 无对应 recv 串 ⇒ 永不消费 |

---

## 2. 报文逐字段表（★核心交付）

> 通道 = `:30002`（channel）。u32=`sub_B02DD0`、u16=`sub_B02DF0`、u8=`sub_B06230`、NUL 串=`sub_B02BA0`。**线偏移**从报文体第 0 字节（不含 2B ID）起算。每 case 末尾 `游标 == 报文尾`，否则整包丢弃。

### 2.1 `0xA3B2` send_channellobby_enter（C→S，体空）

| # | 线偏移 | 类型 | 长度 | 字段名 | 取值域 / 必须非零 | 证据 |
|---|---|---|---|---|---|---|
| — | — | — | **0** | （体空） | 仅 2B ID，`alloc(2)` 只写 ID | `sub_B8DBB0` `*(_WORD*)v3=-23630` 后无任何字段写 |

- **期望应答**：无。服务端收到后应**主动推 `0xA64A`** 播大厅初始化脚本（这是 enter 之后客户端"下一步"的驱动来源）。
- **异常处理**：无应答不卡流程；但若服务端从不推 `0xA64A`，大厅场景只靠客户端本地 UI 流程推进（见 W08：`sub_442970` 由 FSM case0x14 触发，与 enter 无关）。

### 2.2 `0xD377` send_channellobby_members_get（C→S，体 4B）

| # | 线偏移 | 类型 | 长度 | 字段名 | 取值域 / 必须非零 | 证据 |
|---|---|---|---|---|---|---|
| 1 | 0 | u32 | 4 | `is_simple` | ★是否简表（0=完整/1=简表；服务端可忽略，仅回显） | `sub_B8DD40` `*(u32*)(v4+2)=a2`；日志 `aIsSimple="is_simple="` |

- **体 = 4B**（总 6B 含 2B ID）。
- **触发节奏**：`sub_42D830` 是轮询入口，要求 `大厅就绪(app[114201]) && 会话就绪 && !app[114202]`；`app[114202]` 是"成员拉取中"互斥位（发后置 1，`sub_43C630` 发 enter 后清 0）。实际约 **每 ~4s 一次**（历史 `server/logs/push.txt` 挂在 `0xD377` 节拍上补发的依据）。
- **期望应答**：`0x1D02`（见 §2.4）。

### 2.3 `0xC475` send_channellobby_scene_transition（C→S，体 4B）

| # | 线偏移 | 类型 | 长度 | 字段名 | 取值域 / 必须非零 | 证据 |
|---|---|---|---|---|---|---|
| 1 | 0 | u32 | 4 | `destination` | ★目标场景的"目的地编码"（0..6），见下表 | `sub_B8DEF0` `*(u32*)(v4+2)=a2`；日志 `aDestination="destination="` |

- **体 = 4B**（总 6B）。
- **★destination 映射**（`sub_433770` 的 `switch(scene_id)`，scene_id 是 `sub_43A350` 压栈的大厅场景号）：

| 场景号 scene_id（v5） | destination | 说明 |
|---|---|---|
| 4 | 1 | 变更频道转场（`sub_43BC70` 里 `sub_43A350(4,1.0)`） |
| 6 | 3 | |
| 8 | 2 | |
| 13 | **不发送**（`case 13: return sub_A7DF40(13)`） | 首屏转场场景，直接走本地 |
| 17 | 4 | |
| 19 | 5 | |
| 21 | 6 | |
| default（其它） | 0 | |

- **期望应答**：无。服务端收到 destination 后应**推 `0xA64A`** 播放该场景对应脚本（历史实测：服务端推 `0xA64A` 时客户端会切大厅场景）。

### 2.4 `0x1D02` recv_channellobby_members_get_r（S→C，应答 0xD377）

> case 入口 `0xB574ED`（`push 62h`；守卫链 `sub eax,1CF4h; jz loc_B577DF; sub eax,0Eh; jnz def` ⇒ ID=`0x1CF4+0x0E`=`0x1D02` ✓）；`vt[0x78](0x5800C)` alloc=360460（结构/向量**容量**总量，非体长 ✗）。

| # | 线偏移 | 类型 | 长度 | 字段名 | 取值域 / 必须非零 | 证据 |
|---|---|---|---|---|---|---|
| 1 | 0 | u32 | 4 | `is_simple` | ★回显请求的 is_simple（0/1）；无 result 语义 | 日志 `aIsSimple`（`sub_B02DD0` @`0xB57544`） |
| 2 | 4 | u32 | 4 | `world_client_num` | ★世界/频道当前在线客户端数 | 日志 `aWorldClientNum="world_client_num="`（`@0xB57581`） |
| 3 | 8 | u32 | 4 | `count` | ★成员条数，**≤ 0x800(2048)**（`cmp ebx,800h; ja` ⇒ 失败） | `sub_B02DD0` @`0xB57597` |
| 4 | 12 | 嵌套×count | 159×count | `pilots[]` | 大厅成员记录（159B/条，`sub_B06980`，23 字段，见 W07 §3.6） | 循环 `sub_B06980`，内存步长 `0xB0`=176B |

- **体长** = `12 + 159×count`。空列表（count=0）= **12B**；含自己（count=1）= **171B**。
- **★内存步长 vs 线长**：每条记录线 159B、内存 176B（`0xB0`），`sub_B41310` 按 count 预分配向量；末尾 `cmp cursor,end` 恰到底（`@0xB5761D`）。
- **★业务回调**：`vt[0x148](is_simple, world_client_num, pilots_ptr, count)`（`@0xB577AF`/`@0xB577C3`），即"成员列表更新"处理器（更新大厅成员面板）。
- **★无「必须非零」字段**：`is_simple`/`world_client_num`/`count` 全 0 即可过（count=0 时只发 12B 也能被接受）。
- **异常处理**：任一条 159B 记录越界、或 `count>0x800`、或游标≠末尾 ⇒ `vt[0x64](0x62,1)` 上报 + 整包丢弃。

### 2.5 `0xA64A` recv_channellobby_script_play（S→C，服务端主动推送）

> case 入口 `0xB7061C`（`push 63h`；守卫链 `sub eax,0A5FEh; jz loc_B70853; sub eax,4Ch; jnz def` ⇒ ID=`0xA5FE+0x4C`=`0xA64A` ✓）；`vt[0x78](0x49)` alloc=73（**结果结构体**大小 65B 名缓冲+2×u32，**不是体长** ✗）。

| # | 线偏移 | 类型 | 长度 | 字段名 | 取值域 / 必须非零 | 证据 |
|---|---|---|---|---|---|---|
| 1 | 0 | NUL 串 | 变长 | `src` | ★脚本名，**NUL 结尾、上限 65B(0x41)**；不带 `script/` 前缀 | `sub_B02BA0(dst,&cur,0x41)` @`0xB7066B`；日志 `aSrc="src=\""` |
| 2 | ++ | u32 | 4 | `val1` | 脚本参数 1 | `sub_B02DD0` @`0xB706A8`；日志 `aVal1="val1="` |
| 3 | ++ | u32 | 4 | `val2` | 脚本参数 2 | `sub_B02DD0` @`0xB706CC`；日志 `aVal2="val2="` |

- **体长** = `len(src)+1 + 4 + 4` = **`len(src)+9`（变长）**。末尾 `cmp cursor,end` 恰到底。
- **★业务回调**：`vt[0x14C](src, val1, val2)`（`@0xB70826`/`@0xB70837`），即"播放脚本"处理器（`/lobbyscript <名字.nut>` 机制，名字不带 `script/` 前缀）。
- **★踩坑（继承 nodes/10）**：勿按"定长 65B+8=73B"发 ✗——73 是客户端结果结构体大小、不是体长；`sub_B02BA0` 是 `memchr(NUL)` 找结尾，**必须变长**。名字要在 cap 65 内含 NUL。
- **异常处理**：名字 65B 内无 NUL、或游标≠末尾 ⇒ `vt[0x64](0x63,1)` + 丢弃。

---

## 3. 「客户端下一步动作」判据（★W13 判据核心）

| 事件 | 客户端动作 | 服务端必须做什么 | 失败现象 |
|---|---|---|---|
| 客户端**进入频道大厅** | 发 `0xA3B2` enter | **推 `0xA64A`**（播 `Lobby_Official.nut` 等） | 无应答不卡，但大厅脚本流程不启动 |
| 客户端**周期性轮询**（~4s） | 发 `0xD377` members_get | 回 `0x1D02`（is_simple 回显 + world_client_num + count + 159B×count） | 成员面板空；但**不卡大厅**（count=0 即可过） |
| 客户端**切场景** | 发 `0xC475`（scene_id→destination） | 据 destination **推 `0xA64A`** 播对应场景脚本 | 场景脚本不播，但 UI 本地流程仍会走 |
| 服务端**推脚本** | 收 `0xA64A` → `vt[0x14C]` 跑脚本 | — | — |

> ★ 关键：`0xA3B2`/`0xC475` 都**没有应答**，客户端不因缺应答而卡死；这族报文的"推进"靠**服务端主动推 `0xA64A`**（唯一 S→C 主动手段）。而 `0x1D02` 是唯一带体应答，但它对进大厅**不门控**（W08 已证门控在 `0x063E` 的 `is_processing_comeback`）。

---

## 4. 期望服务端回包（造包铁律）

1. **`0xD377` → `0x1D02`**：`u32 is_simple(回显) | u32 world_client_num | u32 count(≤2048) | count×159B`；空列表 = **12B**；159B 记录字段序 = W07 §3.6（`pilot_id u32 | name 25B定长 | troops u8(0基) | level u8 | mil_class u8 | byword u16 | ...`）。
2. **`0xA64A`（推）**：`src(NUL串,cap65) + val1(u32) + val2(u32)`，体长 = `len(src)+9`；脚本名**不带** `script/` 前缀。
3. **`0xA3B2`/`0xC475` 不回包**；收到后按需推 `0xA64A`。
4. ★ **体长必须精确 + 游标恰到底**（`0x1D02` 每条 159B、`0xA64A` 每个字段错位 ⇒ 整包丢弃）。

---

## 5. 待研究 / 未定

1. ⚠️ `sub_433770` 里 `sub_A7DF40(scene_id)` 的语义（切场景后本地还做什么）未追——它决定"destination 之外客户端本地动作"，但对服务端无影响。
2. ⚠️ `destination` 编码（0..6）的**业务语义**（各代表哪个大厅子场景）未与资源层 `script/UI/Lobby_*.nut` 逐条对应；服务端只需"收到后推对应脚本"，可先照抄历史 `0xA64A` 播 `Lobby_Official.nut`。
3. ⚠️ `is_simple` 的**业务分叉**（=1 时 `0x1D02` 记录是否应精简）未追——反编译显示 159B 读取器 `sub_B06980` 无条件读 159B，故 `is_simple` 不影响本结构线长；它只透传给 `vt[0x148]`。
4. ⚠️ `world_client_num` 与 `count` 的差（世界在线数 vs 本包成员数）未做真机对照。
5. ⚠️ `0xD377` 的 ~4s 轮询节拍是否由定时器注册（`sub_42D830` 的 4 个调用者 `sub_73E810/sub_88B280/sub_8B7E50/sub_8BB900` 全是 UI 事件）未逐一追——但"成员列表只在 UI 事件时拉取"已可解释历史"每 ~4s 出一次 0xD377"的现象（大厅心跳/界面刷新驱动）。

---

## 6. 对服务端落地的影响

1. ★ **`0x1D02` 无 `result` 字段**：`server/internal/protocol/lounge_channel.go` 若按旧总表"`u32 result + ...`"造 12B 成员应答，首 4B 会被客户端当 `is_simple` 读——值对业务无门控影响，但**语义错误**；建议按 `is_simple + world_client_num + count` 三字段造。
2. ★ **159B 成员记录与创建机师记录同构**（同 `sub_B06980`/`EncodeLobbyMember`）：服务端已有 `EncodeLobbyMember`（W12 已核对 `+0=pilot_id`/`+4=name(25B)`/`+29=troops`/`+30=level`/`+31=mil_class`/`+32=byword`），可直接复用。
3. ★ **`0xA3B2`/`0xC475` 无需应答**：服务端只需把这两条 ID 纳入已知报文（避免打"未知报文"），并在适当时机**主动推 `0xA64A`** 驱动大厅脚本。
4. ★ **`0xA64A` 变长铁律**：体长必须 `len(src)+9`（NUL 串），不能用定长 73B；历史已踩坑（nodes/10 §四）。
5. **`0xD377` 请求体 4B**（`is_simple`）服务端已可解析（W12 定案）；本轮补"总长 6B、门 97、回显 is_simple"。

---

## 7. 证据地址清单

| 结论 | 证据 |
|---|---|
| send enter 体空 / ID 0xA3B2 / idx96 | `sub_B8DBB0`（`if(!this[188])`；`*(_WORD*)v3=-23630`；`v3->vt[120](v3,2)`；`v11(this,96,v3,2)`） |
| send members_get 体 u32 is_simple / ID 0xD377 / idx97 | `sub_B8DD40`（`if(!this[189])`；`*(_WORD*)v4=-11401`；`*(u32*)(v4+2)=a2`；`v11(this,97,v4,6)`） |
| send scene_transition 体 u32 destination / ID 0xC475 / idx100 | `sub_B8DEF0`（`if(!this[192])`；`*(_WORD*)v4=-15243`；`*(u32*)(v4+2)=a2`；`v11(this,100,v4,6)`） |
| 全 IDB 仅 2 个 recv 串 | `find_regex "recv_channellobby"` ⇒ `recv_channellobby_script_play`(0xEE7574) / `recv_channellobby_members_get_r`(0xEE9A68) |
| 0x1D02 case + 门 98 + 字段序 | `sub_B51930` @`0xB574ED`（`push 62h`；守卫 `sub eax,1CF4h`/`sub eax,0Eh`）；字段 `is_simple`/`world_client_num`/`count` 日志 @`0xB576B6`/`0xB576DF`；`cmp ebx,800h` @`0xB575C0`；`sub_B06980` 循环 @`0xB575EF`；回调 `vt[0x148]` @`0xB577AF` |
| 0xA64A case + 门 99 + 字段序 | `sub_B51930` @`0xB7061C`（`push 63h`；守卫 `sub eax,0A5FEh`/`sub eax,4Ch`）；`sub_B02BA0(...,0x41)` @`0xB7066B`；`src`/`val1`/`val2` 日志 @`0xB70778`/`0xB707AD`/`0xB707D2`；回调 `vt[0x14C]` @`0xB70826` |
| enter 触发者 + 清 114202 | `sub_43C630`（`sub_AFEC70()` @`0x43c66c`；`this+114202=0` @`0x43c679`） |
| members_get 触发者（轮询门槛） | `sub_42D830`（`!this[114201] || !sub_AF6FB0() || this[114202]` @`0x42d84b`） |
| scene_transition destination 映射 | `sub_433770`（`switch(v5)` case4→1/6→3/8→2/17→4/19→5/21→6/default→0；case13 不发送） |
