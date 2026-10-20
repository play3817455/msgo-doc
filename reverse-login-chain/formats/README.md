# formats · 全链文件与格式总索引

> 本目录/文件汇总"登录链"沿途涉及的所有**文件、报文、资源格式**，供各节点直接引用。
> 格式结论**只有一个真相源**：各节点文档的「文件与格式」节；本文件只做**索引与速查**。
> 冲突时：协议类以 `.codebuddy\memory\topics\08-协议报文总表-已验证.md` 为准。

---

## 一、本地文件

| 文件 | 路径 | 格式 | 涉及节点 |
|---|---|---|---|
| `sysinfo.ini` | `GundamOnline\data\sysinfo.ini`（★客户端只读 data/ 那份） | INI：`[SETTING] Target_Url / Target_port / GAME / GVERSION / SP` | N1 N2 |
| `account.ini` | 游戏目录 | INI：`AUTH,1` / `ID,<账号>` / `ID/PW_SAVE,1` | N1 |
| 注册表 | `HKLM\SOFTWARE\WOW6432Node\9you\GOnline` | `path` / `gamever`(0x181) | N1 |
| `download_list.csv` | 客户端 `settings\`（也在 `unpackdat\settings\`） | UTF-8 无 BOM / CRLF / `#` 注释与表头；77 条表清单 | N6 |
| `autoexec.cfg` / `autoexec_sv.cfg` | 本地 `data\settings\` / 服务端下发 | CSV 脚本方言（UTF-8 无 BOM + CRLF + 尾逗号） | N6 |
| `str_table.txt` | `data\settings\` | UTF-16LE **带 BOM**、`main,sub,id,string,#注释`、CRLF | 全局 |
| `authsv*.csv` | 归档内 `settings_0000.dat`（等长改写） | UTF-8、`#` 注释、`组ID,组名,IP,端口,图标ID` | N2 |

### 一·补（N1 实测，2026-09-14）

- `account.ini`（宽串 `L"account.ini"` @ `0xD681B8`）：**读写走游戏自有 VFS**（`sub_46F2F0/46F080/46E590/46F170/46E240/46F250`），**不使用** Win32 `Get/WritePrivateProfileString`。实测键名（非"段"）：`ID/PW_SAVE`（`0xD681A0`，`"0"/"1"`）、`ID`（`0xD68198`，账号 UTF-8）、`AUTH`（`0xD6818C`，十进制索引）。⚠️ 是否含 `[section]` 待运行时实证。
- `sysinfo.ini` / `Target_Url` / `Target_port` / `SP` / `GAME` / `GVERSION`：**在本 exe（`GundamOnline_CHINA_v15.exe`）宽/窄串扫描 0 命中** ⇒ 该文件很可能属"敢达启动器"或加密资源，**不在客户端主 exe**（⚠️待验证）。
- 注册表 `HKLM\SOFTWARE\WOW6432Node\9you\GOnline`（`path`/`gamever`）：**在本 exe 无 `GOnline`/`SOFTWARE`/`gamever` 明文** ⇒ 疑在启动器侧（⚠️待验证）。本 exe 的 `Reg*` 仅用于 `sub_587C90`（`CPcSpecOptionTable`：CPU `~MHz`/`ProcessorNameString`、内存、显卡）与 `sub_A1F8A0`/`sub_A215F0`（通用注册表脚本引擎）。

### 一·补（N2 实测，2026-09-14）

- `authsv*.csv`（VFS `./settings/authsv.csv`，在归档 `settings_0000.dat` 内）：**客户端只经 VFS(`sub_AEFD80`) 读**，
  磁盘散装同名文件**不被读取** ⇒ 私服改列表必须**等长改写归档内条目**。表由 **`IF::CLoginWindow`** 全程负责。
- 规格：`组ID,组名,IP,端口,图标ID`；行分隔 `"\n"`（`asc_D6AAB8`@`0xD6AAB8`）；`#` 首字符整行跳过；列解析为 `std::wstring`。
- 条目结构：`ServerGroup` 52B（`+0` int 组ID / `+4` wstring 组名 / `+32` vector<Server> / `+48` int 图标ID）；
  `Server` 32B（`+0` wstring IP / `+0x1C` uint16 端口）。map 在 `CLoginWindow+340`（键=组ID）。
- **加载顺序**：归档池先常驻就绪（`sub_746B40`）→ HTTP 后**覆盖式刷新**（`sub_746DC0`：先 `sub_746A50` 清空再重建）；
  HTTP 失败**不清空**（保留归档）。⇒ 非"先 HTTP 后回落"。
- **HTTP**：`GET http://ms.patch1.9you.com/launcher/authsv.csv`（渠道 3 → `_wegame`；staging → `_stg`）。
  传输 = WinHTTP 异步单例 `HttpMgrEx`，超时 3s×4；非 200 → 抛 `int 1`。**通道号 15 = authsv**。
- 兄弟文件 `sv_add.txt`/`sv_add_stg.txt`（VFS `./settings/`）= 另一路"默认地址池"，元素 `{std::string addr, u16 port}`（32B，随机取 1）。

## 二、网络报文（按通道）

### 2.1 平台/登录（gate `:1633`，经 proxy `:1632`）
| ID | 名称 | 体布局 |
|---|---|---|
| 1542 | `AckAccessCode` | `ID@0(u16), tempID@2(i32), s2c@6(u32), c2s@10(u32)` ⇒ 14B |
| 9001 | `LoginReq` | `ID@0, 账号@[6:21](15B), MD5@[21:54](33B hex)` ⇒ 77B |
| 9002 | `LoginReject` | `ID@0, tag@2, result@6(u16)` ⇒ 8B |
| 9003 | `LoginAccept` | `ID@0, 账号, MD5, 公网IP@[54:69]` ⇒ 106B |
| 2348 | `ServerUDPEp` | `ID@0, ipv4@[6:10], 端口@[10:11]`（**大端**）⇒ 12B |
| 2579 | `ClientUDPEp` | 客户端 UDP 端点（客户端 UDP 固定 3001） |
| 31/32 | `Heartbeat/Reply` | `ID@0, seq@2, stamp@6` ⇒ 10B |

### 2.2 access 握手 + 会话加密（30000/30001/30002 通用底座）
> ★ N3 定案（2026-09-14，静态证据见 `nodes/03-access握手与会话加密.md`）
```
信号层：TCP 裸字节流（无外层锁/无 CRC）
握手  ：C→S 16B = 客户端 RSA 模数 n_C（小端）
        S→C 32B = block1 ‖ block2，★两块都是 RSA_enc(·, n_C, e=65537) 密文
                  block1 → 客户端装入「入站解密 ctx = 对象+0x3A0」
                  block2 → 客户端装入「出站加密 ctx = 对象+0x290」
        （Mode B：S→C 16B = n_S，客户端生成两把 16B 密钥 + 用 n_S 加密后回 32B）
帧    ：4B LE 头 = ★「明文长度 n」；数值 == (块数<<4)|尾字节数
        尾块不足 16B 也发一整块 16B 密文；单帧明文 ≤ 16366（=0x4000−18）
        ⇒ 帧长 = 4 + 16*(n>>4) + (n&0xF ? 16 : 0)；头不加密
密码  ：Camellia-128（标准向量通过；非 AES ✗）
计数器：= ctx 第 1 个 dword（密钥扩展写入 KL[0]），★每块 ++1、跨消息跨连接持续累加、无复位点
游戏层：sub_C84B60 分发，首字节高4位=type(0..4)，低2位=k ⇒ 长度字段占 k+1 字节
        type0 数据帧载荷 → vt[21]（业务报文分发器）；type≥5 ⇒ 返回 −1
```

**type 表（`sub_C84B60`，最小长度实测）**

| type | 最小长度 | 去向 |
|---|---|---|
| 0 | `k+2+len`（`k=buf[0]&3`） | 载荷 → `vt[21]`（业务分发器） |
| 1 | 9 | 对端时间戳（1B+u64） |
| 2 | 9 | RTT（`this[5]=now−u64`） |
| 3 | 5 | 控制帧（1B+u32）→ `vt[23]` |
| 4 | 子类 0:17+N / 1:13 / 2:13+N / 3:14+N | 密钥/安全层（`sub_C84790`/`sub_C84490`/`sub_C81F50`/`sub_C81D30`）；要求 `this[20]`≠0 |
| ≥5 | — | **返回 −1**（未知类型）+ 日志 39 |

**建连落点**：`sub_AF7130(holder,host,port)` → 管理器 vt[6](holder[0],host,port,**30000**,0) → `createSession`(`sub_CA9B40`)；
**host @ 会话+0xC4（256B 串）**、**port @ 会话+0xA0（u16）**、**握手模式位 +0x9C=0（Mode A，真实客户端走这条）**。

> ★ N5 补充（2026-09-14）：第 4 参**恒为硬编码 `30000`**（写入 `会话+0xB0`），**不是连接端口**——
> 三种连接（30000 auth / 30001 lounge / 30002 channel）都传同一常量，且连接状态机 `sub_CAD510` 实际用 `会话+0xA0` 作端口
> （`sub_CB7A60(sock, *((u16*)this+0x50))`）。真端口 = 参数 `port`。
> 三个连接各自的包装与 holder：`sub_AF73B0()`(30000, `dword_1201A5C+968`) / `sub_AF73E0(h,p)`(30001, `dword_1201A60+0x20B0`) / `sub_AF7400(h,p)`(第三 proto, `dword_1201A64+16576`)。
> holder 布局：`+0`=会话对象、`+4`=ready 字节、`+6`=closing 字节。

### 2.3 认证连接（30000，`CGVOProtoAuth`，vtable `0xEED714`，分发器 vt[21] `sub_B03D30`）

> ★ 2026-09-14（N4）**逐条 IDA 复核后重写**：旧表把 `0x1146` 的**应答**字段当成 `0xA380` 的**发送体**。
> 线上口径：`send 体 = ID 之后的字节`、`recv 体 = ID 之后的字节`。

| send | recv | 名称 | send 体（ID 之后） | recv 体（ID 之后） | 分发 case 体 |
|---|---|---|---|---|---|
| 0x34A9 | 0xDE24 | proto_version_check | `u32 version, u32 crc, u32 gentime` ⇒ 12B（实测 1977 / 0x2D45E072 / 0） | 同左 ⇒ 12B（共 14B 帧） | `sub_B04800` |
| 0x2C1A | 0xA5DA | authenticate | `str login_id(≤513) + str login_pw(≤513) + str disk_uuid(≤128) + str mac_addr(≤128)`（4 个 NUL 变长串，**明文**） | `u32 result` ⇒ 4B | `sub_B049F0` |
| 0x8288 | 0x298E | worldlist_get | **空（仅 2B，无 last_world）** | `u32 result + u32 last_world + u32 count(≤32) + count×309B` | `sub_B03DC6` |
| 0x3B8F | 0x4F3F | overplay_resettime_get（防沉迷） | **空（仅 2B）** | `u32 reset_sec` ⇒ 4B | `sub_B04355` |
| 0xA380 | 0x1146 | worldlist_select | `u32 world_id + u32 channeling_type` ⇒ **8B** | `u32 result + str world_name_en(≤49) + str loungesv_host(≤129) + u32 port + u32 userid + str otp(≤41)`（缓冲 231B） | `sub_B04068` |
| 0x8F36 | 0x8F36 | you9channeling（同 ID 双向） | `str×4`（4 个 NUL 变长串） | `u32 result` ⇒ 4B | `sub_B04667` |
| 0xA103 | 0xA103 | bnpotp_input | 空 | **空体（仅 2B）** | `sub_B04B61` |
| 0x60E0 | 0x60E0 | you9otp_input | `u32 otp_type + str otp_matrix_code(≤17)` | 同左 | `sub_B044D4` |

**★ 变长字段铁律（N4 定案，造包必须遵守）**

- 所有字符串都是 **NUL 结尾的变长串**，不是定长字段；`≤N` 只是**读取上限**。
- 读取器 `sub_B02BA0`：`memchr(ptr,0,min(N,剩余))` —— **上限内找不到 NUL ⇒ 返回失败**；
  找到后**游标停在 NUL 之后**（不是字段末尾）。
- 每个 case 结束都要求 `游标 == 报文尾`；⇒ **字段内无 NUL**、或 **NUL 之后还有填充字节**，都会让整包被丢弃。
- 丢弃是**静默的**：报错回调 = vt[25] = `nullsub_35`（空函数，`0x691680`），不断开、不重试、不提示。

**世界条目（309B/条，`sub_B02E20`）**：`u32 worldid(4) | name(49) | name_en(49) | desc(193) | u32 stat(4) | u16 icon_id(2) | u32 client_now(4) | u32 client_max(4)`（内存记录按 316B 步长排，缓冲 10124 = 12 + 32×316）。

**门控**：每报文一个序号槽（send 槽 `this[92+n]`、recv 槽 `this[108+n]`，`sub_B02F10` 初始化**全置 1**）；
`sub_B02C90(this,n)` 校验 `this[108+n]`（=0 ⇒ 错误码 2）并做时间预算检查（错误码 3）。

### 2.4 大厅连接（30001，`_proto_lounge_client`，分发器 `sub_B51930`）
| send | recv | 名称 | 体布局 |
|---|---|---|---|
| 0x34A9 | 0xDE24 | proto_version_check | 同上 |
| 0xF24B | 0xA5DA | lounge authenticate | **send 体 = `u32 userid` + NUL 字符串 `otp`（变长，`sub_B896A0` 组包）；recv 体 = `u32 result` + `u32 admin_lv`（★必须 8B，4B 会失败）** |
| 0xF86A | 0x5290 | datafile_download | `u32 result | str filepath(NUL) | u32 hashval | u32 src_bytes | u16 compress | u32 bin_len | bin` |
| 0x60CD | 0xE13A | pilot_list_get | `u32 result | pilots_eff 1×398B | pilots_zeon 1×398B | u32×4 | u32 charge_point | u32 bmgpack_count(≤16) | count×23B | u8 is_tutorial_end | u32×5` ⇒ 空列表 **845B**（n=0x0E） |
| 0xFD3E | 0xC43C | pilot_create | `u32 result + 159B 记录` ⇒ 163B（n=0x10） |
| 0xF705 | 0x063E | pilot_select | ★**最小 51725B**（不是 68B ✗）：`result u32 | restore_channel u32 | charge_point u32 | tuto_step u32 | tuto_flags u32×2 | tuto_missionid u32 | pilot_detail 51672B | is_netcafe u8 | is_processing_comeback u8 | vip_lv u32 | overplay_type u8 | accum_playtime u32 | daily_compcnt u32 | ncafe_compcnt u32 | heroms_term str(NUL,≤65) | flag_wideuse u8 | level_point u32`（n=0x16；alloc 56201 自洽 ✓） |
| — | 0x0587 | pilot_dailyrecord_notice | 1B `is_open_info` |
| — | 0xFB85 | channel_login | `u32 result, u32 channel_id, str host, u32 port, u32 userid, u32 pilot_id, str otp`（n=7；alloc 0xBE=190 ⇒ 小包） |
| 0x6142 | 0x986D | pilot_delete | 应答**恒 13B**：`result i32 \| pilot_id u32 \| del_kind u8 \| del_remain_sec u32`；请求 = `troops u32 \| slot u32 \| pilot_id u32 \| del_kind u8`（13B）。★★**应答的 `del_kind` 必须回 `2`**（不是回显请求的 0/1）—— 只有 `2` 才会"退出浮层 + 重发列表" ✓（详见 `nodes/07 §3.10`） |
| 0x498B | 0xBF1F | pilot_rename / 命名检查 | 应答**恒 46B**：`result i32 \| troops u32 \| slot u32 \| pilot_id u32 \| pilot_name(NUL,≤25) \| status u8 \| pilot_rename_remaintime u32`；请求 = `troops u32 \| slot u32 \| pilot_id u32 \| bef_name(NUL,≤25) \| new_name(NUL,≤25) \| is_check_only u8`（**1 = 只查重 / 0 = 真改名**）。★★`status`：**3 = 改名成功**（客户端写本地机师记录 ⇒ 卡片立即刷新）/ **1 = 查重·拒绝路径**（按 `result` 弹错误码，如 `-10100 名字已被使用`）（详见 `nodes/07 §3.9`） |

> 完整大厅 send 表（~210 条）见 `topics/14-大厅send报文ID全表.md`。

> ★ N5 补充（2026-09-14，大厅认证解锁链）：
> - **OTP 是不透明串**：由服务器在 `0x1146` 下发 → 客户端存 `app+1297` → 在 `0xF24B` 里**原样回传** → 之后 `0xFB85` 再下发一次覆写。客户端**不计算、不本地校验** ⇒ 私服可下发**空串/固定值**（body 变 `u32 userid + 00`，5B）。
> - `0xA5DA.result < 0` 的后果：客户端会**关掉 30001**（`sub_AF6FF0`）并把 LoginScene FSM **打回 `state 10`（登录窗口）**——排障时莫误判为网络故障。
> - 大厅 step 状态机：`0x=connect(30001)` → `1=等会话就绪` → `2=发 0xF24B` → `3=等 0xA5DA` → `4..0xA=本地初始化`（case 6 打开 CPilotRecordWindow）→ `0xA: app[114201]=1` 结束。
> - 30001 与 30002 **是同一会话槽的两次连接**（`sub_AF7130` holder 同为 `dword_1201A60+0x20B0`）；`0xFB85` 处理器 `sub_43BC70` 先 `sub_AF6FF0()` 断开，再由 `sub_43ADD0` 用**同一个** `sub_AF73E0` 重连到 30002。

> ★ N6 补充（2026-09-14，`0x5290` 逐字段核对 + 76 表泵）：
> - **`0x5290` 体** = `u32 result | str filepath(NUL,≤0x100) | u32 hashval | u32 src_bytes | u16 compress | u32 bin_len | bin[bin_len]`；
>   逐字段读法（VA）：`sub_B41470+sub_B02DD0`(result) → `sub_B02BA0(buf,cursor,0x100)`(filepath，**NUL 结尾**) →
>   `sub_B41470+sub_B02DD0`(hashval) → 同左(src_bytes) → `sub_B413B0+sub_B02DF0`(compress,u16) →
>   同左(bin_len，`>0x8000000` ⇒ 整包丢弃) → 逐字节拷 `bin`；拷完**要求游标正好到报文尾**。
> - `hashval` **不被校验**（`sub_BAAFF0` 内零引用）；`compress=0` 原样、`=1` 走解压（`sub_C86010`）、其它 ⇒ 卡死。
> - ★ `filepath` 是**裸 NUL 结尾串**（**无** u16 长度前缀），必须与请求**逐字节相同**（否则 `sub_576160` 反查 map 失败 ⇒ 静默、不置位 ⇒ 卡死）。
> - `result<0` ⇒ `sub_BAAFF0` 直接空转（不置完成标志）⇒ 泵死锁。
> - **下载泵 `CDataTableDownload`（20B）**：`+0x8 map._Myhead` / `+0xC map._Mysize` / `+0x10 flag(bit0=CAN_SEND)`；
>   `sub_576140` 每帧：`if(flag&1){ flag&=~1; sub_5760B0 }`；`sub_5760B0` 取 **map 最左节点（= 处理器 ID 升序）** 发 `0xF86A`（`hashval` 恒 0）。
> - ★★**只有"成功"才推进**（`sub_A4A020` 删节点 + `flag|=1`）：`result<0` / `compress∉{0,1}` / 脚本解析失败（`sub_BBBD70`、`sub_AEDCF0`）/ filepath 不匹配 —— 四种**都不置位、不删节点** ⇒ **永久死锁（无重试、无超时）**。
> - 泵**每次登录重建**（`sub_42E9B0` → `new` + `sub_576CC0`）⇒ 每次登录**重下全部 76 张表**（完成标志不持久化）。

> ★ N8 定案（2026-09-14，**进频道 = 客户端请求 → 服务端应答**；全文见 `nodes/08-进频道channel_login.md`）：
> - **`0xFB85` 的真名 = `recv_channel_list_select_r`**（日志串 @0xEE55E8 → 引用点 `0xB88045` 落在 case 体 `0xB87E8F` 内）
>   ⇒ 既有文档的 `channel_login_r` 是**臆造名** ✗；且全二进制**没有**写 ID `0xFB85` 的 send 函数（`0FB85h` 只出现于分发器 `cmp` @`0xB878B0`）
>   ⇒ **它只能是"服务端发来的应答"**，不是"被推"的包 ✓
> - 进频道三步（客户端侧全自动，由 `CGameStateStepUpdateGameModeSelectScene::step` = `sub_A87E50` 驱动）：
>   `0x3E0B send_channel_list_get`(体空,2B) → **`0xF11C`** → `0x2830 send_channel_list_select`(`u32 channel_id`,6B) → **`0xFB85`** → 客户端 `sub_43BC70` 断 30001 ⇒ `sub_43ADD0` case4 `sub_AF73E0(host,port)` **连 30002**
> - **`0xF11C recv_channel_list_get_r`**（case `0xB864A2`，n=5，alloc 1924）：`u32 count(≤32,★≥1) + count×`**54B 频道条目**
>   ```
>   +0 u32 channelid | +4 37B name(定长,UTF-8) | +41 u8 type | +42 u8 pilotlv_min | +43 u8 pilotlv_max
>   | +44 u16 user_num_eff | +46 u16 user_num_zeon | +48 u16 user_max | +50 u16 user_conn | +52 u16 user_comeback
>   ```
>   内存步长 **60**（`sub_B41230` 的 `dst += 60` 实证）⇒ alloc 1924 = 4+32×60 ✓
> - **`0xFB85 recv_channel_list_select_r`**（case `0xB87E8F`，n=7）：`u32 result(★≥0) | u32 channel_id | str host(NUL,≤128) | u32 port | u32 userid | u32 pilot_id | str otp(NUL,≤40)`
>   ⇒ alloc 自洽 **190 = 4+4+129+4+4+4+41** ✓（两个字符串用有界串读取器 `sub_B02BA0`，**必须 NUL 结尾、游标恰到底**）
> - ★"回完 `0xFB85` 客户端立刻断开" = **正常**（`sub_43BC70` 第一步就是 `sub_AF6FF0()` 断 30001，下一帧重连 30002；30001/30002 复用同一会话槽）。
> - `0x063E` 体长默认值：服务端 `STICKY_SELECT_BODY_LEN` 已从 68 改为 **51725**（N7）。

### 2.5 频道服（30002，**同一个** `_proto_lounge_client`，同分发器 `sub_B51930`）

> ★★ 2026-09-14 落地要点（Go）：**30002 的报文表 = 30001 的 lounge 全套**（同 ID 空间）
> ＋ **首屏 9 条骨架应答**。以前这里挂的是"只读观察口"（一个 handler 都不注册）⇒
> 客户端连上后第一包 `0x34A9` 无人应答 ⇒ **选完机师白屏** ✗（客户端 FSM `sub_43ADD0` 缺一条应答就卡一格）。
> 启动参数：`-channel :30002`（★别再用 `-observe :30002` ✗）。
>
> 首屏请求 → 应答（★应答 ID 为**候选**，体格式未定 ⇒ 先回 `u32 result=0` 骨架，看客户端是否推进）：
>
> | FSM | 请求 | 请求 ID | 应答 ID | 应答体（★=已按 case 读取序列定死，⚠️=待定） |
> |---|---|---|---|---|
> | 8 | chargepoint_price_list_get | `0x7CCB` | `0x9397` ✓ | ★`u32 \| u32 \| u8` = **9B**（★别写成 3×u32 ✗） |
> | 9 | item_init_get | `0x947E` | `0x02EE` ✓ | ★`u32 count(≤0x384) \| count×24B \| u32×4` ⇒ 空表 **20B** |
> | 0xA | msma_init_get | `0x16AC` | `0x2ACF`（end=`0xFCE6`） | ⚠️ u16/u32 交替长序列 |
> | 0xB | msma_msset_get | `0x9A9D` | `0x356F` | ⚠️ `u32` 起头（`vt[0x78](0x784)` 结构） |
> | 0xC | msma_missionunit_get_list | `0xDCA1` | `0x36D9` | ⚠️ `u32` 起头（`vt[0x78](0x10C)`） |
> | 0xD | player_navi_get_list | `0xF0C4` | `0x0876` | ⚠️ `u32 count(≤0x18) \| count×?` |
> | 0xE | ranking_init_get | `0x05A5` | `0x7C8A` ✓ | ★`u32 is_revoked \| u32 cnt1(≤7) \| cnt1×u16 \| u32 cnt2(≤7) \| cnt2×u16` ⇒ 空表 **12B** |
> | 0xF | pilot_evflag_3_get | `0xB681` | `0xE0DE` | ⚠️ 至少 `u16 item_cnt \| u32 money_gp \| u32×3` |
> | 0x10 | block_list_get_idwlist | `0x921B` | `0xCCDF` | ⚠️ `u32 cnt1(≤0x64) \| cnt1×4B \| u32 cnt2(≤0x64) \| cnt2×4B …` |
>
> ★★ **铁律**：这些 `_r` case 末尾都有 `cmp <cursor>, <end>`（"游标恰到底"）⇒ **体长必须精确匹配** ✗
> （多/少一字节都失败，且失败**不是静默**：走 `vt[0x64](<case 序号>, 1)` 上报 ⇒ 界面看着像卡住）。
> 求体格式的方法：`recv_<名>_r` 日志串 → xref（必在该 case 解析区）→ 往前 ~0x200 的读取序列 ✓
> （`sub_B02DD0`=u32 / `sub_B02DF0`+`sub_B413B0`=u16 / `sub_B41470`=取槽 / `sub_B416C0`/`sub_B41850`=向量）。
>
> 已实证但**应答未实现**（不回也不卡流程，界面缺数据）：`0x48F2 pilot_record_get`、
> `0xE9A2 pilot_favms_get`、`0x2F63 pilotcard_get`、`0xA3B2 channellobby_enter`、
> `0xD377 channellobby_members_get`、`0xC475 channellobby_scene_transition`。

> ★ N9 定案（2026-09-14，全文见 `nodes/09-进入游戏大厅.md`；★本节点 `partial`）：
> - **30002 不是新协议**：`sub_AF73E0(host,port)` → `sub_AF7130` → `dword_1201A58->vt[6](holder[0], host, port, 30000, 0)`
>   （模式位 0 = Mode A）⇒ **完全复用 N3 的 access 握手 + Camellia-128(counter) 帧**；
>   协议对象 = `dword_1201A60+0x20B0` 里那个 `_proto_lounge_client`（与 30001 同一个）⇒ 30001/30002 **共用 ID 空间**。
> - 会话就绪时协议对象**自动**发 `0x34A9`（`sub_BAE160` @vtable 数据槽 `0xEEDB84` → `sub_B89460(2024, 0xCDB0BDE5, 0)`）
>   ⇒ 应答 **`0xDE24`**（12B）。
> - 30002 的驱动器 = 每帧 tick **`sub_43ADD0`**（状态 = `app[+1396]`，2..21）：`case4` 建连 → `case5` 发 **`0xF24B`**
>   （`u32 userid + NUL 串 otp`）⇒ 应答 **`0xA5DA`**（`u32 result + u32 admin_lv`，★8B）→ `case6` `app[114201]=1`（大厅就绪）
>   → `case7..21` **首屏爆发**（下表；每条 case 的"门位"由**上一条应答**的处理器置位 ⇒ 缺一条应答就卡一格）。
> - ★**首屏请求表（请求 ID 逐条实证；应答 ID 为候选 ⚠️）**：
>
> | FSM | 请求 | ID | 体 | 应答（候选） | 应答 ID ⚠️ |
> |---|---|---|---|---|---|
> | 7 | `send_pilot_select` | `0xF705` | 17B | `recv_pilot_select_r` | **`0x063E`**（已验证） |
> | 8 | `send_chargepoint_price_list_get` | `0x7CCB` | 空 | `recv_chargepoint_price_list_get_r` | `0x9397` |
> | 0xE | `send_ranking_init_get` | `0x05A5` | 空 | `recv_ranking_init_get_r` | `0x7C8A` |
> | 9 | `send_item_init_get` | `0x947E` | 空 | `recv_item_init_get_r` | `0x02EE` |
> | 0xA | `send_msma_init_get` | `0x16AC` | 空 | `recv_msma_init_get_r_begin/_end` | `0x2ACF`/`0xFCE6` |
> | 0xB | `send_msma_msset_get` | `0x9A9D` | 空 | `recv_msma_msset_get_r` | `0x356F` |
> | 0xC | `send_msma_missionunit_get_list` | `0xDCA1` | 空 | `recv_msma_missionunit_get_list_r` | `0x36D9` |
> | 0xD | `send_player_navi_get_list` | `0xF0C4` | 空 | `recv_player_navi_get_list_r` | `0x0876` |
> | 0xF | `send_block_list_get_idwlist` | `0x921B` | 空 | `recv_block_list_get_idwlist_r` | `0xCCDF` |
> | 0x10 | `send_pilot_evflag_3_get` | `0xB681` | 空 | `recv_pilot_evflag_3_get_r` | `0xE0DE` |
>
> - 另有三个"频道大厅"报文（ID 实证，触发者未追）：`0xA3B2 send_channellobby_enter`(体空)、
>   `0xD377 send_channellobby_members_get`(`u32 is_simple`)、`0xC475 send_channellobby_scene_transition`(`u32 destination`)。
> - 发送函数命名规则：`send_xxx` 的发送许可位 = `proto[92+n]`、通知索引 = `n`（例：`channellobby_enter` 用 `proto[188]` ⇒ n=96）。
> - ★**实跑判据（本轮 08:41 未通过）**：客户端在 30001 上回完 `0x063E` 后**立刻断开并退回"选择战区"界面**，
>   `0x3E0B` **未出现** ⇒ 卡点仍在 **N7（`0x063E` 体/字段）**，不是 30002 的问题。

## 三、资源归档
| 项 | 格式 |
|---|---|
| `.hed` | `'FPMF' + u32 version + u32 payloadSize + u32 nchunk + payload`；payload 用 `kFpmfKeyHed` 减法 |
| `.dat` | 内容 `data[i] -= fileKey[i%8] + kFpmfKeyDat[i%2048]` |
| 文件条目 | `namelen u8 + name UTF-16LE + plen u8 + path UTF-16LE + volume u32 + fileKey 8B + offset u32 + size u32 + hash 8B` |
| 密钥 | `kFpmfKeyHed` VA `0xF39860`；`kFpmfKeyDat` VA `0xF3A068` |

## 四、CSV 方言（造"给客户端吃的表"必须遵守）

实测（65 个客户端真实 CSV）：

| 项 | 正确值 | 说明 |
|---|---|---|
| BOM | **无 BOM**（62/65） | ★带 BOM ⇒ 行回调 `首字符=='#'` 判定失效 ⇒ 表头被当数据行 ✗ |
| 换行 | **CRLF** | |
| 行尾 | **必须留尾逗号** | 99.2% 数据行如此 |
| 注释/表头 | 整行以 `#` 开头 | 表头也是 `#` 开头 |
| 越界列 | **写你要设的最大列即可，尾部可省略**（越界列=0，不报错） | |
| 地区开关 | `msma_weapon_set.csv` 末列：`JAPAN` ⇒ 整行丢弃；`CHINA`/留空 ⇒ 保留 | |

> ★ N6 核对（2026-09-14）：上表逐条与 `sub_BBBB70` / `sub_BBB4F0` 反编译一致。
> 「越界列=0」的守卫实现在 `sub_BBB4F0`：`col >= 总列数 ⇒ 返回空串（长度置 0），不报错`；
> 列记录步长 **28B**，列数组在 `row+112 / row+116`。
> `download_list.csv` 的行回调 `sub_576C60` 用**同一规则**：`line[0]=='#'(35) ⇒ 整行跳过`（故 **BOM 致命**）。

---

## 五、★ N7 定案（2026-09-14，机师列表/创建/选择）——全文见 `nodes/07-机师列表创建选择.md`

**★ 通用门控机制（lounge 协议，对 N8 至关重要）**

```
_proto_lounge 构造器 sub_B47420（唯一调用者 0xBAE0F3）：
  this[0..620]      = 1    // 621 个 send 许可位
  this[713..1333]   = 1    // 621 个 recv 期望位 ★默认全开
  this+1336..31143  = 0    // 621 × 48B 每报文计时块（全 0 ⇒ 跳过超时检查）
  this+31152(0x79B0)= 0    // 621 × 4B「请求对象」指针表
sub_B41120(this,n)：this[n+713]==0 ⇒ 错误码2/返回0；计时块+16 的 qword≠0 且 now>deadline ⇒ 错误码3
sub_B41110(this,n) = this[n+7788]（第 n 号请求对象；为 0 只影响日志）
⇒ 每个 recv case 第一句的 sub_B41120(n) 守卫【默认一律通过】；
  报文被丢弃只可能是 ①字段读取越界 ②末尾 cursor != end。失败一律静默（跳 loc_B890EE = 直接 return）
```

**★ 原语读取器语义（造包铁律）**

| 函数 | 语义 |
|---|---|
| `sub_B02DD0` / `sub_B02DF0` / `sub_B06230` | 读 u32 / u16 / u8（带边界检查） |
| `sub_B06200` | 读 8B（u32×2） |
| `sub_B02BA0(out,cursor,max)` | ★**有界变长串**：`memchr(NUL, min(max,剩余))` → 拷到 NUL、补 0、**游标停在 NUL 之后**；上限内无 NUL ⇒ 失败。**不是"跳过 N 字节"** |
| `sub_B42BB0` / `sub_B06980` / `sub_B068B0` | 398B 机师记录 / 159B 创建记录 / 18B 外观子对象（内部字符串**全定长、逐字节读、不做 NUL 检查**） |
| 指针助手 `sub_B41470`(4) / `sub_B05E30`(4) / `sub_B41A10`(8) / `sub_B41350`(424) / `sub_B05F00`(176) / `sub_B41260`(**56080**) | `*out=*cur; *cur += 步长`，**步长 = 该字段内存尺寸**；alloc 大小 = 解析结果结构尺寸 ⇒ 可自洽校验 |

**三处 alloc 自洽校验**：`0xE13A` 1281 = 4 + 424×2 + 16 + 4 + 4 + **24×16** + 1 + 20 ✓ 精确相等；
`0xC43C` 180 = 4+159(+17) ✓；`0x063E` 56201 = 28 + **56080** + 89(+4) ✓。

**字段速查**

- **398B 机师记录**（`sub_B42BB0`，内存步长 424B，**58 字段全命名**）：`pilot_id u32 | name 25B定长 | last_in u32 | troops u8 | level u8 | mil_class u8 | byword u16 | avatar 18B | cmdr_fame u32 | rate_vslocal u16×3 | 战绩 u32×28 | comment 116B定长 | clan_id u32 | clan_name 31B定长 | clan_emb_base/parts1/parts2 u8×3 | clan_memb_exp u32 | cupteam_id u32 | cupteam_name 31B定长 | channel_id u8 | state_bits u8 | accum_point u32 | rank u32 | base_accump u32 | req_accump u32 | level_point u32 | capture_bonus_state u8 | capture_bonus_limit u32` = 398 ✓
- **18B 外观**（`sub_B068B0`）：`avatar_id u32 | gender u8 | face u8 | skincolor u8 | clothes u16 | hair u32 | accessory u8 | frame u8 | voice u8 | u16⚠️未命名` = 18 ✓
- **bmgpack 元素**（`sub_B458A0`）：**线 23B / 内存 24B** = `shopitem_id u32 | gp_x01 u32 | gp_x10 u32 | cp_x01 u32 | cp_x10 u32 | bit_eff u8 | stock u16` ⇒ `0xE13A` = **845B + 23×n**（count ≤ 16）
- **159B 创建记录**（`sub_B06980` 读 / `sub_B06360` 写，内存 176B）：`pilot_id u32 | name 25B | troops/level/mil_class u8×3 | byword u16 | cmdr_fame u32 | rate_vslocal u16×3 | level_point u32 | avatar 18B | clan_id u32 | clan_name 31B | clan_emb_* u8×3 | cupteam_id u32 | cupteam_name 31B | accum_point/rank/base_accump/req_accump/level_point u32×5` = 159 ✓
- **`0x063E.pilot_detail`**（`sub_B42640`）：**线 51672B / 内存 56080B** 的机师全量存档，含 `favms_arr`(**720 条 × 66B 线 / 72B 内存**)、`hav_avatar` 160×8B、`hav_modules` 128×u32、`hav_rental_module` 128×8B、`cshist` 32×6B、`comment` 115B定长、`beginner_challenge` 454B(32×u16+96×u32) 等；字段名可用日志函数 **`sub_B48010`** 全量枚举，段级分布见节点文档 §3.2。
- **`0xF705` send 体**（`sub_B8A8B0`，日志串 `send_pilot_select` @0xB8A9C2）：`troops u32 | pilot_id u32 | is_tutorial_skip u8 | dbg_comeback_disable u32 | channeling_type u32` = 17B（+2B ID）
- ★ **`0x063E` 最小体 = 51725B**（服务端旧值 68 ⇒ 必失败）。`0x70E9` = `send_you9_cps_ClientCheck_response`（**不是** select 成功的证据）。

---

## 六、★ 30002 首屏应答体长定案（2026-09-14，N9·补；全文 `nodes/09 §附三`）

**★ 先记一条影响面最大的根因（作废两条旧推断 ✗）**：**单帧明文上限 = 16366B**（客户端 `sub_C88510`：
`n = 4B 头；if (n > sub_C87F30(this) || !n) break;` ⇒ `sub_CAC820(13,5)` **直接关连接**）。
⇒ 任何 >16366B 的下行报文**必须多帧连发**（`wrap_stream`），应用层报文可跨帧（客户端 `sub_C88510` 消费一帧后**循环读下一帧** ✓）。
⇒ 历史上"选机师就断链 / 大表一过就掉线 / 51725B 比 68B 更早失败"**全是这一条** ⇒ 多帧后 51725B(4 帧) 被接受，客户端随即发 `0x3E0B` ✓。

**首屏 9 条 `_get` 的应答 = 零填体长**（`sub_43ADD0` case7..0x10 依次发；**体长必须精确匹配**，末尾 `cmp cursor,end`）：

| 请求 ID | 应答 ID | case 入口 | alloc | **零填体长** | 读取序列 |
|---|---|---|---|---|---|
| `0x7CCB` | `0x9397` | `0xB6D145` | 37 | **37B** | 7×u32+3×u16+3×u8（alloc == 固定和 ✓✓）|
| `0x05A5` | `0x7C8A` | `0xB68904` | 40 | **16B** | u32∥(count1≤7)+表∥u16∥(count2≤7)+表∥u16 |
| `0x947E` | `0x02EE` | `0xB524F6` | 62464 | **64B** | 4×u16∥6×u32∥(≤300)+表∥(≤100)+表∥(≤1300)+表∥(≤900)+表∥4×u32（★alloc 是向量容量总量、非体长）|
| `0x16AC` | `0x2ACF` | `0xB59F70` | 28 | **28B** | u32,u16,u32,u32,u16×3,u32,u32（✓✓）|
| 〃（追加） | `0xFCE6` | `0xB884CD` | — | **0B（真空体）** | case 首句即 `cmp cursor,end` ⇒ 补 4B 反而被丢 ✗ |
| `0x9A9D` | `0x356F` | `0xB5BADF` | 1924 | **4B** | u32 count(≤20)∥count×sub_B43B00 ⇒ count=0 |
| `0xDCA1` | `0x36D9` | `0xB5C764` | 268 | **4B** | u32 count(≤22)∥count×sub_B43BE0 ⇒ count=0 |
| `0xF0C4` | `0x0876` | `0xB542C3` | 36 | **36B** | u32,8B,u32,u32,u16,u16,u32,u16,u16,u32（✓✓）|
| `0xB681` | `0xE0DE` | `0xB8240B` | 8 | **8B** | 单个 8B 读 + 游标检查（✓✓）|
| `0x921B` | `0xCCDF` | `0xB7B003` | 556 | **20B** | u32∥(count1)+表∥u32∥(count2)+表∥u32 |

> 提取方法（复用）：`recv_<名>_r` 日志串 `DataRefsTo` → 引用点 + `sub_B51930` 里 `cmp eax,<ID>` → 紧随 `jz` = case 入口；
> 体长判据 = 末尾"游标恰到底" ＋ 开头 `vt[0x78](N)`（= 解析结构**内存**尺寸）。
> 旧估算值 `0x9397=9/12B`、`0x02EE=20B`、`0x7C8A=12B` **全部作废** ✗。

---

### 五·补（2026-09-14 真机现逆：删除 / 改名 / 四条铁律）

**两条新报文**（逐字段见 §2.4 表 + `nodes/07 §3.9/§3.10`）：

- **`0x6142 → 0x986D` 删除**：应答恒 **13B**；★`del_kind` **必须回 2**（回显 0/1 ⇒ 机师浮层关不掉、永远卡在删除页 ✗）。
- **`0x498B → 0xBF1F` 改名 / 命名检查**：请求末字节 `is_check_only`（`1` = 只查重、`0` = 真改名；
  真机实测两次点击间隔 ~4s）；应答恒 **46B**；★`status`：**3 = 改名成功**（客户端把新名字写进本地记录 ⇒ 卡片立即刷新）/
  **1 = 查重·拒绝路径**（客户端 `sub_726400(win, result)` 按 `result` 弹错误码）。

**四条铁律**（都是真机踩出来的，详见 `nodes/07 §3.11`）：

1. ★★**`_r` 应答一律定长**（删除 13B / 创建 163B / 列表 845B+23n / 改名 46B）——
   `case` 里 `push <常量>` 就是客户端定长读的长度；**把变长字段（NUL 串）放进应答 ⇒ 游标错位 ⇒ 整条静默丢弃** ✗
   ⇒ 现象伪装成"服务端明明改了、客户端就是不认"（改名那条就是这么坑了整整一轮 ✗）。
2. **`del_kind` / `status` 这类 u8 是"结果种类"**（决定客户端下一步做什么），
   **不是请求回显、也不是成败标志**（成败看 `result`）⇒ 猜值必错，必须反编译回调。
3. **势力值线上是 0 基**（`0 = 秩序/eff`、`1 = 抵抗/zeon`），内部与文档一律 `1 = 秩序 / 2 = 抵抗`。
   证据：同账号建"秩序/男"+"抵抗/女"，创建包 diff ⇒ `off29`(势力) / `off52`(性别 = `avatar+4`) 双双 0/1。
4. **`slot` 是"每阵营各自从 0 数"**（同一账号在秩序与抵抗各建一个，两次 `slot` 都是 0）⇒
   服务端存储键必须 `(账号, 阵营, slot)`；列表 `pilots_eff`/`pilots_zeon` 必须**按各自阵营分别填**
   （否则另一个阵营的机师"创建了但没显示" ✗）。

---

## 六、★ 离线产物索引（自动导出，供"造表/读代码"直接用）

| 产物 | 路径 | 内容 |
|---|---|---|
| **服务端数据表列规格** | `formats\数据表-80表列规格.md`（人读）＋ `formats\tables_spec.json`（机读） | **79 张表**（= `download_list.csv` 全量 76 行 ＋ 3 张本地表）：下载序 → 表ID → 文件名 → 类名 → 逐列读取函数 → **列定义（列号 0-based + 原语类型）**；★**已解出 78/79 张、共 1155 个列位、0 处未解析**（`AUTOEXEC` 是脚本、无列定义） |
| **枚举值表（名↔值）** | `formats\枚举表.md` ＋ `formats\enums.json` | ★**30 个"表型"枚举共 599 条名↔值**（可直接照抄进 CSV）＋ 10 个"比较链型"（名称已导出、值需人工确认）；含 **169 个枚举列 → 转换函数** 的对照 |
| 生成器 | `formats\extract_table_spec.py`、`formats\gen_enum_spec.py` | 由 `_idmap.json` / `_tables_extract.json` / `enums.json` / `download_list.csv` 合成上面几份 |
| 表ID 映射 | `formats\_idmap.json` | ★**`download_list.csv` 行序 → 表ID**（客户端查表 `sub_575FF0` @`0xD783E0`，是 `{u32 id; wchar_t* 定义名}` 数组）——**注意：行序 ≠ 表ID**（如 行序19↔ID20、行序31/32/33 → ID32/33/31） |
| 登录链伪代码 | `asm\登录链-伪代码-01..16.md` | **633 个函数**的 Hex-Rays 伪代码（含 VA/大小/调用者） |
| 登录链汇编 | `asm\登录链-汇编核心-01..17.md` | **421 个核心函数**的完整汇编 |
| 复现脚本 | `asm\dump_login_chain.py`、`asm\README.md` | 重跑方式与"从这里开始读"的入口清单 |
