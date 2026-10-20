# node-01 · N1 登录界面与凭据采集

> 本文是**本次任务**的专属指令。执行前先读 `common.md`（公共规则）与 `progress.json`。
> 产出：`nodes/01-LoginUI与凭据.md`

## 1. 目标

把「主窗口出现 → 登录窗口弹出 → 用户输入账号/密码 → 点登录 → 进入网络请求」这一段**静态讲清楚**。
这是全链起点，后续 N2 的切入点就在本节点末尾。

## 2. 入口线索（已在知识库中确认）

| 地址 | 身份 |
|---|---|
| `sub_A88920` | 登录流程 FSM tick，状态在 `this+4`；state **10** 打开 CLoginWindow、**11** 等窗口就绪、**12** 等登录结果（窗口 `vt[197]`）、成功后存用户名/密码 → 13 |
| 窗口/UI | CLoginWindow 类（需定位 vtable 与 ctor） |
| `sub_43E2D0` | state13 等待 |
| `sub_42D330` | state14 认证完成判定 |

## 3. 研究清单（逐条给结论 + 证据）

1. **CLoginWindow 定位**：vtable 地址、ctor、窗口创建调用点（state10 分支里）。
2. **控件 → 内存**：账号/密码输入框对象、取值路径、字符串编码（ANSI/UTF-16）与长度限制。
3. **MD5**：实现地址（是否标准 RFC1321）、调用点、输入（密码明文？加盐？）、输出形式（hex 小写？33B 填充？）。
   - 注意与 `server\internal\protocol\protocol.go` 的 `LoginReq` 布局对上（账号 15B + MD5 33B hex）。
4. **凭据落盘**：写 `account.ini` 的函数与字段（`AUTH` / `ID` / `ID,PW_SAVE`）；
   是否用 `WritePrivateProfileString`（找到调用点）；"记住密码/自动登录"分支的判定。
5. **`sysinfo.ini` 读取**：`Target_Url` / `Target_port` / `SP` / `GAME` / `GVERSION` 的读取函数与缓存位置；
   `SP` 如何决定走 9you 平台链还是 Client_Start 链（与 N2 衔接）。
6. **注册表**：`HKLM\SOFTWARE\WOW6432Node\9you\GOnline` 的读/写点（`path` / `gamever`）。
7. **状态机全貌**：state 10~13 的完整迁移条件与超时/取消路径（用户点关闭窗口会怎样）。

## 4. 产出要求

- 按 `nodes\_节点模板.md` 写 `nodes/01-LoginUI与凭据.md`，重点是把 §1.1 调用链画出来。
- 新增的文件格式（`account.ini` 字段、MD5 输入输出形式）追加到 `formats\README.md`。
- 可信的地址结论追加到 `topics\10-逆向地址索引.md`。

## 5. 完成判据

能回答：
- 账号/密码从控件到 `LoginReq` 报文的**完整数据流**（每一步的函数地址）；
- MD5 的确切输入与输出格式；
- `SP` 的值从哪里来、影响哪条分支。

## 6. 注意

- 若发现 state 10~13 与知识库描述不一致（state 编号/窗口槽位），**以静态实证为准并记录差异**。
- 本节点不涉及网络，不需要跑客户端；纯 IDA 静态分析即可完成。
