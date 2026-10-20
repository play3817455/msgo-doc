# W02 · 平台认证 authsv（N2）逐字段：URL 参数 / HTTP 请求 / CSV 逐列 / 服务器条目内存布局

> 状态：`done`　｜　完成：`2026-09-15T01:38`　｜　会话：第 2 次（v2 队列驱动）　｜　工作项：`workqueue.json.items[W02]`
> 证据来源：IDA Pro MCP 静态（IDB `unpacked\GundamOnline_CHINA_v15.exe.i64`，基址 `0x400000`，Hex-Rays）＋ 归档 CSV 实文件字节
> 继承：`nodes/02-平台认证authsv.md`（链路/超时/通道号已定案）　｜　本文件**只补 N2 未落地的"逐字段"部分**
> 地址口径一律 `sub_XXXXXX`（VA）。**全程静态，无动态**（9you 域名已停服）。

---

## 0. 一句话结论

`authsv` = 客户端"平台认证服务器列表"的**分发通道**，与任何游戏内报文无关：

1. **数据面 = 5 列 CSV**：`组ID,组名,IP,端口,图标ID` → 内存 `std::map<int 组ID, ServerGroup>`；
   **每组 = `pair` 52B**（键 4B + 组名 `std::wstring` 28B + `vector<Server>` 16B + 图标 int 4B）；
   **每服务器 = `Server` 32B**（地址 `std::wstring` 28B + 端口 `u16` 2B + pad 2B）。
2. **本地先行**：`sub_746B40`（构建期）经游戏 VFS 读 `./settings/authsv[_stg|_wegame].csv`，逐行回调 `sub_746710`。
3. **远端覆盖**：`sub_747E10` → `HttpMgrEx::vt[3]` = `sub_BB22E0` 发 **`GET`** + **唯一附加参数 `t = GetTickCount()`**（值经 **URL-encode**，拼成 `k=v&k1=v1`，序列化器 `sub_BB35E0`）。
   成功 ⇒ `sub_746DC0` **先清空 map 再重建**；失败 ⇒ **保留本地池**（这就是私服"只改归档即可"的根因）。
4. **URL 不手工拼**：`sub_BAFBD0` 直接调 **`WinHttpCrackUrl`** 拆出 host/user/pwd/path/extra(=`?…`)/port/scheme，故 **端口未在串里出现 ⇒ `nPort = 80`**（本次三个 URL 都无显式端口）。

---

## 1. 汇编逻辑

### 1.1 本项新增/复核的调用链

```
【本地池建立】（构建期，一次性）
sub_746B40(this=C瓦LoginWindow, a2=?)
  ├ sub_402AD0(&v8, a2, L"E01_ServerSelect", 0x10)                       组装子控件名（0xDD1034）
  ├ sub_762430(&v8, {sub_744DF0, this})                                  == 0 ⇒ vt[+44](this)、return 0
  ├ v4 = sub_BDC300(340, flt_EF0EF8, 0); *v4 = &IF::CPopupBackgroundWindow::vftable
  ├ 路径三选一（★与 HTTP 侧同条件，两处独立代码）
  │    sub_A1E840()  ⇒ L"./settings/authsv_stg.csv"     (0xDD10C0)
  │    else sub_A1E880()!=3 ⇒ L"./settings/authsv.csv"  (0xDD1058)
  │    else (==3)     ⇒ L"./settings/authsv_wegame.csv" (0xDD1084)
  ├ sub_C3CF00(dword_11E3FCC)                                          选"当前表上下文"
  ├ sub_AEFD80(&path, 2, sub_746710, this, 1, 0)                       ★VFS 读 + 逐行回调
  └ sub_744570(this); sub_745210(this)                                  滚动范围 + UI 条目

【逐行回调】（本地/远端**共用同一个**）
sub_746710(a1 = 行对象(TokenRow), a2 = CLoginWindow*)
  ├ col0 = sub_456D90(&v15, 0)                                         列 0（wstring）
  │    ★ 首字符 == '#'(35) ⇒ 整行跳过；列 0 长度(+20)==0 ⇒ 空行跳过     （v12 标志）
  ├ v6 = sub_BBB370(a1, 0)                  组ID  = atoi(列0)          → pair+0
  ├ v7 = sub_BBB4F0(&v15, a1, 1)  → sub_BBB130(v29, v7, 0)  组名        → 记录 +4（28B wstring）
  ├ col2 = sub_BBB4F0(&v15, a1, 2); sub_402310(col2, 0, -1)   IP        → Server+0
  ├ v28 = (u16)sub_BBB370(a1, 3)   端口                                 → Server+0x1C
  ├ v10 = sub_BBB370(a1, 4)        图标ID                               → 记录 +48
  ├ sub_744680(this+340, &it, &v13)                                     map::find_or_insert(组ID)
  │    命中已有组（返回 != end 且 != _Myhead） ⇒ 只 sub_745F90(&elem)    ⇒ vector push_back
  │    新组                                      ⇒ 建记录：
  │         sub_745B90()                         记录 ctor（pair, 52B）
  │         v30 = v6; sub_4029E0(v31, v29, 0, -1) 组名 → pair+4
  │         v31[11] = v10                        图标 → pair+48
  │         sub_745F90(v24)                      group+32 的 vector push_back(Server 32B)
  │         sub_745C50(&v30)                     记录拷贝进 map 节点
  └ return 0（恒 0 ⇒ 永不提前终止遍历）

【HTTP 拉取】
sub_747E10(this, a2=0首次/1刷新)
  ├ this[376] 的 bit1(0x2) ← a2；bit2(0x4) 已置 ⇒ return（防重发）
  ├ this[376] |= 4
  ├ sub_42E760(dword_11E3EA8); sub_43A350(0, 1.0)                       进度/场景
  ├ sub_BB3920(v6)                                                      ★HttpParameters ctor（16B）
  ├ sub_402880(L"t" /*0xDD194C*/, 1)                                    ★追加参数名 "t"
  ├ sub_BB33C0(v7, GetTickCount())                                      ★参数值 = 当前 tick 计数
  ├ 选 URL（同 §1.1 三选一）
  └ (*(HttpMgrEx+0)+12)(HttpMgrEx, 15 /*通道号*/, L"GET", URL, &v6)

HttpMgrEx::request = sub_BB22E0(this, a2=通道号, a3=方法, a4=URL, a5=附加参数)
  ├ if (*(this+4) == 0) return 0                                        未初始化
  ├ sub_BAFBD0(a4, …8 输出…)                                            ★WinHttpCrackUrl 拆 URL
  │    失败 ⇒ sub_BAE500(GetLastError) + return 0
  ├ sub_4029E0(a3,0,-1); sub_4029E0(a4,0,-1)                            方法/URL 移动进请求对象
  ├ v10 = a5 + 4; sub_BB09C0(&v15, *v43, v43); sub_BB0A80(v10)          ★参数对象拷进请求对象
  ├ sub_BB2280(&v41)                                                    入队（环形数组 + 锁）
  └ sub_BAFA20()

【发送】
sub_BB5A80(req, ?)
  ├ sub_408530(method, 0, len, L"POST" /*0xD91C48*/, 4)                  ★方法名比较（std::wstring::compare）
  │    分支 A（比较结果 == 0）: sub_BB35E0(…) + WinHttpSendRequest(h, &szHeaders, dwHeadersLength, 0,0, dwTotalLength, ctx)
  │    分支 B（非 0）        : WinHttpSendRequest(h, 0,0, 0,0, 0, ctx)
  └ 失败 ⇒ sub_BAE500(GetLastError)

【参数序列化】★本次新解
sub_BB35E0(this=参数表, a2=输出 std::string)
  遍历 HttpParameters 的红黑树（+8 = head）：
    if (i > 0) sub_41D990(buf, &unk_EEEF8C)          ← 追加分隔符 **"&"**
    v7 = sub_BB3450(…, v6)                            ← **URL-encode(值)**
    v8 = sub_BB3450(…, 键)                            ← **URL-encode(键)**
    sub_ADC970(buf, v8)                               ← 追加键
    sub_41D990(buf, &unk_EEEF88)                      ← 追加分隔符 **"="**
    sub_ADC970(buf, v7)                               ← 追加值
  ⇒ 结果形如 `t=1234567`，多参数为 `k=v&k1=v1`
sub_BB3450(输出串, 输入串) = **percent-encoding**：
  保留 [0-9][A-Z][a-z] 与 `-` `.` `_` `~`；其余 ⇒ `%XX`（37='%'，两位大写十六进制、fill '0'）
```

### 1.2 关键函数表（本项新增/复核部分）

| 地址 | 身份 | 作用 | 证据 |
|---|---|---|---|
| `sub_746710` | authsv **逐行回调** | 解析 5 列 → 建/追加 `ServerGroup` | 全文反编译（本文件 §1.1） |
| `sub_456D90` | **取第 i 列**（`std::wstring`） | `cap>=8 ⇒ heap 指针`；越界 ⇒ 空串 | `*(this+24)=7`（wstring SSO）；`(a1+112)+28*i` 元素步长 **28B** |
| `sub_BBB370` | 第 i 列 → **int** | 越界返回 **0**；否则 `sub_CC6876`(=`atoi`) | 全文反编译；`(a1+116)-(a1+112))/28` 边界检查 |
| `sub_BB3920` | **`HttpParameters` ctor** | vftable `HttpParameters::vftable`(`0xEEEF5C`) + 建红黑树头（`+65=1` 哨兵） | 全文反编译 |
| `sub_BB33C0` | **追加参数值** | 造"值对象"并挂到参数表 | `sub_BB2860`/`sub_BB2C40`/`sub_BAFAB0` |
| `sub_BB35E0` | **参数序列化** | 红黑树 → `k=v&k1=v1`（键值都 URL-encode） | `unk_EEEF88`=L"="、`unk_EEEF8C`=L"&" |
| `sub_BB3450` | **URL-encode** | 保留 `0-9A-Za-z - . _ ~`，其余 `%XX` | 全文反编译（37='%'，fill '0'） |
| `sub_BB2FD0` | 值 → 文本（4 种值类型） | `type-1`: 0→`sub_B087C0(+4)`；1→`sub_BB2AE0(+8 u8)`；2→`sub_ADC970(+8 串)`；3→`sub_B03580(+8)`；**4=default 不输出** | 全文反编译 |
| `sub_BAFBD0` | **URL 解析** | **`WinHttpCrackUrl`**（`dwStructSize=60`）→ 7 输出 | 全文反编译（`0xD66578`） |
| `sub_BB5A80` | 发送 | `WinHttpSendRequest`；先与 `L"POST"` 比方法 | 全文反编译 |
| `sub_408530` | `std::wstring::compare` | `(this+5)=长度`、`(this+6)=容量`、逐 `wchar` 比较 | 全文反编译 |
| `sub_BB2280` | **入队** | 环形数组 `this[1]`、容量 `this[2]`、索引 `this[4]`；节点 76B | `sub_CC55FA(76)` |
| `sub_BBB130` / `sub_7465C0` | 组名/记录搬运 | `sub_BBB130(v29, v7, 0)` 取列 1 | 调用点 `0x746846` |

### 1.3 新解常量/字面量（全部实读）

| 地址 | 内容 | 用途 |
|---|---|---|
| `0xDD194C` | `L"t"` | **唯一附加参数名**（`sub_747E10` 内 `sub_402880`） |
| `unk_EEEF88` = `0xEEEF88` | `L"="` | 参数序列化：键值分隔符 |
| `unk_EEEF8C` = `0xEEEF8C` | `L"&"` | 参数序列化：参数间分隔符 |
| `0xEEEFC0`（符号名 **`szHeaders`**） | `L"Content-Type: application/x-www-form-urlencoded\r\n"` | `sub_BB5A80` 里传给 `WinHttpSendRequest` 的头缓冲（**代码中无写入点**，仅 `sub_BB5A80@0xbb5afb` 引用） |
| `0x120A98C`（符号名 **`dwHeadersLength`**） | int | 同上（仅 `sub_BB5A80@0xbb5aeb` 引用） |
| `0xD91C48` | `L"POST"`（后接 `param6…param1` 串表） | `sub_BB5A80` 方法名比较；亦被 `sub_690430/6907B0/690CF0`、`sub_BB5C10` 引用 |
| `0xDD1034` | `L"E01_ServerSelect"` | 子控件名 |
| `0xDD1058 / 0xDD1084 / 0xDD10C0` | `./settings/authsv.csv` / `_wegame.csv` / `_stg.csv` | 本地三选一 |
| `0xDD1818 / 0xDD1878 / 0xDD18E8` | `http://ms.patch1.9you.com/launcher/authsv.csv` / `_wegame.csv` / `_stg.csv` | 远端三选一 |
| `0xD912FC` | `L"GET"` | 方法 |

---

## 2. 状态机

### 2.1 `CLoginWindow` 侧（复核 N2，本项补充位语义）

| 字段 | 偏移 | 位 | 置/清 | 含义 |
|---|---|---|---|---|
| 标志 | `this+376`(0x178) | bit1 `0x2` | `sub_747E10` 入口 `|= …` 按 `a2` | 本次请求**是否"刷新"** |
| 标志 | `this+376` | bit2 `0x4` | 置：`sub_747E10`；清：`sub_7472E0(len!=0)` | **HTTP 在飞**（唯一防重发手段，**无重试计数**） |
| 结果位 | `this+372`(0x174) | `0x1000`/`0x4000` | `sub_7472E0` | 拉取结果 |
| 就绪 | `this+380`(0x17C) | — | — | !=0 才解析响应 |

触发源 3 个：① `sub_746B40`（构建期本地池）② `sub_748190`（窗口初始化 `a2=0`）③ `sub_7485F0 case5`（用户刷新 `a2=1`）。

### 2.2 HTTP 侧

```
[空闲] → request(vt[3]) → [入队 sub_BB2280] → [64ms 轮询 sub_BB0B30] → [发 sub_BB5A80]
   → HEADERS(200) → READ_COMPLETE(EOF) → sub_BB5480(通道号=15, 成功) → sub_AFD080 → sub_7472E0 → sub_746DC0
   → 清空 map → 逐行 sub_746710 重建 → sub_744570/sub_745210 刷新 UI
失败（错误位 / 空体 / 非 200）⇒ sub_BB5480 走失败分支：`__CxxThrowException(1, __TI1H=0xFFB8C0)` + `sub_AFD080(0,0)`（**不清空 map**）
```

---

## 3. 逐字段表 ★核心

### 3.1 HTTP 请求逐字段（本次新解）

| 项 | 值 | 类型/长度 | 含义 | 取值域 | 证据 |
|---|---|---|---|---|---|
| 方法 | `GET` | `wstring` | — | 固定 | `sub_747E10` push `0xD912FC` |
| scheme | `http` | — | 明文 | `WinHttpCrackUrl` 输出 | `sub_BAFBD0` |
| host | `ms.patch1.9you.com` | `wstring` ≤256 | 主机名 | — | `sub_BAFBD0` `a2` |
| user / pwd | `""` | `wstring` ≤128 | URL 内嵌凭据（无） | — | `sub_BAFBD0` `a3`/`a4` |
| path | `/launcher/authsv.csv`（或 `_stg` / `_wegame`） | `wstring` ≤2083 | 请求路径 | 3 选 1 | `sub_BAFBD0` `a5` |
| extra（query） | `""` | `wstring` ≤1000 | URL 里的 `?…`（**URL 串中本就没有**） | — | `sub_BAFBD0` `a6` |
| **port** | **80** | `int` | ★URL 无显式端口 ⇒ WinHTTP 默认 80 | — | `sub_BAFBD0` `*a7 = nPort` |
| scheme 标志 | ⚠️ | `bool` | `sub_BAFBD0` 末行 `*a8 = (nScheme == INTERNET_SCHEME_GOPHER)`（IDA 枚举疑似错认，实际意义应为"是否某 scheme"） | — | ⚠️待验证 |
| **附加参数** | `t = <GetTickCount()>` | 名 `wstring` + 值 `DWORD` | 防缓存时间戳 | `0…0xFFFFFFFF` | `sub_747E10`（`0xDD194C`=L"t" + `GetTickCount`） |
| 参数序列化形态 | `t=1234567`（多参数 `k=v&k1=v1`） | 文本 | 键/值均 **URL-encode** | — | `sub_BB35E0` + `unk_EEEF88/8C` + `sub_BB3450` |
| 请求头 | `Content-Type: application/x-www-form-urlencoded\r\n`（常量 `szHeaders`） | 常量 | `sub_BB5A80` 引用，**无写入点** | — | xref：只有 `sub_BB5A80` |
| 体 | 无（GET） | — | — | — | — |
| 超时 | 3s×4（resolve/connect/send/receive） | — | — | — | `sub_BB6260` |

**★未定（不影响私服，但记录）**：`sub_BB5A80` 里"参数串 `sub_BB35E0` 的产物"最终是**头**还是**体**，取决于 `*(req+56)` 与他处对 `szHeaders/dwHeadersLength` 的赋值——**这两个全局在代码里只有 `sub_BB5A80` 引用、无写入点** ⇒ 常量头 + ⚠️ 参数串去向待验证（见 §5.1）。

### 3.2 响应（S→C）逐字段

| 项 | 值 | 说明 | 证据 |
|---|---|---|---|
| 状态码 | 必须 **200** | 非 200 ⇒ 写 `L"status != 200\n"`(`0xEEF054`) ⇒ 失败分支 | `sub_BB5C10` |
| 体 | **与本地 CSV 完全同格式**（见 §3.3） | 复用同一 tokenizer + 同一行回调 `sub_746710` | `sub_746DC0` |
| 头 | 只需 `Content-Type: text/*`（客户端不校验） | ⚠️未验证 | — |
| 空体 | `len==0` ⇒ 走 `sub_746DC0(0,0)`（清列表/失败态路径） | `sub_7472E0` | — |
| 通道号 | `15` | `*(req+28)`；只有 15 走 authsv | `sub_BB15E0`/`sub_BB5480` |

### 3.3 `authsv*.csv` 逐列（★字节级，已实读归档）

**列定义（解析器只读 0..4 共 5 列）**

| 列 | 索引 | 类型（文件文本） | 解析函数 | 目标字段 | 取值域 | 必须非零? |
|---|---|---|---|---|---|---|
| 组ID | 0 | 整数串 | `sub_BBB370(row,0)`=`atoi` | `pair+0`（map 键） | ≥0；`0` 合法但会成为 map 首项 | ✅ 建议 ≥1 |
| 组名 | 1 | UTF-8 文本 | `sub_BBB4F0(row,1)`→`sub_BBB130` | `pair+4`（`wstring` 28B） | 任意；UI 显示 | ⚠️可空 |
| IP/主机 | 2 | UTF-8 文本 | `sub_BBB4F0(row,2)`→`sub_402310(x,0,-1)` | `Server+0`（`wstring` 28B） | 主机名或点分 IP | ✅ 必须（空 ⇒ 不可连） |
| 端口 | 3 | 整数串 | `sub_BBB370(row,3)` 截断为 `u16` | `Server+0x1C` | 0…65535 | ✅ 必须 |
| 图标ID | 4 | 整数串 | `sub_BBB370(row,4)` | `pair+48` | 图标索引（**0 = 无图标**，实测 stg 表第 4 列留空 ⇒ 0） | ⚠️可空 |

**解析规则（逐条，全部有代码证据）**

| 规则 | 行为 | 证据 |
|---|---|---|
| 行分隔 | `"\n"`（`asc_D6AAB8`@`0xD6AAB8`） | `sub_BBBEE0` |
| 字段分隔 | `,`（行对象内部分列） | `sub_456D90` 按 28B 步长取列 |
| **注释行** | 列 0 首字符 == `'#'`(35) ⇒ **整行跳过** | `sub_746710`：`if (*v5 == 35) v12 = 0` |
| **空行** | 列 0 长度 == 0 ⇒ 跳过 | `sub_746710`：`!*(_DWORD*)(sub_456D90(v18,0)+20)` |
| 列超范围 | `sub_BBB370` 返回 **0**（不崩） | 边界 `(a1+116)-(a1+112))/28` |
| 同组多行 | 不新建组；`Server` push_back 进 `group+32` 的 vector **（顺序 = 文件出现顺序）** | `sub_744680` 命中 ⇒ `sub_745F90` |
| 排序 | map 按 **组ID 升序**（UI 呈现顺序） | `map<int,…>` |
| 端口截断 | `int → u16`（`v28` 是 `__int16`） | `mov [.. var_64], ax` |
| 大小写/空白 | **不 trim**：`atoi` 容忍尾随空白/`\r`；但组名/IP 的空白会**原样保留** | `sub_CC6876`=`atoi` |
| CRLF | `\r` 会**留在最后一列**；`atoi` 不受影响 ⇒ 用 CRLF 安全，但别把 `\r` 混进 IP | §3.3 规则 8 + `sub_456D90` |

**实文件字节（归档 `unpackdat/settings/`，本项目已改成私服口径）**

```
authsv.csv                                  236B
  #認証サーバーリスト,\r\n
  #グループID,グループ名(UI表示用),認証サーバーIPアドレス,認証サーバーポート番号,画像ID\r\n
  #CBTテストサーバー,\r\n
  1,技术测试区    ,127.0.0.1,30000,1\r\n
  2,第二,,,2\r\n

authsv_stg.csv                              572B   ← 第 4 列（图标）留空 ⇒ 图标 0
  1,技术测试区,127.0.0.1,30000,\r\n

server/datafiles/region/authsv.csv（服务端种子，单区）
  #本机（只保留一个大区）\r\n
  1,技术测试区,127.0.0.1,30000,\r\n
```

> ⚠️ 注意：`authsv_stg.csv` 的表头写的是 `アイコンID`（图标ID），`authsv.csv` 的表头写 `画像ID`（图像ID）——**同一列**（列 4），只是文案不同；实文件第 4 列**可以为空**（⇒ 0）。
> ⚠️ `authsv_develop.csv`（2.69KB）是**开发服**表：同一 `组ID` 连续两行同 IP（如 `1,…,30090` ×2）⇒ 该组 `vector<Server>` 会有**两个相同元素**（客户端不去重）。

### 3.4 `ServerGroup` / `Server` 内存布局逐字段（★本次给出偏移证据）

**map 值 = `std::pair<const int, ServerGroup>`，总 **52B**

| 偏移(pair) | 偏移(group) | 类型 | 长度 | 含义 | 来源列 | 证据 |
|---|---|---|---|---|---|---|
| `+0` | — | `int` | 4 | **组ID**（map 键） | 0 | `v30 = sub_BBB370(row,0)` → `sub_744680` 作键 |
| `+4` | `+0` | `std::wstring` | 28 | **组名** | 1 | `sub_4029E0(v31, v29, 0, -1)`（`v31` 相对 `v30` = `+4`） |
| `+32` | `+28` | `std::vector<Server>` | 16（`begin/end/cap`，本 build 用 3 指针） | **该组服务器表** | 2/3（每行 1 元素） | `sub_745F90(a2+8)` 内的 `a2+32`；元素步长 `>>5`=32B |
| `+48` | `+44` | `int` | 4 | **图标ID** | 4 | `v31[11] = v10`（`v31`=`+4` ⇒ `+4+44=+48`）；`sub_745C50` 拷贝 `this[12]` |

**`Server`（vector 元素，32B）**

| 偏移 | 类型 | 长度 | 含义 | 来源列 | 证据 |
|---|---|---|---|---|---|
| `+0` | `std::wstring` | 28 | **IP / 主机名** | 2 | `sub_402310(&elem, &列2wstring, 0, -1)` @`0x7468a0` 附近 |
| `+0x1C` | `uint16` | 2 | **端口** | 3 | `mov [esp+118h+var_64], ax` @`0x7468dd`；`var_64` 相对元素起点(0x94) = `+0x1C` |
| `+0x1E` | pad | 2 | 对齐 | — | 步长 `>>5` |

**对照：另一路"标题画面默认池"`./settings/sv_add[_stg].txt`（`sub_A89930`）**

| 偏移 | 类型 | 长度 | 含义 | 与 authsv 的差异 |
|---|---|---|---|---|
| `+0` | `std::string`（**ANSI**，SSO 判定 `< 0x10`） | 28 | 地址 | authsv 用 `wstring`；此处是单字节串 |
| `+0x1C` | `uint16` | 2 | 端口 | 同 |

**`HttpParameters`（附加参数表）**

| 偏移 | 类型 | 含义 | 证据 |
|---|---|---|---|
| `+0` | vftable `HttpParameters::vftable`(`0xEEEF5C`) | — | `sub_BB3920` |
| `+4` | 红黑树头指针 | 节点 `+65` = 哨兵标志；节点含 键(串) / 值对象 | `sub_BB3920`、`sub_BB35E0`/`sub_BB09C0` 遍历 |
| `+8` | `size_t` 计数 | 参数个数 | `this[2]` |

**值对象（`sub_BB2860` 构造，可由 `sub_BB2FD0` 转文本）**

| 偏移 | 含义 |
|---|---|
| `+0` | 类型：1..4（由 `sub_BB2860` 内 `+24 = 15` 的串对象与 `sub_BB2730` 联合决定）⚠️ |
| `+8` | 值负载（`u8` / 串 / 指针，按类型） |
| `+20`/`+24` | 串长度 / 容量（**15** ⇒ `std::string` SSO） |

> ⚠️ `t` 的值对象的**类型号**未确证（`sub_BB33C0` 内看到局部写 `4`，而 `sub_BB2FD0` 的 `case 4 = default 不输出`）⇒ §5.1。

---

## 4. 期望"服务端"回包（本地 HTTP :8899 转发器）

| 项 | 要求 | 说明 |
|---|---|---|
| 监听 | `http://ms.patch1.9you.com:80/launcher/authsv.csv`（本项目用 PAC + `server/net_redirect.py` 的本地 :8899 接管） | 见 `topics/12 §八` |
| 响应码 | **200** | 非 200 ⇒ 客户端抛异常 + 但**本地池仍可用** |
| 响应体 | `text/csv`，**与 §3.3 同格式 5 列** | 复用同一回调 |
| 关键路径 | `/launcher/authsv.csv`（正式）/ `_stg` / `_wegame` 三选一，按 `sub_A1E840()/sub_A1E880()` | 本 build 私服走**正式**分支 ⇒ 只需 `/launcher/authsv.csv` |
| 参数 | `?t=<ticks>` 可**完全忽略**（查询串同样被忽略） | 但若转发器只按**路径**匹配，必须容忍 query |
| 数值来源 | 与归档 `settings/authsv.csv` **保持一致**（组ID=1 / IP=127.0.0.1 / 端口=30000） | 端口即同一进程的 auth 端口 |

---

## 5. 待研究 / 未定

1. **⚠️ `t=<ticks>` 的最终去向（头 or 体）**：`sub_BB5A80` 中 `szHeaders`(`0xEEEFC0`) 与 `dwHeadersLength`(`0x120A98C`) 在**全 IDB 内只有 `sub_BB5A80` 一个代码引用、无写入点** ⇒ 它们只能是常量头（`Content-Type: application/x-www-form-urlencoded\r\n`）；
   而 `sub_BB35E0` 产出的参数串被写入一个**未在反编译里显式使用**的 `std::string`（`dwTotalLength` 疑似其 `_Mysize`）。
   ⇒ 结论待定：**"参数串是否为请求体/头"无法静态闭合**（需要一次抓包或 `eval_expression` 读 `0xEEEFC0`/`0x120A98C` 运行值）。
   **对私服无影响**：转发器忽略 query/头即可。
2. **⚠️ `sub_BB5A80` 分支方向**：`sub_408530(method, 0, len, L"POST", 4)` 的**实参映射**（`this` 与 `a2` 谁是谁）IDA 反编译不自洽（出现 `this=0`）⇒ "GET 走哪一支"未定。
3. **⚠️ 值对象类型号**（§3.4 末）与 `sub_BB2FD0` 的 4 个 `case` 的对应关系。
4. **⚠️ 组名/IP 的源编码**：列是 `std::wstring`（宽化），但 CSV 编码（UTF-8 无 BOM？GBK？）与宽化代码页未确认（与 `topics/16` 的数据表方言结论需对齐）。
5. **⚠️ `off_110B128` 列类型表**（`sub_BBBB70(...,a5=off_110B128, a6=3)`）：`a6=3` 语义未定（N2 §5.4 遗留）。
6. **⚠️ `sub_BB5480` 失败分支 `throw int 1`** 的捕获点未定位（N2 §5.6 遗留）。
7. **⚠️ 通道号 2/3/0 的 URL**：`wmode.txt`(`0xF5D8DC`)/`fmode.txt`/`dmode.txt`/`remote/config.txt`/`ClientCheck/config.xml` 5 串在 IDB 内 `xrefs_to = 0`（N2 结论保留）。本项**未新证**。
8. **⚠️ `this+376` 的初值与 `sub_7472E0` 清位时机**（N2 §2.2）未逐指令核对。

---

## 6. 对服务端落地的影响

1. **认证服列表两处必须同时正确**（缺一即"列表为空"）：
   - 归档内 `data/settings/0000.dat` 的 `settings/authsv.csv`（VFS 读，**等长改写**；散装磁盘文件**不被读取**）；
   - 若启用 HTTP 接管：`/launcher/authsv.csv` 必须 200 + 同格式体。
2. **端口就是同一进程的 auth 端口（30000）**：客户端拿到的 `(IP, 端口)` 直接用于 `:30000` 连接 ⇒ **CSV 的端口必须等于 Go 服务端 auth 监听端口**（否则连不上，且表现为"选完区卡住"）。
3. **组数与图标**：`组ID` 升序决定 UI 行序；**只保留 1 组 1 行**（如服务端种子 `region/authsv.csv`）即可减少客户端 UI 分支。
4. **HTTP 请求可安全忽略**：`t=<ticks>` 与任何头都不需要正确应答；只要 **路径匹配 + 200 + 5 列 CSV**。
5. **非 200 不会致命**：失败只置状态位、**不清 map** ⇒ 本地池仍在（这是私服可靠性的保险）。
6. **本项不含任何游戏内报文**：`authsv` 全程 HTTP，与 `:30000/:30001/:30002` 的 iVCE 报文链**完全解耦** ⇒ 服务端实现次序上可以最后做。

---

## 7. 证据索引（可回溯）

| 结论 | 证据 |
|---|---|
| 5 列 + 各列去向 | `sub_746710` 全文（`0x74682a` col0 / `0x746846` col1 / `0x746898` col2 / `0x7468dd` col3 / `0x7468f1` col4） |
| `'#'` 跳过 / 空行跳过 | `sub_746710` `0x7467ad` 附近 |
| 组存在则 push_back | `sub_744680` 返回值与 `_Myhead` 比较（`0x746909`~`0x74692e`） |
| 52B / 32B | `v31[11]`(=`+48`)、`sub_745F90(a2+8)`→`a2+32`、步长 `>>5` |
| WinHttpCrackUrl | `sub_BAFBD0`（`0xD66578`） |
| `t` 参数 | `sub_747E10`：`0xDD194C`=L"t"（`get_string`） + `GetTickCount` |
| 序列化 `k=v&` | `sub_BB35E0` + `unk_EEEF88`=L"="、`unk_EEEF8C`=L"&"（py_eval 宽串扫描） |
| URL-encode | `sub_BB3450` 全文（`%`=37、fill `'0'`=48） |
| 常量头 | py_eval：`DataRefsTo(0xEEEFC0)` = 仅 `sub_BB5A80@0xbb5afb`；`0xEEEFC0`=L"Content-Type: application/x-www-form-urlencoded\r\n" |
| `L"POST"` | `0xD91C48` 字节 `50 00 4f 00 53 00 54 00` |
