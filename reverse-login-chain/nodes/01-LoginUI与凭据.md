# N1 · 登录界面与凭据采集

> 状态：`done`　｜　完成时间：`2026-09-14T02:07`　｜　负责任务：`automation/prompts/node-01.md`
> 结论来源：IDA Pro 静态分析（IDB `unpacked\GundamOnline_CHINA_v15.exe.i64`，基址 0x400000）；动态仅作证据补充并注明。
> 原始证据 dump：`.codebuddy\fsm.txt`、`ida_out6.txt`、`ida_out7.txt`、`ida_out9~15.txt`。

---

## 0. 一句话结论

登录界面类为 `IF::CLoginWindow`（派生自 `rhyme::rymUIControl`，vftable `??_7CLoginWindow@IF@@6B@` = `0xDD148C`）。
全流程由状态机 `sub_A88920`（登录 FSM tick，状态字段 = `this+4`）驱动：**state10** 用 UI 管理器控件 id=100 绑定登录窗口并读 `account.ini` 预填；**state11** 等窗口就绪并选中"记忆账号"；**state12** 轮询窗口结果码 `vt[197]`，用户点登录后把账号框→`FSM+20`、密码框→`FSM+48`、记忆勾选框→`FSM+76`（均为 `std::wstring`/`byte`，**全程无 MD5、无哈希、无加密**）；**state13** 弹等待窗并挂 `CGameStateStepUpdateConnectAuth` 步骤；**state14** 等步骤完成并关闭登录窗；**state15** `sub_43E3F0` 把 `FSM+20/+48` 转 UTF-8 落到 `app+28`（账号）/`app+541`（密码），创建 `CGameStateStepUpdateLoginAuth` 步骤（`sub_430D00`，**N2 的切入点**），并按 `FSM+76` 回写 `account.ini`。

---

## 1. 汇编逻辑

### 1.1 入口与调用链

```
主循环(每帧) → sub_A88920(this=登录FSM, dt)                 [VA 0xA88920, 0xA88E20 跳转表, 状态=this+4]
  ├─ state10 ─ (*(UIMgr vt+60))(dword_11E3EAC)                       取控件容器
  │             → sub_CC61BB(容器, 100, 0, 0, &rhyme::rymUIControl)   __RTDynamicCast(id=100)
  │             → (*(win vt+652))(win, &IF::CLoginWindow RTTI, 0)     绑定/创建 CLoginWindow(槽163)
  │             → sub_433E60(app)                                     读 account.ini（见 §3.1）
  │             → sub_42D320(app)                                     = app[114204]（PW_SAVE）
  │             → sub_747090(win, flag)                               设置"记住密码"勾选框
  │             → if(PW_SAVE) sub_430CD0(app,&w) / sub_747040(win,账号,空)  预填账号框
  ├─ state11 ─ sub_A88280() → CLoginWindow；if((*(vt+660))(win) && !(win[376]&4))
  │             app[1056]==-1 ? sub_747020(win) : sub_747080(app[1056])   选中默认/记忆账号
  ├─ state12 ─ sub_A88280() → CLoginWindow
  │             if( sub_7470E0(win) || timer>=limit )                      窗口关闭/超时
  │                r = (*(win vt+788))(win) - 1                          取结果码(槽197)
  │                if(r==1){ sub_747D70(win,&w) → FSM+20 账号                (0xA88B07)
  │                          sub_79A860(win,&w) → FSM+48 密码                (0xA88B3D)
  │                          sub_7470A0(win)    → FSM+76 记忆位；state→13 }  (0xA88B6B)
  │                if(r==0) (*(dword_11E3F78 vt+12))(dword_11E3F78, 4)     取消/中止流程
  │             else state = 100                                          (见 §2 ⚠️)
  ├─ state13 ─ sub_43E2D0(app)  ★N2：弹等待窗(控件183/217/250/177,149,202)
  │                             + 建 CGameStateStepUpdateConnectAuth 步骤
  ├─ state14 ─ sub_42D330(app)=sub_AF6EF0 步骤完成判定 → (*(UIMgr vt+20))(UIMgr,100) 关登录窗
  └─ state15 ─ sub_43E3F0(app, FSM+20, FSM+48)  ★N2 起点（提交登录）
                 ├─ 账号 wstring → UTF-8(sub_BC3FB0) → sub_CC65C6(app+28 ,513)  
                 ├─ 密码 wstring → UTF-8(sub_BC3FB0) → sub_CC65C6(app+541,513)  
                 ├─ sub_430D00(账号,密码) = CGameStateStepUpdateLoginAuth ctor（账号→+20,密码→+533）
                 ├─ sub_43E130(&step, obj)  注册步骤
                 └─ 回到 state15 分支：sub_42D310(app,FSM+76) → sub_434140(app) 写 account.ini；state→16
```

### 1.2 关键函数表

| 地址 | 名称/身份 | 作用 | 关键参数/偏移 |
|---|---|---|---|
| `sub_A88920` | 登录 FSM tick | 驱动 state 0~23 / 100~101 / 998~999 | `this+4`=状态；`this+80`=计时器 |
| `sub_433E60` | 读 account.ini | 读 `ID/PW_SAVE`/`ID`/`AUTH` | → `app+114204`,`app+28`,`app+1056` |
| `sub_434140` | 写 account.ini | 写 `ID/PW_SAVE`/`ID`/`AUTH` | 源：`app+114204`,`app+28`,`app+1056` |
| `sub_43E3F0` | 提交登录（state15） | 账号/密码 → `app+28`/`app+541`；建 LoginAuth 步骤 | ecx=app；a2=FSM+20；a3=FSM+48 |
| `sub_430D00` | **CGameStateStepUpdateLoginAuth ctor** ★N2 | 账号→`obj+20`，密码→`obj+533`（各 513B UTF-8） | vftable `CGameStateStepUpdateLoginAuth::vftable` |
| `sub_43E2D0` | **state13 等待** ★N2 | 建 `CGameStateStepUpdateConnectAuth` 步骤 + 等待窗 | `CWaitingUIWindow` |
| `sub_A88280` / `sub_A882D0` | 取窗口 | 取 CLoginWindow / CWorldSelectWindow | UIMgr `vt+32`, id=100/2 |
| `sub_CC61BB` | dynamic_cast 辅助 | MSVC `__RTDynamicCast` 包装 | `(obj, offset, baseRTTI, derivedRTTI, throw)` |
| `sub_747090` / `sub_7470A0` | 记忆勾选框 set/get | `win[93]` 槽195/196 | → `app[114204]` / `FSM+76` |
| `sub_747040` | 写账号/密码框 | `win[86][268]`/`win[87][268]` 槽1024 | |
| `sub_747D70` / `sub_79A860` | 取账号/密码框文本 | `sub_747730(win)` / `sub_747730(win[87])` | 基址 0x747D70 / 0x79A860 |
| `sub_747730` | 通用"取控件文本" | `control[67] → (*(*+700))(&wstring)` | wstring→out |
| `sub_7470E0` | 窗口关闭/就绪探测 | `sub_783590() \|\| (*(win[96]+660))(win[96])` | 槽165 |
| `sub_747020`/`sub_747080`/`sub_745530` | 账号下拉框 | 默认项 / 选第 idx 项并回写 `app+1056` | `win[95]`,`win[88]`,`win[89]` |
| `sub_430CD0` | `app+28`→wstring | `sub_BC4110(&w, app+28)` | |
| `sub_BC3FB0` / `sub_BC4110` | 编码转换 | wide→UTF-8(std::string,CP=0xFDE9) / UTF-8→wide | |
| `sub_CC65C6` | 有界字符串拷贝 | `(dst, cap, src, n)` | |
| `sub_46F2F0`/`46F080`/`46E590`/`46F170`/`46E240`/`46F250` | **游戏自有 VFS INI 读写** | 构造 reader / 打开 / 读值 / 写值 / 落盘 / 关闭 | 见 §3.1 |
| `sub_402AD0` | `std::wstring::assign` | ecx=this(wstring) | |
| `sub_587C90` | `CPcSpecOptionTable` ctor | 采 CPU/内存/显卡（**非 9you 键**） | 见 §4 |
| `sub_A1F8A0` / `sub_A215F0` | 通用注册表脚本引擎 | RegOpen/Create/Delete/Set/Query | 见 §4 |
| `sub_746B40` | authsv.csv 加载 ★N2 | `./settings/authsv*.csv` | 路径串 0xDD1058/0xDD10C0/0xDD1084 |
| `sub_747E10` | authsv.csv 远程下载 ★N2 | `http://ms.patch1.9you.com/launcher/authsv.csv` | 串 0xDD1818 |

### 1.3 数据结构

**登录 FSM 对象**（`sub_A88920` 的 `this`，全局指针 `dword_11E3EE0`）：

| 偏移 | 类型 | 含义 |
|---|---|---|
| `+4` | int | 状态（见 §2） |
| `+8` | int | 重试计数/窗口句柄（state998→`sub_435C40(app, this+8)`） |
| `+20` | `std::wstring`(28B) | **账号**（state12 写入） |
| `+48` | `std::wstring`(28B) | **密码**（state12 写入） |
| `+76` | byte | **记住密码**（state12 写入，state15 回写 app） |
| `+80` | float* | 计时器指针（state12 累加 dt） |

**app 单例**（`dword_11E3EA8`，主流程对象）：

| 偏移 | 类型 | 含义 |
|---|---|---|
| `+28` | char[513] | 账号 UTF-8（读/写 account.ini，state15 由 FSM+20 更新） |
| `+541` | char[513] | 密码 UTF-8（state15 由 FSM+48 更新） |
| `+1056` (0x420) | int | 记忆账号索引（= `AUTH`），-1 = 无 |
| `+1136` (0x470) | int | 选中世界索引（state17） |
| `+1352` (0x548) | vector | 世界列表 |
| `+114200` (0x1BE18) | byte | 登录/自动标志（state15 清 0） |
| `+114204` (0x1BE1C) | byte | **ID/PW_SAVE** |

**CLoginWindow**（`IF::CLoginWindow`；vftable `0xDD148C`；RTTI TypeDescriptor `0x101E14C`）：

| 偏移 | 类型 | 含义 |
|---|---|---|
| `+344` (`this[86]`) | 控件包装 | 账号输入框；`[+268]` = 文本控件 |
| `+348` (`this[87]`) | 控件包装 | 密码输入框；`[+268]` = 文本控件 |
| `+372` (`this[93]`) | 控件 | 记住密码勾选框（槽195 set / 槽196 get） |
| `+380` (`this[95]`) | 控件 | 账号下拉框（槽163 = vt+652） |
| `+384` (`this[96]`) | 控件 | 就绪/关闭探测（槽165 = vt+660） |
| `+376` | byte 标志 | `&4` 位参与 state11 就绪判定 |
| `vt[163]` `0x748190` | 方法 | 设窗口类型（带 RTTI 参数） |
| `vt[165]` `0xBE5940` | 方法 | 就绪判定 |
| `vt[197]` `0xBE5B90` | 方法 | **取登录结果码**（state12） |

> 控件文本读写：读 = `sub_747730`（`control[67]` → 虚槽 `+700` 取 wstring）；写 = 虚槽 `+1024`。

---

## 2. 状态机

`sub_A88920` 的 `this+4` 取值与迁移（`0xA88960: cmp eax,66h; ja default` ⇒ 0~102 有效）：

| 状态 | 含义 | 迁移条件 |
|---|---|---|
| 0 | 初始 | → 10（直接落到 state10 体） |
| 10 | 打开/绑定 CLoginWindow + 读 account.ini + 预填 | 无条件 → 11 |
| 11 | 等窗口就绪，选中记忆账号 | `(*(vt+660))(win) && !(win[376]&4)` → 12 |
| 12 | 等登录结果 | 见下方分支（成功 → 13） |
| 13 | 弹等待窗 + 建 ConnectAuth 步骤 | `sub_43E2D0` 后 → `sub_43E2D0` 末 `sub_744570/sub_745210`；state13 体 `sub_43E2D0(app)` 后无条件 → 14 |
| 14 | 等 ConnectAuth 完成 | `sub_AF6EF0` 为真 → `关登录窗(id=100)` → 15 |
| 15 | 提交登录（建 LoginAuth 步骤）+ 写 account.ini | `sub_43E3F0` 返回真 → 16；假 → 998 |
| 16 | `sub_A88300()` 状态过渡 | → 17 |
| 17 | 弹出 CWorldSelectWindow（id=2）并填充世界列表 | → 18 |
| 18 | 等世界选择结果 | `vt[197]==1 && sub_74AAA0 && sub_42D360` → 23 |
| 19 | `sub_A88330()` 过渡 | — |
| 20~22 | 大厅登录准备 | → `sub_42D3C0(); sub_433670(4)` |
| 23 / 102 | 等待态 | 空转 |
| 100 | `sub_6AC760(0)` 重置 | → 101 |
| 101 | `sub_6ABFF0()` | 完成 → `sub_42FE00(1)` → 下一态 |
| 998 | `sub_435C40(app, this+8); state=999` | |
| 999 | `sub_42E250(app)` | 真 → `this+8=0; state=10`（**回到登录**） |
| 其它 | 返回 1（未处理） | |

**state12 分支（0xA88A9A–0xA88B76）**：

```
条件A = sub_7470E0(win)  ||  (timer += dt; limit >= timer)      // limit=*(app阶段表[132]+152)
if (条件A)
    r = (*(win vt+788))(win) - 1                                // vt[197] 结果码
    if (r == 1) { 账号→FSM+20; 密码→FSM+48; 记忆位→FSM+76; state→13 }   // 结果码==2 = 登录
    else if (r == 0) (*(dword_11E3F78 vt+12))(dword_11E3F78, 4)         // 结果码==1 = 取消 → 流程管理器切状态4
    // 其它 r：不迁移
else state = 100
```

⚠️ `sub_7470E0` 与 `else → state=100` 支路的**精确语义**（"取消/关闭 vs 超时"）待动态确认，见 §5。

---

## 3. 文件与格式

### 3.1 本地文件 `account.ini`

- 文件名（宽串 `L"account.ini"` @ `0xD681B8`）；**读写全部走游戏自有 VFS**：
  `sub_46F2F0`(构造 reader,栈对象) → `sub_46F080(reader, path, 1, 1)`(打开) →
  `sub_46E590(reader, &val)`(读) / `sub_46F170(reader, &val)`(写) →
  `sub_46E240()`(落盘) → `sub_46F250(reader)`(析构/关闭)。
- **不使用** Win32 `GetPrivateProfileString`/`WritePrivateProfileString`（导入表 + 全串扫描均 0 命中）。
- 字段（键名宽串地址 → 语义）：

| 键 | 字面量地址 | 读（`sub_433E60`） | 写（`sub_434140`） |
|---|---|---|---|
| `ID/PW_SAVE` | `0xD681A0` | `app+114204 = atoi(v)!=0`（`sub_CC6876`） | `L"1"`/`L"0"`（按 `app+114204`） |
| `ID` | `0xD68198` | `sub_BC3FB0`(UTF-8→wchar) → `sub_CC65C6(app+28, 513, s, 512)` | `sub_BC4110(app+28)` → 宽串 |
| `AUTH` | `0xD6818C` | `app+1056 = atoi(v)` | `wsprintfW(buf, L"%d", app+1056)` |

- 写入顺序：`ID/PW_SAVE` → `ID` → `AUTH` → `sub_46E240()` 落盘 → 关闭。
- ⚠️ 本 exe 只按"键名"取值，未见 section 解析；文件是否含 `[section]` 待运行时抓一次实证。

> 注：`formats\README.md` 原有条目写作 `AUTH,1 / ID,<账号> / ID,PW_SAVE,1`；本节点实测键名为 `AUTH` / `ID` / `ID/PW_SAVE`，语义为 `AUTH=<索引整数>`、`ID=<账号字符串>`、`ID/PW_SAVE=<0|1>`。

### 3.2 网络报文

**本节点不产生报文**（state15 只"创建步骤对象"，实际发包在 N2）。交接给 N2 的两个步骤对象：

| 步骤类（vftable 名） | 构造点 | 载荷 |
|---|---|---|
| `CGameStateStepUpdateConnectAuth` | `sub_43E2D0` (state13) | 连接/鉴权握手 |
| `CGameStateStepUpdateLoginAuth` | `sub_430D00` (state15) | `obj+20`=账号(513B UTF-8)、`obj+533`=密码(513B UTF-8) |

**结论（重要）**：客户端在进入网络前**不对账号/密码做任何哈希**，直接以明文 UTF-8 装入 auth 步骤对象。
因此 node-01 §3.3 假设的"客户端 MD5 生成点"在本 exe **不存在**（见 §5.1 与 §4 负证据）。

---

## 4. 实测证据

| 项 | 证据 |
|---|---|
| FSM 全貌 | `sub_A88920` pseudocode + disasm（`0xA88920–0xA88DD8`，跳转表 `0xA88DD8`，case 索引表 `byte_A88E20`） |
| 调用链地址 | 见 `.codebuddy\fsm.txt` 的 disasm（`0xA8898E` 推 RTTI、`0xA889BF call sub_433E60`、`0xA88B07 call sub_747D70`、`0xA88B3D call sub_79A860`、`0xA88B6B call sub_7470A0`、`0xA88C08 call sub_434140`） |
| account.ini 键名 | `off_D6818C='AUTH'`、`off_D681B8='account.ini'`、`aIdPwSave='ID/PW_SAVE'`、`aId_2='ID'`（宽串实测） |
| INI 走自有 VFS | 导入表无 `*PrivateProfile*`；读写经 `sub_46E590`/`sub_46F170` |
| **MD5 缺失（负证据）** | 全 exe：无 `0123456789ABC…`(T 表)、无 `67452301…`(IV)、无 `"md5"` 串；`login` 路径亦无哈希调用 ⇒ 客户端不做 MD5 |
| **无 Win32 INI API（负证据）** | `GetPrivateProfileString`/`WritePrivateProfileString` 导入 0 命中 |
| **sysinfo.ini 缺失（负证据）** | 宽/窄串扫描：`sysinfo`/`Target_Url`/`Target_port`/`SP`/`GAME`/`GVERSION` 均 0 命中 |
| **9you 注册表键缺失（负证据）** | 宽/窄串扫描：`GOnline`/`SOFTWARE`/`gamever` 0 命中；仅 `.9you.com` URL（patch 服务器） |
| 注册表 API 分布 | `Reg*` 只出现在：`sub_587C90`（`CPcSpecOptionTable`：`RegOpenKeyExW(HKLM, "HARDWARE\DESCRIPTION\System\CentralProcessor\0\")` + `~MHz`(`ValueName`) + `ProcessorNameString`(`off_D7BCD0`) + `GlobalMemoryStatusEx` + WMI 显卡）；`sub_A1F8A0`/`sub_A215F0`（通用注册表脚本引擎）。**无 9you 键** |
| authsv 线索（N2） | `sub_746B40` 引用 `./settings/authsv.csv`(0xDD1058)/`authsv_stg.csv`(0xDD10C0)/`authsv_wegame.csv`(0xDD1084)；`sub_747E10` 引用 `http://ms.patch1.9you.com/launcher/authsv.csv`(0xDD1818) |

> 说明：以上负证据基于**主 exe 全段原始字节扫描**（`.rdata` 等），未覆盖运行期解密后的字符串；若客户端存在被加载的 DLL 或加密资源，需另行确认（见 §5）。

---

## 5. 待研究 / 未定

1. **⚠️ MD5 缺失的复核**：node-01 假设客户端做 MD5（对齐 `server\internal\protocol\protocol.go` 的 `LoginReq`：账号 15B + MD5 33B）。实测本 exe 无 MD5。需确认三选一：
   (a) MD5 位于某个被加载的 DLL；
   (b) `LoginReq`(9001) 属 9you 平台链（gate :1633）而非本 build 的 authsv 直连路径；
   (c) 哈希在 **N2** 的 `CGameStateStepUpdateLoginAuth` 内部（本节点只到"装入步骤对象"为止）。
2. **⚠️ `sysinfo.ini`/`Target_Url`/`Target_port`/`SP` 的读取点**未在本 exe 找到明文 ⇒ 疑在"敢达启动器"或加密资源内，需在 N2 前先定位 `SP`（决定走 9you 平台链 or Client_Start 链）。
3. **⚠️ `HKLM\SOFTWARE\WOW6432Node\9you\GOnline`（`path`/`gamever`）** 在本 exe 无明文键串 ⇒ 疑在启动器侧。
4. **⚠️ state12 的 `sub_7470E0` 语义与 `else→state=100` 支路**：需动态确认"点关闭按钮/取消"时到底走 `vt[197]==1`（流程管理器切状态4）还是 `state=100`。
5. **⚠️ `account.ini` 是否含 `[section]`**：静态只见键名，未见段名解析。

---

## 6. 对下游节点的影响

- **N2 切入点已就位**：
  - 连接步骤 `CGameStateStepUpdateConnectAuth`（`sub_43E2D0`，state13）；
  - 登录步骤 `CGameStateStepUpdateLoginAuth`（`sub_430D00`，state15）——账号在 `obj+20`、密码在 `obj+533`（明文 UTF-8）；
  - 服务器列表来源 = `sub_746B40`（`./settings/authsv*.csv`，按 `sub_A1E840()/sub_A1E880()` 选 staging/wegame/正式）+ 远程兜底 `sub_747E10`。
- **风险**：若 N2 沿用 server 的 `LoginReq = 账号15B + MD5 33B` 假设，与本节点"客户端无 MD5"冲突 ⇒ N2 必须先定位 `CGameStateStepUpdateLoginAuth` 的实际发包函数，确认认证体字段（明文？编码？）。
- **卡点**：`SP` 分支值来源未知，N2 需先解决 §5.2 才能判断走哪条认证链。
