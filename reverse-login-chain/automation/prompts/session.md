# session.md · 单次研究会话指令（每个自动化会话的 prompt）

你在执行「机动战士敢达Online · 登录入口 → 战斗大厅」**全链逆向**工程的一次研究会话。
工程根：`f:\9ymsgo\9you\`　｜　工作目录：`f:\9ymsgo\9you\reverse-login-chain\`

> ★会话**不限时长**，一直研究到**完成当前工作项**为止，不要因为时间而草草收尾。

## 第一步（读进度）

读 `f:\9ymsgo\9you\reverse-login-chain\workqueue.json`，拿到 `currentItem`（本次要研究的工作项）。

## 第二步（研究）

依次读取并严格执行：

1. `f:\9ymsgo\9you\reverse-login-chain\automation\prompts\common.md` —— **会话公约（必读，含铁律与产出规范）**
2. `f:\9ymsgo\9you\reverse-login-chain\workqueue.json` —— 进度真相源，取 `currentItem`
3. `f:\9ymsgo\9you\reverse-login-chain\formats\全链报文总表.md` —— 已知规格总表
4. 该工作项相关的 `nodes\*.md`、`detail\W*.md`、`.codebuddy\memory\topics\{08,10,14}.md`

然后用 **IDA Pro MCP**（`http://127.0.0.1:13338/mcp`，IDB `unpacked\GundamOnline_CHINA_v15.exe.i64`，基址 `0x400000`）
完成 `currentItem` 的研究，产出：

- `detail\W<NN>-<名>.md`（按 common.md §5.1 骨架，**逐字段表是核心产物**）
- 更新 `formats\全链报文总表.md`（改状态、补体长、指向明细、记录冲突/作废）
- 追加 `automation\runs.log` 一行
- 更新 `workqueue.json`（本项状态 / `currentItem` / `sessionCount` / `sessionLog`）
- 更新 `progress.json`（`updatedAt`/`runCount`/`lastRun`/`currentBlockers`）
- 追加 `.codebuddy\memory\YYYY-MM-DD.md`（当天进展）

## 第三步（收尾：创建下一个会话任务）

**完成本项研究、所有产出文件写完后**，用 `automation_update` 的 `suggested create` 创建**下一个会话**的
一次性任务（10 分钟后运行）：

```
mode               = "suggested create"
name               = "全链逆向·续跑（<下一项 currentItem>）"
cwds               = ["f:/9ymsgo/9you"]
status             = "ACTIVE"
scheduleType       = "once"
scheduledAt        = <当前时间 + 10 分钟>      # ISO 8601，如 "2026-09-15T03:10"
prompt             = 见下方【会话 prompt 全文】（原样复制）
```

> ★**只在会话【完成后】创建一次**下一个任务（不要会话开头就建、不要重复建），否则任务列表堆积。

最终回复 ≤200 字：本项结论 / 关键证据（地址·字节·实测）/ 下一项是什么。

## 铁律提醒（违反会让进程死掉）

- 客户端**任何断点都不能下**（软件/硬件/条件断点都会触发反外挂退出）；只允许**纯读内存**与服务端日志。
- 不改客户端配置；不删既有知识库；不猜字段（不确定写 `⚠️待验证`）。

---

## 【会话 prompt 全文】（创建下一个任务时原样复制到 `prompt` 字段）

```
你在执行「登录链全链逆向（登录入口 → 战斗大厅）」项目的一次研究会话（不限时长，研究到完成当前工作项为止）。
请依次读取并严格执行以下文件（不要跳过）：
1) f:/9ymsgo/9you/reverse-login-chain/automation/prompts/common.md      （会话公约：节奏/铁律/产出规范）
2) f:/9ymsgo/9you/reverse-login-chain/automation/prompts/session.md     （本次会话指令）
3) f:/9ymsgo/9you/reverse-login-chain/workqueue.json                    （进度真相源：currentItem）
4) f:/9ymsgo/9you/reverse-login-chain/formats/全链报文总表.md            （已知规格总表）

要求：
- 只推进 workqueue.json 的 currentItem 一项，研究到完成；产出 detail/W<NN>-*.md（逐字段表为核心）+ 更新总表 + 收尾四件套。
- 目标粒度：每个报文都能回答「方向/通道/ID/发送函数/接收case/体逐字段(偏移·类型·长度·含义·取值域)/期望应答/应答体/异常处理/证据」。
- 禁止在客户端下任何断点；不改客户端配置；不猜字段。
- ★会话【完成后】才创建下一个 once 任务（scheduledAt = 当前时间 + 10 分钟）；不要会话开头建、不要重复建。
完成后按 common.md §5 收尾。
```
