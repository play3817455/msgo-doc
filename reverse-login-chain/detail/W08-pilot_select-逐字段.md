# W08 · 0xF705→0x063E 选机师：请求 17B 与应答 51725B 顶层逐字段

> 工作项：`W08`（P1）｜ 判据：**0xF705 全 17B 逐字段 + 0x063E 顶层 17 段逐字段（含 is_processing_comeback 等门控字段的客户端用途）**
> 目标文件：`GundamOnline_CHINA_v15.exe`（基址 `0x400000`，已脱壳）
> 方法：IDA Pro MCP 本轮**重取**（`sub_B8A8B0` 发送函数 / `sub_AFE850` 包装 / `sub_437040` 业务回调 / `sub_43ADD0` FSM / `sub_450E10` 门控升级 / `sub_42A610` tuto 处理器 / `sub_A1E880` / `sub_436180`）＋ case 体反汇编（`0xB53A20..0xB53DD4` 字段读取/回调实参序）
> 日期：2026-09-15 ｜ 上游 `nodes/07`（N7）＋ `formats/全链报文总表.md` §2.2 L6 ＋ `server/internal/protocol/lounge.go` + `server/internal/authsrv/server.go`
> 标注：✅ 本轮反编译/反汇编直接确认 ｜ ★ 本轮新增/修正 ｜ ⚠️ 仍未定

---

## 0. 一句话结论

`0xF705`（17B 请求体）= `troops u32 | pilot_id u32 | is_tutorial_skip u8 | dbg_comeback_disable u32(恒0) | channeling_type u32`；`0x063E`（应答，**最小 51725B**）= 17 段顶层字段，其中 **`is_processing_comeback`（第 9 段，u8）是唯一门控字段**：非 0 ⇒ 回调 `sub_437040` 写 `app+0x1BDAC = 1` ⇒ 稍后 `sub_450E10` 把它升成 **2** ⇒ FSM `sub_43ADD0` `case 0x14` 才调 `sub_442970`（**开大厅/主菜单窗口**）；恒 0 ⇒ `app+0x1BDAC` 恒 0 ⇒ **窗口永不开 ⇒ 白屏**。回调末尾还会 `app+1400 |= 2`（首屏门位 bit1）推进下一格。**其余 15 段字段全非门控**（尤其 `restore_channel` 在回调里根本没被使用 ⚠️）。

---

## 1. 汇编逻辑

### 1.1 调用链（发送 + 接收两侧全通）

```
【发送 0xF705】
sub_43ADD0 case7 @0x43AED4（30002 首屏第 1 格，也是 30001 选机师点击路径）
   ├─ troops        = [app+0x6F108]        （当前选中势力）
   ├─ pilot_id      = [app+0x6F0FC]        （选中机师 ID）
   ├─ is_tutorial_skip = [app+0x1BE22] != 0
   ├─ channeling_type  = sub_A1E880() == dword_1104680（0..3）
   └→ sub_AFE850(troops, pilot_id, is_tutorial_skip, 0, channeling_type)
        └→ sub_B8A8B0(this, troops, pilot_id, is_tutorial_skip, /*dbg=*/0, channeling_type)
             └ 写体：*(u16*)buf=0xF705; +4B troops; +4B pilot_id; +1B is_tutorial_skip(u8); +4B dbg(u32); +4B channeling_type(u32)

【接收 0x063E】
sub_B51930 case loc_B53684（cmp eax,63Eh; jz @0xB51A15 ✓，n=0x16，alloc(0xDB85)=56201）
   → 17 段字段读入结果结构（日志 @0xB53A3B..0xB53CF0 印证序）
   → vt[0x94](this, result, restore_channel, charge_point, tuto_step, tuto_flags[0], tuto_flags[1],
              tuto_missionid, pilot_detail*, is_netcafe, is_processing_comeback, vip_lv, overplay_type,
              accum_playtime, daily_compcnt, ncafe_compcnt, heroms_term, flag_wideuse, level_point)
        = sub_AF7790 → sub_437040(app=dword_11E3EA8, …)
```

### 1.2 关键函数表

| 地址 | 身份 | 作用 |
|---|---|---|
| `sub_B8A8B0` | `send_pilot_select` | 写 0xF705 17B（日志串 `)<-_proto_lounge_client::send_pilot_select(` @`0xEEA3D0`） |
| `sub_AFE850` | case7 发送包装 | `sub_B8A8B0(v5,a1,a2,a3,0,a5)`——**dbg_comeback_disable 硬编码 0** |
| `sub_42ECA0` | 选机师页按钮驱动 | 另一处调 `sub_AFE850`，is_tutorial_skip=`(app+114210!=0)` |
| `sub_437040` | ★0x063E 业务回调 | 17 段字段消费 + 门控写 `app+0x1BDAC` |
| `sub_AF7790` | `sub_437040` 的 vt 包装 | `sub_437040(dword_11E3EA8, a1..a18)` |
| `sub_450E10` | 频道登录/lobby 进入回调 | ★把 `app+0x1BDAC` 从 1 升成 2（`0x450FAD/FB7`） |
| `sub_43ADD0` | 频道登录每帧 FSM | case7 发 / case0x14(20) 门控判 |
| `sub_42A610` | tuto 处理器 | 存 `app+114164/172/176/180`，清 `app+114207` |
| `sub_A1E880` | channeling_type 取用 | `return dword_1104680` |
| `sub_436180` | heroms_term 串处理器 | `sub_BC4110` 解码 + `sub_4029E0` |

### 1.3 数据结构偏移（app 对象 = `dword_11E3EA8`）

| 偏移 | 字段 | 谁写/读 |
|---|---|---|
| `+0x6F108` | 当前选中 troops | case7 读 → 0xF705.troops |
| `+0x6F0FC` | 当前选中 pilot_id | case7 读 → 0xF705.pilot_id |
| `+0x1BE22`(114210) | is_tutorial_skip 源 | case7 读 |
| `+0x1BDAC`(114092) | ★is_processing_comeback 落点（0/1/2） | `sub_437040` 写1 / `sub_450E10` 升2 / `sub_43ADD0` case20 读 |
| `+0x1BD88`(114040) | accum_playtime（float） | `sub_437040` 写 |
| `+0x1BD8C`(114044) | overplay_type（dword） | `sub_437040` 写 |
| `+0x1400`(0x578) | ★首屏门位位图 | `sub_437040` `|=2`（bit1） |
| `+114203` | case0x11 标志 | `sub_437040` 写 1 |
| `+455166` | vip_lv（byte） | `sub_437040` 写 |
| `+416092` | is_netcafe（byte） | `sub_437040` 写 |
| `+455248` | flag_wideuse（byte） | `sub_437040` 写 |
| `+454968` | level_point（dword） | `sub_437040` 写 |

---

## 2. 状态机（选机师 → 进频道）

| 步骤 | 动作 | 关键证据 |
|---|---|---|
| 1 | 30001 上 `0xF705`（选机师）→ 服务端回 `0x063E`(≥51725B) | `sub_B8A8B0` / case `0xB53684` |
| 2 | `0x063E` 解析成功 ⇒ `sub_437040` 置 `app+1400|=2`（bit1）+ `app+0x1BDAC`(按 come_back) | `sub_437040` |
| 3 | 30002 首屏 `sub_43ADD0`：case7 再发 `0xF705` → case8 等 `app+1400&2` | `@0x43AF1B` |
| 4 | 后续频道登录回执（`sub_450E10`）把 `app+0x1BDAC` 1→2 | `0x450FAD/FB7` |
| 5 | `sub_43ADD0` case0x14：`app+0x1BDAC==2` ⇒ `sub_442970`（开大厅窗口） | `@0x43B0B6` |

> ★ 30001 与 30002 都会发 `0xF705`（case7 是 30002 首屏第 1 格；30001 上则是选机师点击）。两条都需回 `0x063E`。

---

## 3. 报文逐字段表（★核心交付）

> 通道 = `:30001`(lounge) 与 `:30002`(channel) 共用。u32=`sub_B02DD0`、u8=`sub_B06230`、有界串=`sub_B02BA0`。**线偏移**从报文体第 0 字节（不含 2B ID）起算。每 case 末尾 `游标 == 报文尾`，否则整包丢弃。

### 3.1 `0xF705` 请求（C→S，体 17B）

发送函数 `sub_B8A8B0`，写入序列逐条证据：

| 线偏移 | 类型 | 长度 | 字段 | 取值域 / 来源 | 证据 |
|---|---|---|---|---|---|
| 0 | u16 | 2 | ID | `0xF705`（写 `-2299`） | `sub_B8A8B0` `*(WORD*)v8=-2299` |
| 2 | u32 | 4 | `troops` | ★线上 **0 基**（0=秩序/1=抵抗）；来源 `[app+0x6F108]` | case7 `mov eax,[esi+6F108h]` |
| 6 | u32 | 4 | `pilot_id` | 选中机师 ID；来源 `[app+0x6F0FC]` | case7 `mov edx,[esi+6F0FCh]` |
| 10 | u8 | 1 | `is_tutorial_skip` | 0/1；来源 `[app+0x1BE22]!=0` | `sub_B061C0(&a4,v30)`（u8 写）+ case7 `setnz cl` |
| 11 | u32 | 4 | `dbg_comeback_disable` | ★**恒 0**（调试开关，两处调用点都硬编码 0） | `sub_AFE850` `sub_B8A8B0(v5,a1,a2,a3,0,a5)` |
| 15 | u32 | 4 | `channeling_type` | 0..3；来源 `sub_A1E880()==dword_1104680` | `sub_A1E880` `return dword_1104680` |

- 体长 = 4+4+1+4+4 = **17B**；发送缓冲 alloc 22B（2B ID + 17B 体 + 3B 冗余）。
- 日志串序（`sub_B8A8B0` 内）：`troops=`/`pilot_id=`/`is_tutorial_skip=`/`dbg_comeback_disable=`/`channeling_type=` ✓ 与写入序一致。

### 3.2 `0x063E` 应答（S→C，最小 51725B）—— 17 段顶层字段

字段名 = 日志串（`sub_B51930` case 内），读取序/类型由反汇编 `0xB53A20..0xB53DD4` 逐条坐实；客户端用途 = `sub_437040` 回调。

| # | 线偏移 | 类型 | 字段 | 客户端用途（sub_437040） | 取值域 / 必须非零 | 证据 |
|---|---|---|---|---|---|---|
| 1 | 0 | u32 | `result` | `if(a2>=0)` 才继续；`==0` 调 `sub_A2CCD0()`；`==1` 额外 `sub_5FAC70`+`sub_6574C0×2`+`sub_657860` | **必须 ≥0（0=成功）** | 日志 `@0xB53A3B`；回调 `@0x43713D` |
| 2 | 4 | u32 | `restore_channel` | ⚠️**回调内未使用**（`a3` 全文零引用） | 0 即可（服务端为保险回 1，见 §6） | 日志 `@0xB53A65`；反编译无 `a3` |
| 3 | 8 | u32 | `charge_point` | `*(dword_11E3EA4+36)=a4` | 充值点 | 日志 `@0xB53A92` |
| 4 | 12 | u32 | `tuto_step` | `sub_42A610` → `app+114164`；并清 `app+114207`（"不发 0x3E0B"门） | 0=无教程 | 日志 `@0xB53ABF` |
| 5 | 16 | u32×2 | `tuto_flags[0..1]` | `sub_42A610` → `app+114176/114180` | 0 | 日志 `@0xB53AE9`（`sub_B08500` 打印 2 个 u32） |
| 6 | 24 | u32 | `tuto_missionid` | `sub_42A610` → `app+114172` | 0 | 日志 `@0xB53B16` |
| 7 | 28 | 51672 | ★`pilot_detail` | 指针；`sub_437040` 提取 20+ 子字段（money@+4、deckcost@+24、second_chance_free@+2584、hav_* 各段、cshist@+2328、heroms_grants@+55460…） | 全 0 亦可过解析，但业务靠它（`[0]=pilot_id` 让大厅认"我是谁"）；**内容归 W09** | 日志 `@0xB53B41`（`sub_B48010`） |
| 8 | 51700 | u8 | `is_netcafe` | `*(app+416092)=a10!=0`；且 `if(a10) sub_6571F0(a16) else sub_6571F0(0)`（决定 ncafe_compcnt 是否生效） | 0/1（网吧标志） | 日志 `@0xB53B6B`（`sub_B0C1F0`） |
| 9 | 51701 | u8 | ★`is_processing_comeback` | ★**`*(app+0x1BDAC)=a11!=0`（唯一门控）** | ★**必须 1**（0 ⇒ 白屏） | 日志 `@0xB53B95`；`sub_437040` `@0x437429` |
| 10 | 51702 | u32 | `vip_lv` | `*(app+455166)=a12`（按 byte 存） | 0 | 日志 `@0xB53BC1`（`sub_B03580`=u32） |
| 11 | 51706 | u8 | `overplay_type` | `*(app+0x1BD8C)=a13`（按 dword 存） | 0 | 日志 `@0xB53BE9`（`sub_B0C1F0`） |
| 12 | 51707 | u32 | `accum_playtime` | `*(float*)(app+0x1BD88)=(float)a14` | 累计游戏时长（秒，存 float） | 日志 `@0xB53C15` |
| 13 | 51711 | u32 | `daily_compcnt` | `sub_6571F0(a15)` | 0 | 日志 `@0xB53C3F` |
| 14 | 51715 | u32 | `ncafe_compcnt` | `if(is_netcafe) sub_6571F0(a16) else sub_6571F0(0)` | 0 | 日志 `@0xB53C69` |
| 15 | 51719 | NUL 串 | `heroms_term` | `sub_436180(串)`（解码处理） | ★**必须 NUL 结尾、上限 65**；空串写一个 `\0` | 日志 `@0xB53C96` |
| 16 | ++ | u8 | `flag_wideuse` | `*(app+455248)=a18`；bit0x20 ⇒ `*(dword_11E3F34+222)` | 0 | 日志 `@0xB53CC9` |
| 17 | ++ | u32 | `level_point` | `*(app+454968)=a19` | 0 | 日志 `@0xB53CF0` |

- **最小体长**（heroms_term 空串）：`28 + 51672 + 1+1+4+1+4+4+4 + 1 + 1 + 4 = 51725B`。
- 回调实参序（`0xB53D3C..0xB53DD2` 反汇编逐条）与上表 **完全一致** ✓（result→restore_channel→charge_point→tuto_step→tuto_flags[0/1]→tuto_missionid→pilot_detail→is_netcafe→is_processing_comeback→vip_lv→overplay_type→accum_playtime→daily_compcnt→ncafe_compcnt→heroms_term→flag_wideuse→level_point）。
- 回调尾部副作用（★推进关键）：`*(app+1400) |= 2`（首屏门位 bit1，case8 继续）、`*(app+114203) = 1`。

### 3.3 ★★ `is_processing_comeback` 门控链（完整证据）

```
① sub_437040 @0x437429        *(DWORD*)(app+0x1BDAC) = is_processing_comeback != 0   // 0x063E 回调写 1
② sub_450E10 @0x450FAD/FB7    if (*(DWORD*)(app+0x1BDAC)) *(DWORD*)(app+0x1BDAC) = 2 // 频道登录回执升 2
③ sub_43ADD0 case20 @0x43B0B6 mov eax,[app+0x1BDAC]; test; jz → 跳过开窗口
                              cmp eax,2; jnz → sub_43F7F0(); jnz 命中 → sub_442970(app)  // ★开大厅窗口
```

- 证据：`find_bytes "AC BD 01 00"`（=0x1BDAC LE）命中 **36 处**，与本链相关的恰为 `0x43742B`（写1）、`0x450FAF/0x450FB7`（读/写2）、`0x43B0B8`（case20 读）。
- `app+0x1BDAC` 三态：**0**（未处理回归/无回归奖励）→ **1**（0x063E 回调置位）→ **2**（频道登录回执升级）。
- case20（`0x43B0B6`）判 `==2` 才 `sub_442970`；`==0` 直接 `jz loc_43B0E1`（state=21，**不开窗口**）。

---

## 4. 期望服务端回包（造包铁律）

1. **体 ≥ 51725B**，且 `heroms_term` 必须 NUL 结尾（空串 = 单字节 `0x00`）。
2. **`result = 0`**（<0 ⇒ 回调整体跳过）。
3. **`is_processing_comeback = 1`**（★唯一门控，0 ⇒ 白屏）。
4. **`pilot_detail[0..3] = pilot_id`（小端）** —— 大厅认"我是谁"（其余 51668B 可零填，内容归 W09）。
5. `restore_channel` 回调内未用；为保险服务端回 `1`（≠0），但不影响门控（门控只看 is_processing_comeback）。
6. 其余字段（charge_point/tuto_*/is_netcafe/vip_lv/overplay_type/accum_playtime/daily_compcnt/ncafe_compcnt/flag_wideuse/level_point）**回 0 即可**。
7. ★**多帧连发**：51725B 超单帧上限 16366B，服务端须自动切帧（已实现 `wrap_stream`）。

---

## 5. 待研究 / 未定

1. ⚠️ `restore_channel`（a3）在 `sub_437040` 内**全文零引用** —— 是解析后不被消费的"死字段"，还是被别的代码读结果结构？本轮未追其它读者（服务端按 1 下发不影响）。
2. ⚠️ `sub_450E10`（把 app+0x1BDAC 1→2 的那条回执）的**报文 ID 未最终坐实**：它经 vt 槽 `@0xEEDD1C`（`_proto_lounge_client` vtable 基 `0xEEDB6C` + 0x1B0 = 槽 108）派发，签名 `(result, ?, host, port, ?, otp)` 与 `0xFB85` 高度相似，但 `sub_43BC70`（已知 0xFB85 回调）写的是 `app+1168/1340/1297`，而 `sub_450E10` 写 `app+115060/115232/115189` —— **两者是不同回调**，归属待确认。
3. ⚠️ `vip_lv`（u32）在回调里被按 **byte** 存到 `app+455166`（`*(_BYTE*)...=a12`），`overplay_type`（u8）反而按 **dword** 存 `app+0x1BD8C` —— 线类型（u32/u8）已由日志坐实，但客户端内部结构这两字段的槽宽与线类型**不严格一致**（仅记录，不影响造包）。
4. ⚠️ `is_processing_comeback=0` 是否**必然**白屏：静态链已明确（0 ⇒ case20 跳过 `sub_442970`），但 `sub_450E10` 内还有一处 `if((app+114268&2)==0) sub_442970()` 的**旁路开窗**路径，是否兜底尚未真机验证。服务端已按 `=1` 下发（安全侧）。
5. ✅（已由 W09 承接）`pilot_detail` 51672B 内部逐字段，本项只给顶层指针与 20+ 子字段的提取点。

---

## 6. 对服务端落地的影响

- ★ **服务端已全部实现且字段序正确**：`server/internal/protocol/lounge.go` 的 `PilotSelect`(0xF705) / `PilotSelectR`(0x063E) 与本文 §3.1/§3.2 **逐字段一致**（含 `IsProcessingComeback: 1`、`restore_channel` 兜底 1、`pilot_detail[0]=pilot_id`）。
- ★ **本轮为服务端已有注释补上完整证据链**（`server.go` 第 1098~1112 行的"白屏根因"注释与本轮 `sub_437040`/`sub_450E10`/`sub_43ADD0` 三处地址证据**完全吻合**）：
  - `sub_437040 @0x437429` 写 `app+0x1BDAC = (comeback!=0)` ✓
  - `sub_450E10 @0x450FB7` 全二进制唯一写 `2` 的地方 ✓
  - `sub_43ADD0 case20` `app+0x1BDAC==2 ⇒ sub_442970` ✓
- ★ **纠偏一处注释表述**：`server.go` 第 1070 行把 `restore_channel` 说成"决定 app+0x1BDAC 的模式"，措辞易误导 —— 真正写 `app+0x1BDAC` 的是 **`is_processing_comeback`（a11）**，`restore_channel`（a3）根本不参与门控（第 1111 行也已自证"试过 restore_channel=1 无效"）。建议注释措辞改为"门控字段 = is_processing_comeback"。
- ★ **`dbg_comeback_disable` 恒 0**：这是客户端请求里的调试位，服务端无需处理，但解析器要正确跳过它（17B 体里它是 u32，不是 u8）。
- ★ **判定口径**：客户端 `0x063E` 解析失败会走 `vt[0x64](0x16,1)` 显式上报（`nodes/09 §3.7`），且 `app+1400` 的 bit1 不会置位 ⇒ 看"是否出现 `0x7CCB`（case8）"即可判定本条是否被接受。

---

## 7. 证据地址清单

| 结论 | 证据 |
|---|---|
| 0xF705 发送体 17B（5 字段） | `sub_B8A8B0`（`*(WORD*)v8=-2299` + `+2/6` u32 + `sub_B061C0` u8 + `sub_B02D80` u32×2） |
| 0xF705 字段来源 | `sub_43ADD0` case7 `@0x43AED4`（troops=`[esi+6F108h]`、pilot_id=`[esi+6F0FCh]`、skip=`[eax+1BE22h]`、ch=`sub_A1E880()`） |
| 0x063E case + alloc | `sub_B51930` `cmp eax,63Eh; jz @0xB51A15`；`alloc(0xDB85)=56201` |
| 17 段字段序/类型 | 日志区 `0xB53A3B..0xB53CF0`（u32=`sub_B03580`/u8=`sub_B0C1F0`/str=`sub_B41D990` 引号） |
| 回调实参序 | `0xB53D3C..0xB53DD2`（`mov edx,[edx+94h]; call edx` = vt[0x94]） |
| 回调身份 | `sub_AF7790` → `sub_437040(dword_11E3EA8, …)` |
| is_processing_comeback 门控 | `sub_437040 @0x437429` / `sub_450E10 @0x450FAD/FB7` / `sub_43ADD0 case20 @0x43B0B6`；`find_bytes "AC BD 01 00"` 36 命中 |
| restore_channel 未使用 | `sub_437040` 全文 `a3` 零引用 |
| tuto 四字段用途 | `sub_42A610`（存 `app+114164/172/176/180`，清 `app+114207`） |
| heroms_term 处理 | `sub_436180`（`sub_BC4110` 解码 + `sub_4029E0`） |
