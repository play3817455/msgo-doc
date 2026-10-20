# N2 · 平台认证 authsv（HTTP 链）

> 状态：`done`　｜　完成时间：`2026-09-14T03:05`　｜　负责任务：`automation/prompts/node-02.md`
> 结论来源：IDA Pro 静态分析（IDB `unpacked\GundamOnline_CHINA_v15.exe.i64`，基址 `0x400000`，Hex-Rays）；
> **本节点全程静态，无动态实证**（9you 域名已停服）。
> 地址口径一律 `sub_XXXXXX`（VA）。

---

## 0. 一句话结论

认证服务器列表 `authsv.csv` 由 **`IF::CLoginWindow`** 一个类全程负责，分两步、**本地在前、HTTP 在后**：

1. **本地（归档）池先就绪** —— `sub_746B40`（CLoginWindow 虚拟槽 `@0xDD1128`，控件构建期）经**游戏自有 VFS**
   读 `./settings/authsv.csv`（或 `_wegame` / `_stg`），用**与远端完全同一个**逐行回调 `sub_746710`
   装进 `CLoginWindow+340` 的 `std::map<组ID, ServerGroup>`。
2. **随后 HTTP 覆盖式刷新** —— `sub_748190`（槽 `@0xDD1718`，窗口初始化）/ `sub_7485F0`（槽 `@0xDD17C8`，事件 `case5`=刷新）
   → `sub_747E10` → `HttpMgrEx::request(通道号 15, L"GET", L"http://ms.patch1.9you.com/launcher/authsv.csv", stamp)`。
   成功 → `sub_BB5480(case15)` → `sub_AFD080` → `sub_7472E0` → `sub_746DC0`：**先 `sub_746A50` 整体清空 map，再逐行重建**；
   失败 → 只置状态位、**不清空** ⇒ 本地池原样保留。

**⇒ 修正 node-02 §5 判据的表述**：不是"先试 HTTP、失败后回落归档"，而是"**归档常驻 + HTTP 成功即整体替换（失败=保留归档）**"。
这正好解释私服侧"散装 CSV 无效、必须**等长改写归档**"：客户端**只**经 VFS(`sub_AEFD80`) 读 `./settings/authsv*.csv`，
它解析到归档 `settings_0000.dat` 内的同名条目；磁盘上再放一份散装文件**根本不会被读到**（§3.1、§4）。

传输层 = **WinHTTP 异步**，单例 `HttpMgrEx`（`dword_120A974`），会话超时 **3s×4**；
响应非 200 / 空体 / 请求错误 → `sub_BB5480` 走失败分支 `__CxxThrowException(1, &__TI1H)`（ThrowInfo `0xFFB8C0`）。

---

## 1. 汇编逻辑

### 1.1 入口与调用链

```
【A · 本地归档池】（构建期）
CLoginWindow.vt[槽 @0xDD1128] = sub_746B40
  ├ sub_402AD0(&v8, a2, L"E01_ServerSelect", 0x10)          组装子控件名
  ├ sub_762430(&v8, {sub_744DF0, this})                     建子控件；==0 ⇒ return 0（失败）
  ├ sub_BDC300(340, flt_EF0EF8, 0) → vtable = IF::CPopupBackgroundWindow::vftable
  ├ 路径选择（三分支，见 §1.3 环境判定）
  │   sub_A1E840()                ⇒ L"./settings/authsv_stg.csv"     (0xDD10C0)
  │   else sub_A1E880() != 3      ⇒ L"./settings/authsv.csv"         (0xDD1058)
  │   else (==3 = wegame)         ⇒ L"./settings/authsv_wegame.csv"  (0xDD1084)
  ├ sub_C3CF00(dword_11E3FCC)                                ◆ 全局“当前脚本/表上下文”
  ├ sub_AEFD80(&v8, 2, sub_746710, this, 1, 0)               ★VFS 载入 + 逐行回调（与 HTTP 同回调）
  └ sub_744570(this); sub_745210(this)                       列表收尾（滚动范围 + 条目录入）

【B · HTTP 拉取】（初始化 / 刷新）
CLoginWindow.vt[槽 @0xDD1718] = sub_748190   → sub_747E10(this, 0)   // 窗口初始化，a2=0
CLoginWindow.vt[槽 @0xDD17C8] = sub_7485F0                              // 事件处理
     case 5 → sub_747E10(this, 1)                                       // ★刷新（重试）
     case 6 → sub_BC46A0(0x1400004F)

sub_747E10(this, a2):
   ├ sub_BB3920(v6)                                                    构造附加参数对象（16B）
   ├ sub_402880(L"t", 1) + sub_BB33C0(v7, GetTickCount())              疑构造 "t=<ticks>"（防缓存/自定义头）⚠️
   ├ i  = sub_A1E840()        ⇒ URL = "http://ms.patch1.9you.com/launcher/authsv_stg.csv"    (0xDD18E8)
   │  else if sub_A1E880()!=3 ⇒ URL = "http://ms.patch1.9you.com/launcher/authsv.csv"        (0xDD1818)
   │  else                   ⇒ URL = "http://ms.patch1.9you.com/launcher/authsv_wegame.csv" (0xDD1878)
   ├ guard: this[376] & 0x4 已在飞 ⇒ return（不重复发）；否则 this[376] |= 0x4
   ├ bit: this[376] bit1(0x2) = a2                                      （0=首次，1=刷新）
   └ (*(*(HttpMgrEx)+12))(v4, 15, L"GET", URL, a5)                      ★HttpMgrEx::vt[3] = sub_BB22E0

HttpMgrEx::request = sub_BB22E0(this, a2=通道号, a3=方法, a4=URL, a5=附加参数)
   ├ if (*(this+4) == 0) return 0                                       未初始化
   ├ sub_BAFBD0(a4, ...)                                                解析 URL（8 输出）；失败 → sub_BAE500(GetLastError)
   ├ sub_4029E0(a3,0,-1); sub_4029E0(a4,0,-1)                           清空形参（移动进请求对象）
   ├ sub_BB09C0(&v15, *(a5+4), a5+4)                                    拷附加参数
   └ sub_BAF9B0() / sub_BAF350(...) / sub_BB2280(&v41) / sub_BAFA20()   加锁·建请求对象·入队·解锁

【C · 工作线程 / 传输】
HttpMgrEx+136 = CThread 成员；过程 sub_BAF680(CThread*, HttpMgrEx*)
   └ while (WaitForSingleObject(evt, 0x40)) vt[+32]()                   ★64ms 轮询
       轮询体 sub_BB1000（进入队列）/ sub_BB0B30（在飞队列）
         ├ sub_BB15E0 / sub_BB5A80 → WinHttpSendRequest(*(req+4)=hRequest, ...)
         └ 完成/错误 → sub_BB5480(req[7]=通道号, *(req+22)=错误位, *(req+24)=数据, req[8]=长度)
   WinHTTP 状态回调 sub_BB5FC0（经 sub_BB5880 ⊂ sub_BB5FE0 注册）
         ├ 0x00020000 HEADERS_AVAILABLE → WinHttpQueryHeaders(0x20000013 STATus_CODE|NUMBER)
         │     == 200 ⇒ WinHttpReadData；否则错误串 L"status != 200\n"（0xEEF054）
         ├ 0x00100000 SENDREQUEST_COMPLETE → WinHttpReceiveResponse
         ├ 0x00080000 READ_COMPLETE  → 收满/EOF ⇒ HttpMgrEx.vt[7]=sub_BAF7B0 “请求完成”
         ├ 0x00200000 REQUEST_ERROR  → HttpMgrEx.vt[6]=sub_BAF740
         └ 0x00400000 WRITE_COMPLETE → 写体后 Receive

【D · 响应分发（通道号 = HTTP 层的“路由标签”）】
sub_BB5480(a1=通道号, a2=错误, a3=数据, a4=长度)   __stdcall
  if ((BYTE)a2 || !a3 || a4<=0)                ← 失败：错误位 / 空体
       { v31 = 1; __CxxThrowException(&v31, &__TI1H); }        ★throw int 1（ThrowInfo 0xFFB8C0）
       switch(a1){ 0→sub_AFCFF0(1,..); 2→sub_AFD010(0,0); 3→sub_AFD030(0,0);
                  15→sub_AFD080(0,0); 4..14→sub_AFD050(a1-4,0,0); 1→return; }
  else （成功）
       switch(a1){ 0→sub_BB53C0(v21,a3,a4) 解析 XML(id/category/title/crowd/close, 逐条 sub_A42BA0);
                   2→sub_AFD010(a3,a4); 3→sub_AFD030(a3,a4);
                   15→sub_AFD080(a3,a4); 4..14→sub_AFD050(a1-4,a3,a4); 1→return; }

【E · case15 = authsv 专用链】
sub_AFD080(a1,a2) = sub_7472E0(a1,a2); if(!a2) sub_746DC0(0,0); return nullsub_1(a1);
   └ sub_7472E0(obj, len):  __RTDynamicCast(obj,0,rymUIControl,IF::CLoginWindow,0) 失败即退
        len!=0 ⇒ this[376] bit2 清；等结果位（this+372 的 0x1000/0x4000）
        len==0 ⇒ sub_746DC0(0,0)（空数据 = 清列表/失败态）
        len>0  ⇒ sub_747860(this,len) 并给 this+16*j 的表登记
              if (*(this+380)) { sub_C3CE40(...); sub_746DC0(len,len) }   ★真正解析
   └ sub_746DC0(a2=数据, a3=长度):
        sub_BBBD70(a2, a3)                     把响应体包成流对象
        sub_C3CF00(dword_11E3FCC)              选表上下文
        if (sub_AEDCF0(v7, v4, 1))   parse 失败 ⇒ 全部跳过（列表不动）
        sub_746A50(this + 340)                 ★★ 清空 map（整体替换的关键）
        if (!sub_BBBB70(v4, 2, sub_746710, this, off_110B128, 3))   ★逐行回调
             { sub_744570(this); sub_745210(this); }                 列表收尾
```

### 1.2 关键函数表

| 地址 | 名称/身份 | 作用 | 关键参数/偏移 |
|---|---|---|---|
| `sub_746B40` | **本地池加载 = CLoginWindow 虚拟槽** `@0xDD1128` | 建 `E01_ServerSelect` 控件 + VFS 读 `./settings/authsv*.csv` | 路径 3 串 `0xDD1058/84/C0`；回调 `sub_746710` |
| `sub_747E10` | **URL 组装 + 发起 HTTP** | 选 URL、置标志、调 `HttpMgrEx.vt[3]` | `a2`=0 首次 / 1 刷新；`this[376]` bit1/bit2 |
| `sub_748190` | CLoginWindow 虚拟槽 `@0xDD1718` | 窗口初始化 → `sub_747E10(this,0)` | |
| `sub_7485F0` | CLoginWindow 虚拟槽 `@0xDD17C8` | 事件；`case5` → `sub_747E10(this,1)` 刷新 | |
| `sub_BAF820` / `0xBB1AF0` | `HttpMgrEx` getter / ctor | 单例取用 / 构造 | getter 只有 `return dword_120A974`（无锁） |
| `sub_BB20B0` | **HttpMgrEx 单例创建者（唯一）** | 加锁 → 懒创建 → 解锁 | `sub_BDC300(164,…)` + `sub_BB1AF0()` |
| `sub_BAF830` | 单例销毁 | 加锁→`(*(*p))(p,0)`+`sub_BDC340(p)`→`=0`→解锁 | `off_110B038` = 单例保护锁对象 |
| `dword_120A974` | `HttpMgrEx*` 单例指针 | —— | |
| `0xEEEF64` / `0xEEEF38` | `HttpMgrEx` / `HttpMgr` vtable | —— | `[0]=0xBB1C00 [1]=0xBB0610 [2]=0xBB0990 [3]=0xBB22E0 [4]=0xBAFE40 [5]=0xBB1000 [6]=0xBAF740 [7]=0xBAF7B0 [8]=0xBB1C20` |
| `sub_BB22E0` | **请求入口（vt+12 = 通道号/方法/URL/附加）** | 解析 URL → 建请求 → 入队 | `a2`=通道号、`a3`=方法、`a4`=URL、`a5`=附加 |
| `sub_BB15E0` / `sub_BB1C20(vt[8])` | 入队（URL 变体，无 method/stamp） | 供 `sub_BAFE40` 等 | 存 `req+28 = 通道号` |
| `sub_BAFE40` | 通用 GET 请求 helper（vt[4]） | 造 `L"GET"` → vt[3] | |
| `sub_BAF350` | 建请求对象 | `WinHttpSetOption(h,0x26 PROXY,{…},0xC)` | 代理来自 IE 设置（`sub_BAF0B0`） |
| `sub_BB5A80` | 发送 | `WinHttpSendRequest(*(req+4),hdr,len,0,0,total,ctx)` | `req+4` = HINTERNET hRequest |
| `sub_BB5FE0` | 建请求句柄 | `WinHttpOpenRequest` + `WinHttpSetStatusCallback` | `fnInternetCallback` |
| `sub_BB5880` | 会话回调注册 | `WinHttpSetStatusCallback(session,…)` | |
| `sub_BB5C10` | **WinHTTP 状态回调** | 见 §1.1【C】；非 200 写 `L"status != 200\n"` | 状态码比较 `== 200` |
| `sub_BB6260` / `sub_BB6280` | 会话建立 | `WinHttpSetTimeouts(3000,3000,3000,3000)` / `WinHttpOpen(0,0,0,0,0x10000000 ASYNC)` | 超时 **3s×4** |
| `sub_BAF680` | **工作线程过程** | 64ms 轮询驱动 `vt[+32]` | `WaitForSingleObject(evt,0x40)` |
| `sub_BB1000` / `sub_BB0B30` | 队列轮询体 | 发请求 / 派完成事件 | 日志格式串 `L"connection%u request%u process%u complete%u laster%u step%u"` |
| `sub_BB5480` | **响应分发（通道号 → handler）** | 见 §1.1【D】；失败 `throw 1` | `__TI1H`=`0xFFB8C0`；抛点 `0xBB550D` / `0xBB575A` |
| `sub_AFD080` / `sub_7472E0` | case15 前段 | RTTI 校验 + 状态位 | `__RTDynamicCast`→`IF::CLoginWindow` |
| `sub_746DC0` | **case15 解析（清空+重建）** | `sub_AEDCF0` → `sub_746A50` → `sub_BBBB70` | 失败则不动列表 |
| `sub_746A50` | **清空 map** | 清 `this+340` 分组表 | |
| `sub_AEDCF0` | 响应体 tokenizer（与数据表同一解析器） | `(表对象, out, 1)` | |
| `sub_BBBB70` | **CSV 行迭代器** | 逐行调回调；回调返回非 0 = 停 | `a2=2`、`a5=off_110B128`(列类型表)、`a6=3` |
| `sub_BBBEE0` | 读一行 | `sub_CCC87F(buf, asc_D6AAB8)`，**行分隔符 = `"\n"`** | `asc_D6AAB8="\n"`（`0xD6AAB8`） |
| `sub_BBBFD0` | 行迭代初始化 | `this+124 = a5`、`sub_BBBCD0(this+40,256)` 行缓冲 | 256B 行缓冲 |
| `sub_746710` | **逐行回调（本地/远端共用）** | 解析 5 列 → 建 `ServerGroup`/`Server` 入 map | 见 §1.3 |
| `sub_456D90` | 取第 i 列（wstring） | SSO 判定 `cap < 8`（⇒ **列 = `std::wstring`**） | |
| `sub_BBB370` | 取第 i 列 → int | `atoi`（`sub_CC6876`） | |
| `sub_BBB4F0` | 取第 i 列 → 赋给 wstring | `(dst, row, idx)` | |
| `sub_744680` | map 查找 | 返回迭代器（含 `_Myhead` = end 比较） | map 在 `CLoginWindow+340` |
| `sub_745F90` / `sub_745A90` / `sub_745440` | `std::vector` push_back / 拷贝 / 元素拷贝 | 元素步长 **0x20(32B)**（`>>5`） | |
| `sub_745B90` / `sub_745C50` / `sub_745BE0` | 记录 ctor / 拷贝 / dtor | 记录 = `pair<const int, ServerGroup>` | |
| `sub_744570` | 列表滚动范围收尾 | 用 `this+348` 计数设 `this+356` | |
| `sub_745210` | **列表填充（UI 呈现）** | 遍历 `this+344` 的 map → `sub_745010(组ID,组名,图标)` | 高亮比较 `this+364`；控件 `this+352` |
| `sub_AEFD80` | **游戏 VFS 载入 + CSV 逐行** | `(路径wstring, 2, 行回调, ctx, 1, 0)` | 与 N1 `account.ini` 同族（VFS） |
| `sub_A1E840` | 环境判定 A | `return byte_11FFAC4`（staging/测试位） | 选自 `_stg` |
| `sub_A1E880` | 环境判定 B | `return dword_1104680`（渠道号；**3 = wegame**） | 选 `_wegame` |
| `sub_A89930` / `sub_A89770` | **另一路"默认地址池"**（标题画面） | VFS 读 `./settings/sv_add[_stg].txt` → `vector<{std::string addr, u16 port}>` 随机取 1 | 元素 32B（`>>5`）；见 §3.1 |

### 1.3 数据结构

**`IF::CLoginWindow`（本节点用到的成员）**

| 偏移 | 类型 | 含义 |
|---|---|---|
| `+340` (0x154) | `std::map<int 组ID, ServerGroup>` | **服务器分组表**（`sub_746A50` 清空 / `sub_744680` 查找 / `sub_745210` 遍历） |
| `+344` (0x158) | `map::_Myhead` | 树头/end 哨兵（查找结果比较用） |
| `+348` (0x15C) | int | 计数（`sub_744570` 用来设滚动范围） |
| `+352` (0x160) | 控件 | 列表控件（`sub_745210` 录入条目；`+312` = 内部列表对象、`+276` = 每页数） |
| `+356` (0x164) | 控件 | 列表视图/滚动条（`sub_744570`） |
| `+364` (0x16C) | int | 当前/选中组 ID（`sub_745210` 高亮比较） |
| `+368` (0x170) | int 位域 | 标志（某处清 `0x4000`） |
| `+372` (0x174) | int 位域 | 状态位 `0x1000` / `0x4000`（`sub_7472E0` 读） |
| `+376` (0x178) | byte 位域 | **bit1(0x2)=本次是否为刷新(a2)；bit2(0x4)=HTTP 在飞 guard** |
| `+380` (0x17C) | 控件指针 | `sub_7472E0` 用其判定"列表控件已就绪"才解析（N1 记为账号下拉框，⚠️ 同一地址两处含义待核对） |

**`ServerGroup`（map 的值；= `std::pair<const int, ServerGroup>` 展开后的布局）**

| 偏移(pair) | 偏移(group) | 类型 | 含义 | 来源列 |
|---|---|---|---|---|
| `+0` | — | int | **组ID**（map 键） | 列 0 |
| `+4` | `+0` | `std::wstring`(28B) | **组名** | 列 1 |
| `+32` | `+28` | `std::vector<Server>`(16B) | **该组的服务器(IP,端口)列表** | 列 2/3（每行一个元素） |
| `+48` | `+44` | int | **图标ID** | 列 4 |

> 证据：`sub_746710` 写 `+0=sub_BBB370(row,0)`、`+4=sub_4029E0(&v31, v29)`（v29=列1）、
> `v31[11]=(+48)=sub_BBB370(row,4)`；`sub_745A90(a2+8)` 拷贝 **`a2+32`** 处的 vector；
> `sub_745C50` 拷贝 `this[12]=a2[12]`（= `+48`）。总长 **52B** = `pair<int, {wstring,vector,int}>`。

**`Server`（vector 元素，32B，步长由 `>>5` 证实）**

| 偏移 | 类型 | 含义 | 来源 |
|---|---|---|---|
| `+0` | `std::wstring`(28B) | **IP/主机** | 列 2（`sub_402310(&元素, &列2wstring, 0, -1)`，见 §4 证据） |
| `+0x1C`(28) | `uint16` | **端口** | 列 3（`mov [var_64], ax`） |
| `+0x1E`(30) | pad 2B | —— | 对齐到 32B |

**对照：`./settings/sv_add*.txt` 的元素**（另一路地址池，`sub_A89930`）

| 偏移 | 类型 | 含义 |
|---|---|---|
| `+0` | `std::string`(28B，SSO 判定 `< 0x10`) | 地址（**ANSI**，与 authsv 的 wstring 不同） |
| `+0x1C` | `uint16` | 端口 |

**HttpMgrEx 请求对象**（`sub_BB0B30` 消费）

| 偏移 | 含义 |
|---|---|
| `+0` | vtable（`vt[+4]` 用于释放） |
| `+4` | `HINTERNET hRequest` |
| `+20` | 状态 byte（`==1` 表示已发） |
| `+22` | **错误 byte**（非 0 → `sub_BB5480` 失败分支） |
| `+24` | 响应缓冲对象（`+20`=数据指针、`+24`=长度） |
| `+28` | **通道号**（= `sub_BB5480` 的 `a1`） |
| `+32` | 长度 |

---

## 2. 状态机

### 2.1 HTTP 请求生命周期（`HttpMgrEx` 侧）

```
[空闲] --request(vt3)--> [入队] --64ms轮询(sub_BB0B30)--> [已发 WinHttpSendRequest]
   --> [HEADERS_AVAILABLE]
         ├ code==200 --> [READ_COMPLETE 累数据] --EOF--> 完成 → sub_BB5480(成功) → 业务 handler
         └ code!=200 --> 错误串 L"status != 200\n" --> 完成(错误) → sub_BB5480(失败) → throw 1
   --> [REQUEST_ERROR] --> 完成(错误) → sub_BB5480(失败) → throw 1
```

### 2.2 `CLoginWindow` 侧（本节点视角）

| 状态字段 | 位置 | 取值 | 含义 | 迁移条件 |
|---|---|---|---|---|
| 帧标志 | `this+376` | bit1(0x2) | 本次请求是否"刷新"（`a2`） | `sub_747E10` 入口赋值 |
| 帧标志 | `this+376` | bit2(0x4) | **HTTP 在飞**（防重复发） | 置：`sub_747E10`；清：`sub_7472E0`（`len!=0` 时） |
| 结果位 | `this+372` | `0x1000`/`0x4000` | 拉取结果（清/置） | `sub_7472E0` |
| 就绪 | `this+380` | !=0 | 列表控件已就绪 ⇒ 才解析响应 | `sub_7472E0` |

> 触发源共 3 个：① `sub_746B40`（本地池，构建期）；② `sub_748190`（窗口初始化，`a2=0`）；
> ③ `sub_7485F0 case5`（**用户刷新/重试**，`a2=1`）。**没有**"固定 ×N 自动重试"循环（见 §5.1）。

---

## 3. 文件与格式

### 3.1 本地文件

| 文件 | 路径 | 格式（字节级） |
|---|---|---|
| `authsv.csv` | VFS `./settings/authsv.csv`（归档 `settings_0000.dat` 内） | 见下方《authsv CSV 规格》 |
| `authsv_wegame.csv` | VFS `./settings/authsv_wegame.csv` | 同上（渠道号 `sub_A1E880()==3` 时） |
| `authsv_stg.csv` | VFS `./settings/authsv_stg.csv` | 同上（`sub_A1E840()` 为真时） |
| `sv_add.txt` / `sv_add_stg.txt` | VFS `./settings/sv_add[_stg].txt` | `地址,端口`（每行 1 条）；**另一路"默认地址池"**，`sub_A89930` 随机取 1 条用于标题画面 |

**《authsv CSV 规格》**（`组ID,组名,IP,端口,图标ID`）

| 列 | 索引 | 类型 | 目标字段 |
|---|---|---|---|
| 组ID | 0 | int | `ServerGroup+0`（map 键） |
| 组名 | 1 | `std::wstring` | `ServerGroup+4` |
| IP | 2 | `std::wstring` | `Server+0`（该组下每行追加 1 个 `Server`） |
| 端口 | 3 | int→**uint16** | `Server+0x1C` |
| 图标ID | 4 | int | `ServerGroup+48` |

- 行分隔符 = **`"\n"`**（`asc_D6AAB8`，`0xD6AAB8`）；字段分隔在行对象内部（`,`）。
- **注释/表头：第 0 列首字符 == `'#'`（35）⇒ 整行跳过**（`sub_746710`：`*(_BYTE*)v5 == 35`）。
  空行（列对象 size==0）同样跳过。
- 解析器把文本变成 **`std::wstring`** 列（`sub_456D90` 的 SSO 判定为 `cap < 8`）⇒ 组名/IP 需要"宽化"读入。
- **同组多行**：同 `组ID` 的第 2..n 行不新建分组，只把 `(IP,端口)` **push_back 进该组 vector**（`sub_744680` 命中 → `sub_745F90(existing+0x30, &元素)`）。
- **排序**：`sub_744680` 是 map 的查找/插入（树，按组 ID 有序）⇒ 列表按组 ID 升序。
- ⚠️ 与 `topics/16`（数据表 CSV 方言）不同：本表由 tokenizer **先按 `\n` 切行**，故 CRLF 的 `\r` 会**留在最后 1 列**；
  实践上把"图标ID"列写成 `5` 即可（`atoi` 对尾部 `\r` 不敏感），但**不要**在 IP/组名列依赖 CRLF。

### 3.2 网络报文（HTTP）

| 方向 | 方法 | URL | 说明 |
|---|---|---|---|
| C→S | `GET` | `http://ms.patch1.9you.com/launcher/authsv.csv` | 正式 |
| C→S | `GET` | `http://ms.patch1.9you.com/launcher/authsv_wegame.csv` | 渠道 3 |
| C→S | `GET` | `http://ms.patch1.9you.com/launcher/authsv_stg.csv` | staging |
| S→C | 200 + body | 同《authsv CSV 规格》 | 非 200 ⇒ 客户端写 `status != 200\n` 并 **抛异常** |

- 请求附加参数：`sub_BB3920` + `L"t"` + `GetTickCount()`（疑 `t=<ticks>` 防缓存 / 自定义头）⚠️ 待验证。
- 传输：WinHTTP **异步**，`WinHttpSetTimeouts(3000,3000,3000,3000)`；`WinHttpOpen(..., WINHTTP_FLAG_ASYNC)`；
  代理 = IE 设置（`WinHttpSetOption(hRequest, WINHTTP_OPTION_PROXY=0x26, {type, proxy, bypass}, 12)`）。
- 自定义 header 串：`L"Content-Type: application/x-www-form-urlencoded"` 等（`0xEEEF9C` 起，供 case0 的 XML 使用）。

### 3.3 `sub_BB5480` 通道号 ↔ handler（case ↔ URL）

| 通道号 | 成功 handler | 失败 handler | 身份（本节点确证度） |
|---|---|---|---|
| `1` | `return`（空实现） | `return` | 保留/未用 |
| `2` | `sub_AFD010` → `dword_11E3F50->vt[+44](data,len)` | 同，参数 0 | 管理器文本 feed ⚠️ 具体 URL 未定（候选 `wmode.txt`/`fmode.txt`） |
| `3` | `sub_AFD030` → `dword_11E3F50->vt[+144](data,len)` | 同，参数 0 | 同上 ⚠️ |
| `0` | `sub_BB53C0` 解析 **XML**（键 `id`/`category`/`title`/`crowd`/`close`，逐条 `sub_A42BA0`，`dword_EEEFA8={-1,0,2,1,3}` 做 category 映射） | `sub_AFCFF0(1,…)` | **公告/客户端检查配置 XML**（键名与 `://ms.patch1.9you.com/ClientCheck/config.xml` 相符）⚠️ URL 待定 |
| `4`..`14` | `sub_AFD050(通道号-4, data, len)` → `sub_ADC500(400+idx, data, len)` | `sub_AFD050(idx,0,0)` | **11 个数据表下载槽（400..410）** ⇒ 与 N6 `download_list.csv` 对应 |
| `15` | `sub_AFD080(data,len)` → `sub_7472E0` → `sub_746DC0` | `sub_AFD080(0,0)` | ★**authsv**（`CLoginWindow`），URL 见 §3.2 |

> ⚠️ `wmode.txt`(0xF5D8DC) / `fmode.txt`(0xF5D934) / `dmode.txt`(0xF5D98C) / `remote/config.txt`(0xF5D9D4) /
> `ClientCheck/config.xml`(0xF5DA2C) 这 5 个串在 IDB 内 **`xrefs_to = 0`**（说明它们是**启动器/补丁模块**或经
> 指针表引用，**不是** `HttpMgrEx` 直接 `push` 的常量）。故"通道号 ↔ 这 5 个 URL"的一一对应**本节点未能确证**，
> 只确证 **15 = authsv**（唯一调用者 `sub_747E10`）。其余通道的 URL 归 **N6**（数据表下载）与启动器侧。

---

## 4. 实测证据（全部为静态证据；无动态）

| 项 | 证据 |
|---|---|
| 三个 URL 的确切字面量 | `0xDD1818`=`"http://ms.patch1.9you.com/launcher/authsv.csv"`；`0xDD1878`=…`authsv_wegame.csv`；`0xDD18E8`=…`authsv_stg.csv`（`get_string`/字节 dump） |
| 方法串 | `0xD912FC` = `L"GET"`（字节 `47 00 45 00 54 00 00`） |
| 所选 URL 与 `_stg`/`wegame` 的映射一致（**两处独立代码**） | `sub_747E10`（HTTP）与 `sub_746B40`（本地）分支条件与文件一一对应（均 `sub_A1E840()`→stg、`sub_A1E880()!=3`→正式、`==3`→wegame） |
| 通道号 15 是 authsv | `sub_747E10` 内 `push 0Fh` → `call vt+12`；`sub_BB5480 case 15 → sub_AFD080`；`sub_AFD080` 首步 `__RTDynamicCast(..., &IF::CLoginWindow RTTI)` |
| 请求对象字段（通道号存 `+28`） | `sub_BB15E0`：`*(_DWORD*)(v13+28) = a2`；`sub_BB0B30`：`sub_BB5480(v40[7], *(v40+22), …)` |
| **"清空 + 重建"证据** | `sub_746DC0`：`sub_746A50(this+340)` 在 `sub_BBBB70(...)` **之前** |
| **失败不清空** | `sub_AFD080(a1,0)` ⇒ `if(!a2)` 只走 `sub_746DC0(0,0)`；`sub_7472E0(len==0)` 路径**不调用** `sub_746A50` |
| 行分隔符 | `asc_D6AAB8` @`0xD6AAB8` = `0x0A 0x00`（`"\n"`），用于 `sub_CCC87F(buf, "\n")` |
| `#` 行规则 | `sub_746710` @`0x7467xx`：`if (*(_BYTE*)v5 == 35) v12 = 0`（35=`'#'`），且 `cap<8` 判定 ⇒ 列是 `std::wstring` |
| `Server` 元素 = 32B | `sub_745F90`/`sub_745A90` 元素步长 `>> 5`；`sub_745F90(this+0x30, &elem)` 命中已存在组时的 push_back |
| 端口落点 `+0x1C` | disasm `0x7468dd` 附近：`mov [esp+118h+var_64], ax`，而 `var_64` 相对元素起点(0x94)为 `+0x1C` |
| IP 落点 `+0` | `sub_402310(&var_80(=0x94 元素), &var_F0(=列2 wstring), 0, -1)`（`0x7468a0` 附近） |
| 图标落点 `+48` | disasm `0x74697a`：`mov [esp+118h+var_14], ebp`，`var_14` 相对 `v30`(0xD0) = `+0x30`，即 `ServerGroup` 布局的 `pair+48` |
| 单例是懒创建 | `sub_BB20B0` 是 `sub_BB1AF0` 的**唯一**调用者，体为 `加锁 → if(!dword_120A974) 建 → 解锁` |
| getter 无锁 | `sub_BAF820` = `return dword_120A974;`（单指令） |
| 线程 = 64ms 轮询 | `sub_BAF680`：`while (WaitForSingleObject(evt, 0x40)) (*(*a1+32))(a1)`；`sub_BB1000` 内 `CThread` 成员在 `HttpMgrEx+136`（`this[34]`） |
| 超时 = 3s×4 | `sub_BB6260`：`WinHttpSetTimeouts(session, 3000, 3000, 3000, 3000)` |
| 非 200 行为 | `sub_BB5C10`：`WinHttpQueryHeaders(0x20000013)` → `if (status == 200) ReadData else 写 L"status != 200\n"` |
| **失败 → throw int 1** | `sub_BB5480`：`v31 = 1; sub_CC5664(&v31, &__TI1H)`；`__TI1H`=`0xFFB8C0`（被 `sub_BB5480`/`sub_BB4890`/`sub_BB4A70`/`sub_BB4B20`/`sub_AE8250` 引用） |
| 另一路默认池存在 | `sub_A89930`：`sub_A1E840()? ./settings/sv_add_stg.txt : ./settings/sv_add.txt` → `sub_AEFD80(path,2,sub_A89770,0,0,0)`；元素步长 `>>5`，`+24 < 0x10` ⇒ `std::string` |
| **负证据：无 ×N 重试计数** | `sub_747E10` / `sub_BB22E0` / `sub_7472E0` 内**未见**计数器与 `cmp …,4..6`；`sub_747E10` 的重复发保护只有 `this[376] & 4` 一个位 |
| **负证据：URL 串无 xref** | `xrefs_to(0xF5D8DC/934/98C/9D4/A2C)` 全部 `xref_count = 0` ⇒ 这 5 个 URL 不由 `HttpMgrEx` 直接使用 |

### 4.1 ⚠️ 修正记录（推翻了 node-02 的表述）

| 原表述（node-02/node-01） | 修正为 | 依据 |
|---|---|---|
| "客户端**先**试 HTTP、**失败后**回落归档内置池" | **归档池先常驻就绪；HTTP 之后覆盖式刷新；HTTP 失败=保留归档** | `sub_746B40` 在构建期即装载（同回调）；`sub_746DC0` 的成功路径才是 `sub_746A50` 清空；失败路径不触碰 map |
| "重试 ×4-6" | 未发现固定次数的自动重试；"重试"= 用户刷新（`sub_7485F0 case5`）或窗口重进（`sub_748190`）；单次请求受 3s×4 超时约束 | §4 负证据行 |
| "默认池在 `settings_0000.dat` 内（需等长改写）" | 一致，且给出了**原因**：只经 VFS `sub_AEFD80("./settings/authsv.csv")` 读，磁盘散装文件不被读取 | §3.1、`sub_746B40` 代码 |

---

## 5. 待研究 / 未定

1. **⚠️ 两处虚拟槽的运行时先后**：`sub_746B40`(槽 `@0xDD1128`) 与 `sub_748190`(槽 `@0xDD1718`) 的**实际调用顺序**由 UI 框架决定，
   静态未能证明"构建一定早于初始化"。若动态实测为"先 HTTP 后本地"，§0/§4.1 的先后结论需要收紧为"HTTP 成功即覆盖，与先后无关"。
2. **⚠️ 通道号 2/3 与 0 的 URL**：`wmode.txt`/`fmode.txt`/`dmode.txt`/`remote/config.txt`/`ClientCheck/config.xml`
   5 串无 xref，未能与通道号一一对应；`dword_11E3F50->vt[+44]`/`vt[+144]` 指向的管理器类身份未定。归 N6/启动器。
3. **⚠️ `sub_747E10` 的附加参数 a5**：`sub_BB3920` + `L"t"` + `GetTickCount()` 的最终字节形态（是否 `t=<ticks>` 头）未确证。
4. **⚠️ `off_110B128` 列类型表**：`[0]=0xF64228, [1..4]=0xF5D748("bad allocation"), [5]=0xEEF3B4("esWindow"), [6]=0xF5D748, [7]=0xF4EB4C`；
   `sub_BBBB70(...,a5=off_110B128, a6=3)` 中 `a6=3` 的语义（列数？模式？）未定；`0xF64228`/`0xF4EB4C` 指向的类型对象名未解析。
5. **⚠️ 组名编码**：列被解析成 `std::wstring`（宽化），但源文件的编码（UTF-8 无 BOM？GBK？）与宽化代码页未确认。
6. **⚠️ `sub_BB5480` 的 `throw 1` 捕获点**：未定位到 `catch(int)`（`__TI1H` 的 handler）；"抛出后列表是否被清/是否回退到错误 UI"未明。
7. **⚠️ `this+380` 双重语义**：N1 记为"账号下拉框"，本节点 `sub_7472E0` 用作"列表就绪判定"；需确认是同一控件还是 N1 偏移记错。

---

## 6. 对下游节点的影响

- **N3（access 握手）**：本节点确认**认证前的"选服务器"完全走 HTTP**，与 30000 连接的建立无耦合；
  `sub_43E2D0`(N1 的 state13) 才是连接步骤（`CGameStateStepUpdateConnectAuth`）——N3 应从那里切进去。
- **N6（大厅数据表下载）**：`sub_BB5480` 的 `case 4..14 → sub_AFD050(idx) → sub_ADC500(400+idx)` 就是大厅数据表下载的**落点数组**（400..410，共 11 槽），
  且复用**同一套 `sub_AEDCF0`+`sub_BBBB70`+`sub_456D90` CSV 解析**。N6 应从这里对接 `download_list.csv`；本节点已把"通道号=`req+28`"的传递链定位清楚。
- **N5（世界选择）**：`sub_745210` / `sub_745010` 是"按组渲染列表项"的通用模式，世界列表 UI 很可能同构，可复用 §1.3 的记录布局分析方法。
- **私服工程**：改"服务器列表"必须**等长改写归档内 `settings/authsv.csv`**（散装文件不被读取）；
  HTTP 端（`ms.patch1.9you.com/launcher/authsv.csv`）已停服且客户端**非 200 即抛异常**，故不要指望"删掉远端走本地"以外的路径——
  且**抛异常后本地池仍在**，这正是私服能只用归档就进列表的原因。
- **卡点/风险**：`sub_BB5480` 的 `throw 1` 无人捕获时可能直接冒泡到 UI 循环；若要复现"官方失败态"需要观察运行期表现（本节点无法动态验证）。
