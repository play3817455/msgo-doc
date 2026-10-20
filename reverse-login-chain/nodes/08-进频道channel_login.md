# N8 · 进频道 channel_login（30001 → 30002）

> 状态：`completed`　｜　完成时间：`2026-09-14T08:00`　｜　负责任务：`automation/prompts/node-08.md`
> 结论来源：IDA Pro 静态分析（IDB `unpacked\GundamOnline_CHINA_v15.exe.i64`，VA 基址 0x400000）；
> 动态证据沿用历史实测记录（本次**未**重跑客户端，原因见 §5）。
> ★★ 本节点有**纠正性结论**：`0xFB85` **不是** `channel_login_r`，也不是"被推"的包 —— 它是
> **`recv_channel_list_select_r`**，是客户端 `0x2830 send_channel_list_select` 的**应答**。

---

## 0. 一句话结论

进频道**不是服务端推包**，而是**客户端主动请求两步、服务端各答一步**：

```
① 客户端进"选频道"步骤 ⇒ 自动发 0x3E0B send_channel_list_get（体空，仅 ID）
   服务端必须回 0xF11C recv_channel_list_get_r = u32 count + count×54B 频道条目（count 必须 ≥1）
② 客户端自动选一个频道 ⇒ 发 0x2830 send_channel_list_select（体 = u32 channel_id）
   服务端必须回 0xFB85 recv_channel_list_select_r = result|channel_id|host|port|userid|pilot_id|otp
③ 客户端处理器末尾调 lounge->vt[29] → sub_43BC70：**主动断开 30001**、把 host/port/otp 存进
   app+1168/+1340/+1297、置 app[+1396]=3、注册每帧 tick sub_43ADD0
④ 下一帧 tick case4：sub_AF73E0(app+1168, u16(app+1340)) ⇒ **连 30002**（复用同一会话槽）
   ⇒ 所以历史观测到的"回完 0xFB85 客户端立刻断开"其实是**正确的成功路径**（它就是要切到 30002），
     真正的失败原因在**上游 N7**（0x063E 体 68B 非法 ⇒ 从未真正选中机师）。
```

前置条件（**N7 定案，必须先满足**）：`0x063E` 体 ≥ **51725B**。否则客户端根本走不到第 ① 步。

---

## 1. 汇编逻辑

### 1.1 入口与调用链

```
【客户端侧 · 主动请求】
CGameStateStepUpdateGameModeSelectScene 的步骤函数 sub_A87E50（vtable 0xED0418 段内 slot 0xBC，
                                                    状态字段 = this[1]）
  state0 → sub_43ADA0(app)                     // 0x43ADA0
             ├─ sub_AFE710() → sub_B898B0()    // send_channel_list_get  ★发 0x3E0B（体空，总长 2B）
             ├─ app[349] = -1                  // app+0x574 = app+1396（= 本步骤用的同一状态字段）
             └─ sub_43A350(app, 15, 1.0)       // 主状态 → 15
  state1 → 等 sub_42D6F0(app) == (app[349] == 0)   // 由 0xF11C 的处理器把 app[349] 置 0 ✓
  state2/3 → v5 = sub_4307C0(app, 1)              // 取"推荐频道"（人最多/有空位）
             ├─ 若 v5 == 0 ⇒ sub_439D80(app) = 列表第 1 条的 channel_id（列表空 ⇒ -1 ⇒ 弹错误框 ✗）
             └─ sub_42D6B0(app, channel_id) → sub_AFE730 → sub_B89A30   // ★发 0x2830（体 u32 channel_id）
                （sub_42D6B0 内部：app[349] = 1）
  state4 → 等 sub_42D710(app)（app[349]==21 = 成功）/ sub_42D720（==22 = 失败弹框）
             └─ 成功 ⇒ sub_433670(app, 9)

【服务端侧 · 应答 + 跳转】
lounge 分发器 sub_B51930
  case 0xF11C @0xB864A2 → 解析 → 广播 vt[0x70](=sub_BAAFA0→sub_AF75F0) → sub_43F1D0(app, list, count)
        ⇒ sub_43F1D0 把 app[+1376] 的频道向量重建、**app[+1396] = 0**（解锁 sub_A87E50 state1→2）
  case 0xFB85 @0xB87E8F → 解析 → 广播 vt[0x74](=sub_BAAFC0→sub_AF7610→**sub_43BC70(app, ...)**)
        ⇒ sub_43BC70：sub_AF6FF0() 断开 30001；host→app+1168(≤128)、port→app+1340、
                      otp→app+1297(≤40)；sub_43A350(app,4,1.0)；app[+1404]=1；**app[+1396]=3**；
                      在 app+1376 向量里按 channel_id 定位条目 → app+1388/app+1392；
                      **注册 tick sub_43ADD0（app+1348）**

【客户端侧 · 主状态机 tick = sub_43ADD0（app[+1396] = 状态，取值 2..21）】
  case3 → sub_AF7030() 就绪 ⇒ 状态 4
  case4 → **sub_AF73E0(app+1168, *(u16*)(app+1340))** ⇒ ★连 30002；成功 ⇒ 状态 5
  case5 → sub_AF6FB0() 就绪 → sub_A2A180()/sub_AF6E50() → **sub_BAAF60(v7, app+1297)** 校验 OTP ⇒ 状态 6
  case6 → app[114201]=1；状态 7；sub_43A350(app,13,0)
  case7..21 → 大厅/游戏初始化（7 之后与 N9 相关）
  ⇒ 最终状态 21 ⇒ sub_A87E50 state4 认为"成功" ⇒ sub_433670(app, 9)
```

### 1.2 关键函数表

| 地址 | 身份 | 作用 | 关键点 |
|---|---|---|---|
| `sub_B51930` | lounge 协议分发器 | 二叉搜索所有 recv case | `cmp eax,0FB85h; jg loc_B88246; jz loc_B87E8F` @`0xB878B0/B5/BB` |
| `sub_B87E8F` | **`0xFB85` case 体** | 解析 7 字段 + 广播 vt[29] | `push 7`(n=7)、`vt[0x78](0xBE)`=alloc **190** |
| `sub_B864A2` | **`0xF11C` case 体** | 解析频道列表 + 广播 vt[0x70] | `push 5`(n=5)、`vt[0x78](0x784)`=alloc **1924** |
| `sub_B420E0` | ★频道条目读取器 | 逐字段读 **54B** 线格式 | `u32+37B+3×u8+5×u16`（见 §3.2） |
| `sub_B474B0` | 频道条目日志器 | 字段名来源 | `channelid/name/type/pilotlv_min/pilotlv_max/user_num_eff/user_num_zeon/user_max/user_conn/user_comeback` |
| `sub_B41230` | 数组定位器 | `out[0]=dst; out[1]=count; dst += 60*count` | ⇒ 内存步长 **60**，alloc 1924 = 4+32×60 ✓ |
| `sub_B898B0` | `send_channel_list_get` | `*(u16*)buf = 15883` = **0x3E0B**，总长 2 | 由 sub_A87E50 state0 驱动 |
| `sub_B89A30` | `send_channel_list_select` | `*(u16*)buf = 10288` = **0x2830**，体 `u32 channel_id`，总长 6 | 由 sub_A87E50 state2/3 驱动 |
| `sub_AFE710` / `sub_AFE730` | vt[?] 包装 | → 上面两个 send | 唯一调用者 `sub_43ADA0` / `sub_42D6B0` |
| `sub_A87E50` | ★步骤函数 | 频道列表→选频道→等结果 | `CGameStateStepUpdateGameModeSelectScene`（vtable 0xED0418，slot 0xBC） |
| `sub_4307C0` | 推荐频道选择器 | 遍历 app+1376 向量，取 `(i16)(e+44)-(i16)(e+42)` 最大者 | 单条列表 ⇒ 直接返回该条；>1 条且无空位 ⇒ 返回 0 |
| `sub_439D80` | 列表首条取用 | `*(u32*)(app+1376)`；空 ⇒ −1 | count=0 会走到这里 ⇒ 弹框 ✗ |
| `sub_42D6F0/710/720` | 状态谓词 | `app[349]==0 / ==21 / ==22` | = 频道列表已到 / 进大厅成功 / 失败 |
| `sub_43ADA0` | 请求频道列表 | send 0x3E0B + `app[349]=-1` + 主状态 15 | — |
| `sub_42D6B0` | 请求选频道 | `app[349]∉{0,≥21}` 时返回 0（防重入）；否则 send 0x2830 + `app[349]=1` | — |
| `sub_43F1D0` | ★`0xF11C` 业务处理 | 重建 app+1376 频道向量；**app[349]=0** | 用 `a2+41` 起、步长 **60** 遍历解析缓冲 |
| `sub_43BC70` | ★跳转开关 | 断 30001、存 host/port/otp、`app[1396]=3`、注册 tick | `a2 = result`：**必须 ≥0**，否则 `app[1396]=22`（失败） |
| `sub_AF7610` | vt[29] 直达 | `sub_43BC70(dword_11E3EA8, a1..a7)` | 证实操作对象 = **app 对象** |
| `sub_AF6FF0` | 断开当前连接 | 操作 `dword_1201A60+33640` 的会话对象 | 断的是 **30001** |
| `sub_AF73E0` | 连 30001/30002 的包装 | `(host, port)` → `sub_AF7130` → holder `dword_1201A60+0x20B0` | ⇒ 30001/30002 **复用同一会话槽** |
| `sub_43ADD0` | ★频道登录 tick | `app[1396]` 2..21 状态机 | case4 = 连 30002；case5 = OTP 校验；case21 = 完成 |
| `sub_437040` | `0x063E` 业务回调 | 把 `pilot_detail` 全部字段装进 app | 偏移 `a9+4/+16/+24/+36/+184/+312/+376/+1656/+1720/+2328/+2592/+55460/+55504/+55516/+55536/+55544/+55582/+55606/+55624(0x1C8)` ⇒ **与 N7 §3.2 逐段吻合**（反证 N7 的 51725B 结论 ✓） |

### 1.3 数据结构

| 对象/结构 | 偏移 | 类型 | 含义 |
|---|---|---|---|
| app | `+1168` | char[129] | 频道服 host（sub_43BC70 写入，sub_AF73E0 取用） |
| app | `+1340` | u32 | 频道服 port（**低 16 位**被 sub_AF73E0 取用） |
| app | `+1297` | char[41] | 频道服 OTP（sub_43BC70 写入，sub_BAAF60 校验） |
| app | `+1396` | u32 | **频道登录状态**（= `this[349]`；被两个 FSM 共用，见 §2） |
| app | `+1348` | fnptr | 每帧 tick（= `sub_43ADD0`） |
| app | `+1344` | fnptr | `sub_42F580` |
| app | `+1376` / `+1380` | ptr/ptr | 频道向量 begin/end，**元素 48B**，`[0]` = channel_id |
| app | `+1388` / `+1392` | ptr/u32 | sub_43BC70 定位到的频道条目指针 / 其 `[+32]` 值 |
| app | `+1400` | u32 | 步骤位图（bit1/bit2… 由各 init 步骤置位） |
| app | `+1404` | u8 | "等待"标志 |
| app | `+114201` | u8 | 大厅就绪标志（sub_43ADD0 case6 置 1） |
| app | `+114207` | u8 | sub_A87E50 state0 的门（置位则**不**发 0x3E0B） |
| app | `+310616` | u32 | state1 时清零 |

---

## 2. 状态机

### 2.1 `CGameStateStepUpdateGameModeSelectScene::step` = `sub_A87E50`（状态 = `this[1]`）

| 状态 | 动作 | 迁移条件 |
|---|---|---|
| 0 | `sub_43ADA0(app)`（发 **0x3E0B**） | 若 `app[114207]≠0` ⇒ 原地返回；否则 +1 |
| 1 | 等频道列表 | `app[1396]==0`（由 `sub_43F1D0` 置）⇒ `this[5]=1`、+1 |
| 2 | `sub_4307C0(app,1)` 取推荐频道 ⇒ `this[6]=channel_id` ⇒ `sub_42D6B0`（发 **0x2830**） | 失败（返回 0）⇒ `sub_439D80` 兜底；再失败 ⇒ state=200 + 弹框 `1006666251` |
| 3 | 同上（重入点） | — |
| 4 | 等选频道结果 | `app[1396]==21`（成功）⇒ `sub_433670(app,9)`、state=−1；`==22` ⇒ state=200 + 弹框 `1006666250` |
| 100~104 | 关闭/重开 UI 的过渡态 | `app[114205/114206]` 等标志 |
| 200/201 | 错误处理 | 回 state 1 重试 |

### 2.2 app 级"频道登录"状态机 = `sub_43ADD0`（状态 = `app[+1396]`）

| 状态 | 动作 / 迁移 |
|---|---|
| 2 | `sub_AF7030()` ⇒ 断链 + `app[1404]=1` + `sub_43A350(app,4,1.0)` ⇒ **3** |
| 3 | `sub_AF7030()` 就绪 ⇒ **4**（由 `sub_43BC70` 直接置 3 进入） |
| **4** | **`sub_AF73E0(host=app+1168, port=u16(app+1340))` ⇒ 连 30002** ⇒ 成功 ⇒ **5** |
| 5 | `sub_AF6FB0()` 就绪 ⇒ `sub_BAAF60(otp)` 校验 `app+1297` ⇒ **6** |
| 6 | `app[114201]=1`、`app[1404]=0`、`sub_43A350(app,13,0)` ⇒ **7** |
| 7 | `sub_AFE850(...)` ⇒ **8** |
| 8 / 0xE / 9 / 0xA / 0xB / 0xC / 0xD | 各初始化步骤 ⇒ 14 / 9 / 10 / 11 / 12 / 13 / 15 |
| 0xF / 0x10 / 0x11 / 0x12 / 0x13 | ⇒ 16 / 17 / 18 / 19 / 20 |
| 0x14 | ⇒ **21**（`sub_442970()` 或 `sub_43F7F0()` 就绪） |
| **0x15(=21)** | `sub_438D10(app,13)`、`app[1348]=0`（tick 注销）⇒ **进大厅完成** |
| （失败） | `sub_43BC70` 收到 `result<0` ⇒ `app[1396]=22` + `sub_431790(23, result)` |

```
        ┌────────────── 0xFB85 到达（result≥0）──────────────┐
        ▼                                                    │
  [1396]=3 ──tick4: sub_AF73E0(host,port)──► 连 30002 ──► 5 ──OTP──► 6 ──► 7 .. 20 ──► 21 ──► 进大厅
        │                                                             │
        └──── result<0 ⇒ [1396]=22 ⇒ sub_A87E50 state4 判定失败 ───────┘
```

---

## 3. 文件与格式

### 3.1 本地文件

本节点不新增本地文件格式（沿用 N1/N3 的 `sysinfo.ini` / 会话层）。

### 3.2 网络报文（★逐字段，造包用）

#### (a) 请求 `0x3E0B` `send_channel_list_get`（`sub_B898B0`）
```
u16 0x3E0B                     // 只有 ID，**无体**（函数里的长度参数 = 2）
```

#### (b) 应答 `0xF11C` `recv_channel_list_get_r`（case `0xB864A2`，n=5，alloc 0x784=1924）
```
u32 count                      // ≤ 0x20(32)；>32 ⇒ error(5,1) 整条丢弃 ✗；★必须 ≥1
count × 频道条目（**线 54B**，内存步长 60B）：
  +0   4   u32  channelid
  +4   37  B    name        ★定长 37B（无 NUL 检查；建议 NUL 收尾，UTF-8）
  +41  1   u8   type
  +42  1   u8   pilotlv_min
  +43  1   u8   pilotlv_max
  +44  2   u16  user_num_eff
  +46  2   u16  user_num_zeon
  +48  2   u16  user_max
  +50  2   u16  user_conn
  +52  2   u16  user_comeback
--------------------------------------------------------
线长 = 4 + 54×count ；读完 **游标必须恰到底**（`0xB8656B`）
内存自洽：alloc(1924) = 4 + 32×60 ✓（60 = sub_B41230 的步长）
```
> 选频道逻辑（`sub_4307C0`）：`count>1` 时取 `(i16)user_num_eff − (i16)pilotlv_min` **最大且 >0** 的那条；
> 全都不 >0 ⇒ 返回 0 ⇒ 走 `sub_439D80`（列表第 1 条）。
> ⇒ **造包最省事：只发 1 条**（单条时 `sub_4307C0` 无条件返回它）。

#### (c) 请求 `0x2830` `send_channel_list_select`（`sub_B89A30`）
```
u16 0x2830 + u32 channel_id     // 4B 体，总长 6B
```

#### (d) ★应答 `0xFB85` `recv_channel_list_select_r`（case `0xB87E8F`，n=7，alloc 0xBE=190）
```
u32 result        // ★必须 ≥ 0（sub_43BC70 的 `if(a2>=0)`）；负数 ⇒ app[1396]=22 失败 ✗
u32 channel_id    // 回显客户端请求里的 channel_id（sub_43BC70 用它查 app+1376 向量）
str host          // sub_B02BA0 有界串：**NUL 结尾**，上限 0x81=129（含 NUL）⇒ ≤128 字符
u32 port          // 频道服端口（本例 30002）
u32 userid
u32 pilot_id
str otp           // 有界串：NUL 结尾，上限 0x29=41（含 NUL）⇒ ≤40 字符；可给空串（仅 1 个 NUL）
--------------------------------------------------------
alloc 自洽：190 = 4 + 4 + 129 + 4 + 4 + 4 + 41 ✓（**精确相等**）
读完游标必须恰到底（`0xB88002` `cmp ebx,[var_2C40]; jz loc_B88021`）
⇒ 空 host/otp 时最小体 = 4+4+1+4+4+4+1 = 22B
```

> **两个字符串都是"有界变长串"（`sub_B02BA0`）**：在 `min(上限, 剩余)` 内 `memchr(NUL)`；
> 找不到 NUL ⇒ 失败；游标停在 NUL **之后**。**不要**用定长 129/41 去填零 ✗（游标会 ≠ 尾 ⇒ 整条丢弃）。

---

## 4. 实测证据 / 判定表

### 4.1 ★判定表（本节点核心交付）

| 问题 | 结论 | 代码证据 |
|---|---|---|
| `0xFB85` 是"被推"还是"被应答"？ | **被应答**（应答 `0x2830`） | ① 全二进制 `0FB85h` 只出现 2 处，其中唯一相关的是分发器 `cmp eax,0FB85h` @`0xB878B0`（**没有任何写 ID 0xFB85 的 send 函数**）⇒ 客户端不可能自己发它；② 客户端**确实**发 `0x2830`（`sub_B89A30` `*(_WORD*)buf=10288`，由 `sub_A87E50` state2/3 自动驱动）；③ 该 case 的日志串是 `recv_channel_list_select_r`（@0xEE55E8 → 引用点 0xB88045，落在 case 体内） |
| `0xFB85` 的真名 | **`recv_channel_list_select_r`** | 同上 ③ ⇒ 既有文档里的 `channel_login_r` 是**臆造名** ✗ |
| 先决请求是什么 | `0x3E0B`（体空）⇒ 答 `0xF11C` | `sub_B898B0` + case `0xB864A2`（`cmp eax,0F11Ch; jz` @0xB86073/BE） |
| 客户端何时/被谁驱动去连 30002 | 收到 `0xFB85` 后：`sub_43BC70` 置 `app[1396]=3` 并注册 tick `sub_43ADD0`；**tick 的 case4** 调 `sub_AF73E0(app+1168, u16(app+1340))` 连 30002 | `sub_43BC70` @0x43BD3F（`*(this+1348)=sub_43ADD0`）+ `sub_43ADD0` case4 @0x43AE48 |
| "回完 0xFB85 客户端立刻断开" 是失败吗 | **不是**。`sub_43BC70` 第一件事就是 `sub_AF6FF0()` **主动断 30001**，随后重连 30002（同一会话槽） | `sub_43BC70` @0x43BC96 |
| 期望序号门控 `sub_B41120(7)` | 默认全开（N7 已证），**不是**拒因 | `sub_B47420` 621 组全置 1 |

> ⚠️ 历史"三种推送时机全被拒"的三条记录，其**实验前提（客户端已选中机师）不成立**
> （N7：`0x063E` 体必须 ≥51725B，旧 68B ⇒ 静默丢弃 ⇒ 业务回调 `sub_437040` 从未执行）。
> 因此那三条否证**不能**用来判断 0xFB85 的正确用法。本次已从静态把机制定死。

### 4.2 服务端改动（`server\access_sticky.py`，已落地）

| 报文 | 新增/修改 | 关键旋钮（env） |
|---|---|---|
| `0x3E0B` → `0xF11C` | 新增 `chn_entry()` / `channel_list_get_r()` + `route_reply` 分支 | `STICKY_CHN_COUNT`(1) / `STICKY_CHN_ID`(1) / `STICKY_CHN_NAME` / `STICKY_CHN_TYPE` / `STICKY_CHN_LVMIN` / `STICKY_CHN_LVMAX`(99) / `STICKY_CHN_USER_EFF` / `STICKY_CHN_USER_ZEON` / `STICKY_CHN_USER_MAX`(100) / `STICKY_CHN_USER_CONN` / `STICKY_CHN_COMEBACK` |
| `0x2830` → `0xFB85` | 新增 `channel_list_select_r()` + `route_reply` 分支（**channel_id 回显请求值**） | `STICKY_CL_RESULT`(0) / `STICKY_CL_HOST`(127.0.0.1) / `STICKY_CL_PORT`(30002) / `STICKY_CL_OTP`(空) / `STICKY_USERID` / `STICKY_PILOT_ID` |
| `0x063E` | **默认体长 68 → 51725**；新增 `STICKY_SELECT_RESULT`(0) 与 `STICKY_SELECT_BODY_HEX` | `STICKY_SELECT_BODY_LEN`(51725) |
| 旧 `channel_login_r()` | 保留为兼容别名（指向新函数），旧"主动推"路径（`STICKY_LOUNGE_PUSH`）**保持关闭** | `STICKY_LOUNGE_PUSH=0` |

`server\启动服务端.bat` 的 FIXED ENV VARS 段已同步写入上述固化值。
**本次已重启应答器使其生效**（监听 30000/30001/30002，日志确认 `p2=echo p1msg=1`）。

### 4.3 一轮复现步骤与判据

```
① 停止/启动服务端（server\停止服务端.bat → server\启动服务端.bat）★必须重启，旧进程不会热加载
② 启动客户端（启动客户端(联调).bat）→ 登录 → 选世界 → 选机师（此时 STICKY_SELECT_BODY_LEN=51725 生效）
③ 观察 server\logs\sticky.log：
   成功判据（按顺序出现）：
     .. [选机师] 回 0x063E 体=51725B
     <<< ... 报文ID=0x3E0B            ← ★新报文：客户端开始请求频道列表
     .. [频道列表] 请求 0x3E0B ⇒ 回 0xF11C 体=58B
     <<< ... 报文ID=0x2830
     .. [选频道] 请求 0x2830 channel_id=1 ⇒ 回 0xFB85 体=31B
     #N .. 客户端关闭                    ← ★这是**正常**的（切到 30002），不是失败
     #M 连接 ('127.0.0.1', 5xxxx)        ← ★30002 上的新连接（本进程同端口三监听）
   失败判据：回完 0x063E 后**再无** 0x3E0B ⇒ 仍是 N7 的体长/字段问题；
             有 0x3E0B 但无 0x2830 ⇒ 0xF11C 体不合规（多半 count=0 或条目长度≠54×n）。
```

---

## 5. 待研究 / 未定

1. ⚠️ **未做客户端实跑验证**（本轮为自动化静态任务，客户端未启动；见 §4.3 可直接复现）。
   这是本节点唯一未闭环项，已作为 N9 的第 0 步。
2. ⚠️ `0xF11C` 条目 `name` 字段的**编码**未实测（静态只能看出"定长 37B、无 NUL 检查"）。
   推断为 UTF-8（与 N2/N6 的其它名字字段一致），若乱码改用 GBK 再试 —— 只影响显示，不影响流程。
3. ⚠️ `type` / `pilotlv_min` / `pilotlv_max` / `user_num_*` 的**取值范围与 UI 呈现**未实测；
   当前发 `type=0, lv 0..99, user_max=100` 属"安全默认"。
4. ⚠️ `sub_4307C0` 的"推荐频道"判据只从反汇编得到（`(i16)(+44)-(i16)(+42)` 最大且 >0）；
   多频道场景下的**客户端自动选择结果**未实测（建议先只发 1 条）。
5. ⚠️ `sub_A87E50` 是被**哪个 vtable slot 调用**（`0xED04D4` 是数据槽，属
   `CGameStateStepUpdateGameModeSelectScene` 段）⇒ 可以确定它是"每帧步骤函数"，
   但"该步骤对象何时被创建/激活"未追（不影响服务端造包）。
6. ⚠️ `app[+1400]` 的步骤位图与 `sub_43ADD0` case7..21 各步（大厅初始化）细节留给 N9。

---

## 6. 对下游节点的影响（★ N9 关键产出）

- **N9 可以从"客户端已能连 30002"开始**：本节点给出了完整的"进入频道服"触发链与服务端最小应答，
  N9 只需回答"30002 连接上之后（握手是否复用 access、首包是什么、回什么进大厅）"。
- **N9 第 0 步（必须先做）**：按 §4.3 跑一轮，确认 `0x3E0B→0xF11C→0x2830→0xFB85→连 30002` 全程出现。
  若 0x3E0B 未出现 ⇒ 回到 N7（0x063E 体/字段）而不是继续做 N9。
- **30002 与 30001 是同一会话槽**（`sub_AF73E0` → holder `dword_1201A60+0x20B0`）⇒ 30002 上
  **同样会走 access 握手 + Camellia 帧**（`sub_AF7130` → `sub_CA9B40`）⇒ **N3 的加密层可直接复用**。
- **OTP 会二次下发**：`0xFB85.otp` 覆盖 `app+1297`（`sub_43BC70`），随后 `sub_43ADD0` case5 用
  `sub_BAAF60` 校验；`0x1146`（N5）下发的那份被覆盖 ⇒ **频道服 OTP 可给空串**（实测过 `0x1146` 空串可行）。
- **风险**：`result<0` 会让客户端弹"频道连接失败"框并回到选频道，不会崩；调试时不要用负数，
  以免把"没反应"误判成协议错。

---

## 附：本次新增/修改的文件

| 文件 | 动作 |
|---|---|
| `server\access_sticky.py` | 新增 `chn_entry` / `channel_list_get_r` / `channel_list_select_r`；新增 `0x3E0B`、`0x2830` 两个 `route_reply` 分支；`STICKY_SELECT_BODY_LEN` 默认 68→**51725**；新增 `STICKY_SELECT_RESULT` / `STICKY_SELECT_BODY_HEX` |
| `server\启动服务端.bat` | FIXED ENV VARS 段同步 N8 固化值（51725 / 频道列表 / 保持 push=0） |
| `reverse-login-chain\formats\README.md` | §2.4 追加 N8 定案（0xF11C / 0xFB85 逐字段） |
| `.codebuddy\memory\topics\09` / `topics\14` / `topics\08` | 追加 N8 结论 |
