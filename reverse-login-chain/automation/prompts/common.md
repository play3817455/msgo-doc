# common.md · 「登录入口 → 战斗大厅」全链逆向 · 会话公约（v3，2026-09-15 起）

> **每个自动化会话必读**。执行顺序：① 读 `workqueue.json` → ② 读本文件 → ③ 读 `session.md` → ④ 干活 → ⑤ 收尾（§7）。
> v3（2026-09-15 定案）：**会话不限时长**，研究到完成当前工作项为止；**会话【完成后】才创建下一个 `once` 任务
> （`scheduledAt = 现在 + 10 分钟`）作为下一轮**。**严禁在会话开头就建下一个任务**（否则任务列表堆积）。

---

## 1. 项目与总目标

- 工程路径：`f:\9ymsgo\9you\reverse-login-chain\`
- 客户端 IDB：`unpacked\GundamOnline_CHINA_v15.exe.i64`（基址 `0x400000`，Hex-Rays 可用）
- **总目标**：把「**输入账号密码 → 进入战斗大厅（可出击）**」这条链路上**每一个报文、每一个字段、每一个偏移、
> 每一处汇编逻辑与状态迁移**都研究到"能照着写出服务端"的粒度。
- **产出四件套**（每项都必须有）：
  1. **汇编逻辑**：函数地址（`sub_XXXXXX`）、调用链、分支条件、数据结构偏移
  2. **状态机**：状态字段位置、取值、迁移条件
  3. **报文规格**：方向/ID/发送函数/接收 case/**体逐字段表（偏移·类型·长度·含义·取值域）**/期望应答/应答体/异常处理
  4. **数值与枚举**：每个参数的合法取值、必须非零项、枚举名↔值对应

---

## 2. 会话节奏（★v3 核心）

| 项 | 值 |
|---|---|
| 会话时长 | **不限**（研究到完成当前工作项为止，不设 10 分钟上限） |
| 会话间隔 | **10 分钟**（下一个任务 = 本会话完成时间 + 10min，`scheduleType: "once"`） |
| 每次推进量 | **只推进 `workqueue.json` 的 `currentItem` 一项**（做不完就标 `partial` 并写清已做到哪一步） |
| 任务创建 | **会话【完成后】**由本会话 `suggested create` 下一个 `once` 任务 |

### 2.1 ★续跑铁律（必做，顺序不可乱）

1. **会话【完成后】**（所有产出文件写完、收尾四件套完成）才用 `automation_update` 的 `mode="suggested create"`
   创建**下一个会话**任务：`scheduledAt = 现在 + 10 分钟`、`scheduleType="once"`、`cwds=["f:/9ymsgo/9you"]`、
   `status="ACTIVE"`；`prompt` 用 `session.md` 的【会话 prompt 全文】原样复制。
2. **★严禁在会话【开头】就建下一个任务**，也**严禁重复建**（一次会话只建一个）—— 否则 `once` 任务触发后
   系统不清理，任务列表无限堆积（2026-09-15 教训）。
3. `automation_update` 不可用 ⇒ 在最终回复里明确告知用户「需手动创建下一个会话任务（now+10min）」。

### 2.2 断链自愈

读 `workqueue.json` 后，若 `currentItem` 仍是 pending 但当前会话没有对应的「下一个任务」记录 ⇒ 按 §2.1
在本会话完成后补建。

---

## 3. 研究纪律（血泪教训，必须遵守）

1. **★反外挂铁律：客户端任何断点都不能下** —— 软件断点（`0xCC`）崩；**硬件断点（DR 寄存器）同样会被检测并让进程退出**；
   条件断点/命中计数同样不可靠。**只允许纯读内存**（`eval_expression` / `memory_read`）与服务端日志。
2. **判定"某 case 是不是目标报文"的唯一权威** = 该 `recv_*`/`send_*` **日志串的引用地址**落在哪个 case 区间；
   `cmp eax,<ID>; jz` 只说明"这个 ID 去哪个 case"，两者不一致时以日志串为准（`0xCCDF` vs `0xCE1A` 的教训）。
3. **每条结论必须带证据**：地址 / 字节 / 实测日志三者之一。没有证据的写「⚠️待验证」，不许伪装成结论。
4. **区分"已通"与"已解"**：实测能走通 ≠ 静态已搞清楚；本项目要后者。
5. **不许猜**：不确定的字段宁可留 `⚠️`，也不要用"看起来应该是"填上。
6. **不要修改既有知识库的既有结论**：新结论先写 `detail/` 或 `nodes/`，确认可信后**追加**到 `formats/全链报文总表.md`
   或 `.codebuddy\memory\topics\08`。**只增不改**，作废项标 `✗作废` 并给替代值。
7. **不做交互式动态操作**（自动化无法点界面）：需要实跑时用
   `server\logs\push.txt`（一行 `<ID> <bodyhex>`，挂在客户端每 ~4s 的 `0xD377` 节拍补发）或改服务端固化值后让客户端自动跑。

---

## 4. 工具

### 4.1 IDA Pro MCP（静态分析主力）

- 端点 `http://127.0.0.1:13338/mcp`；先 `fetch_mcp_resource ida://idb/metadata` 确认 IDB 已加载。
- 常用：`decompile`、`disasm`、`find_bytes`、`find_regex`、`xrefs_to`、`search_text`、`list_funcs`、
  `entity_query`、`py_eval`（可跑 `idautils.Strings()` / `DataRefsTo`）。
- **地址口径**：一律 `sub_XXXXXX`（VA，基址 `0x400000`）。

### 4.2 高频手法（已验证有效）

| 目的 | 手法 |
|---|---|
| 定位某字段的读写点 | 把字段偏移当 **disp32** 用 `find_bytes`（例 `app+0x1BDAC` → `AC BD 01 00`；`app+0x2C9` → `C9 02 00 00`） |
| 找应答 ID | `recv_xxx` 日志串 → `DataRefsTo` 得引用点 → 落在 `sub_B51930` 哪个 case 体 → 取"地址 ≤ 引用点且最大"的 case 入口 |
| 求体长 | 逐条数"线读"（`sub_B02DD0`=u32 / `sub_B02DF0`=u16 / `sub_B06230`=u8 / `sub_B06200`=8B / `sub_B02BA0`=NUL 有界串 / `sub_B41470`(+4) / `sub_B413B0`(+2) / `sub_B41A10`(+8)），末尾 `cmp cursor,end` 必须**恰到底**；用 `vt[0x78](N)` 分配量交叉校验（⚠️ N 可能是**结果结构体内存尺寸**，不一定是体长） |
| 追间接调用 | 虚表/方法表是间接调用（找不到 `call [reg+off]`）⇒ 按**数据 xref** 找表槽，再用**已知索引的邻居**做相对定位 |
| 内存取证 | 必须 `debug_init` 自己拉起客户端；**attach 模式下读内存不可用** ✗ |

### 4.3 其它

- `.codebuddy\dis9.py`（capstone）、`.codebuddy\kwscan.py` / `xref.py`；`.codebuddy\xtdlog.py`（XDt 日志解密，但 `XDt/*.log` 通常加密）。
- 客户端资源：`unpackdat\`；服务端：`server\internal\**`（Go）、`server\logs\`。
- `.codebuddy\memory\topics\坑与纪律.md`（**动手前必读**）、`topics\08`（协议权威表）、`topics\10`（地址速查）、
  `topics\14`（大厅 send ID 全表）。

---

## 5. 产出规范

### 5.1 工作项明细文档 `detail/W<NN>-<名>.md`

按下面骨架写（不确定的放 §5，标 `⚠️待验证`）：

```
# W<NN> · <标题>
> 状态 / 时间 / 会话序号 / 证据来源
## 0. 一句话结论
## 1. 汇编逻辑（调用链 + 关键函数表 + 数据结构偏移表）
## 2. 状态机（若有）
## 3. 报文/文件逐字段表  ← ★核心，必须逐字段：偏移·类型·长度·含义·取值域·必须非零?
## 4. 期望服务端回包（ID + 体逐字段 + 数值来源）
## 5. 待研究 / 未定
## 6. 对服务端落地的影响
```

### 5.2 追加到《全链报文总表》`formats\全链报文总表.md`

- 把本次新解出的报文行**改状态**（`⚠️待补` → `◐部分` → `✅已解`），补上体长/逐字段指向 `detail/W*.md`。
- 发现**冲突或作废**：在 §5 变更记录里加一行（日期/项/原因/替代值）。

### 5.3 追加 `automation\runs.log`

一行：`时间 | 工作项 | 动作 | 结果摘要 | 产物`。

### 5.4 更新 `workqueue.json`

- 本项 `status`（`done`/`partial`/`blocked`）、`doneAt`、`result` 摘要；
- `currentItem` = 下一个 `status == "pending"` 的项（全完 ⇒ `null`，`finished: true`）；
- `sessionCount` +1，`updatedAt`，`sessionLog` 追加一条。

### 5.5 进度与记忆

- `progress.json`：`updatedAt`/`runCount`/`lastRun`/`currentBlockers` 同步（阶段与工作项）。
- `.codebuddy\memory\YYYY-MM-DD.md`：追加当天进展（1~N 行，只写有长期价值的内容）。

---

## 6. 会话流程（照抄执行）

```
1. fetch_mcp_resource ida://idb/metadata                     # 确认 IDA 在线
2. read workqueue.json                                        # 拿 currentItem
3. （本会话完成后）suggested create 下一个 once 任务（now+10min）   # 见 §2.1
4. read workqueue.items[currentItem] + 相关 nodes/*.md + formats/全链报文总表.md
5. 用 IDA MCP 做本项研究（反编译/反汇编/字节搜索/xref）
6. 写 detail/W<NN>-*.md；更新 formats/全链报文总表.md
7. 追加 runs.log；更新 workqueue.json；更新 progress.json；追加 .codebuddy\memory\YYYY-MM-DD.md
8. 回复：本项做了什么 / 证据 / 下一步（≤200 字）
```

---

## 7. 禁止事项

- ❌ 一次会话推进多个工作项（保质量、可控）
- ❌ 下任何断点、改客户端 `.text`、用内存断点
- ❌ 改客户端配置（`sysinfo.ini` 等一律**只读**）
- ❌ 删除/覆盖既有知识库文件（只追加；作废要标注）
- ❌ 把未验证的推断写成结论
- ❌ 在会话【开头】创建下一个任务，或一次会话重复创建多个任务（只能在【完成后】建一个；**最高优先级禁止项**）
