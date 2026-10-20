# node-06 · N6 大厅认证与数据表下载（30001）

> 执行前先读 `common.md` 与 `progress.json`。产出：`nodes/06-大厅认证与数据表下载.md`

## 1. 目标

把大厅连接（30001）上"version → lounge authenticate → **数据表串行下载泵（76 张表）** → 脚本 VM 执行"
的**完整机制**静态讲清楚。这是"数据只在服务器"这一现实的落地机制，也是大厅阶段必修课。

## 2. 入口线索（已在知识库中确认）

| 地址 | 身份 |
|---|---|
| `sub_B51930` | **lounge 协议报文分发器**（巨型，多张 switch） |
| `sub_B896A0` | `send_authenticate`（0xF24B，userid+otp） |
| `sub_B89BE0` 内 | `send_datafile_request`（0xF86A，filepath+hashval） |
| `sub_5760B0` | **串行下载泵**：取 `std::map<int id, wstring file>` 最左节点（= ID 升序） |
| `sub_576160` | **脚本 VM 装载**：按 filepath 查【脚本名→处理器ID(0~79)】映射 |
| `sub_BBBD70` | 设源码（`sub_BBBCD0(size)`，**size==0 ⇒ 报错** ✗） |
| `sub_AEDCF0` | 执行脚本（tokenizer `sub_AEDC30`） |
| `sub_BBBB370` | 取列为整型（列号 ≥ 总列数 ⇒ return 0，不报错） |

## 3. 研究清单

1. **lounge authenticate**：`0xF24B` 的参数（userid/otp 从哪来）、应答 `0xA5DA+u32×2` 的语义
   （**为什么体必须 8B，4B 会解析失败**）。
2. **下载泵状态机**：`sub_5760B0` 的推进条件——何时请求下一个文件、何时置完成标志、
   失败是否重试；`download_list.csv` 如何被解析成那个 `std::map`（键是 ID 还是名字？顺序如何确定）。
3. **`0x5290` 线格式逐字段**：`u32 result | str filepath | u32 hashval | u32 src_bytes | u16 compress |
   u32 bin_len | bin`；`result<0` 静默忽略、`compress=1` 解压路径（`sub_CCB673/sub_C86010`）、
   `hashval` 是否校验（据说**不校验**——请确认）。
4. **脚本 VM**：`sub_576160` 的映射表实体（脚本名→处理器 ID 0~79）完整导出；
   `sub_BBBD70`→`sub_AEDCF0` 的执行路径；查不到脚本名 ⇒ 静默返回的代码位置。
5. **76 张表对照**：把"请求顺序 + 处理器 ID + 文件名"整理成完整表（交叉 `topics/13`、`topics/16`）。
6. **CSV 方言**：确认 `sub_BBBB70` 解析器的注释/表头/尾逗号/越界列规则（与 `formats\README.md` §四 对照）。

## 4. 产出要求

- 写 `nodes/06-大厅认证与数据表下载.md`。核心交付：
  - 下载泵的**状态机图**（含每个状态的进入/退出条件）；
  - 76 表的**完整对照表**（顺序/处理器ID/文件名/已解格式与否）。
- `0x5290` 格式与 CSV 方言核对结果更新到 `formats\README.md`。
- 结论追加到 `topics\13-登录期数据表下载机制.md`（追加，不覆盖）。

## 5. 完成判据

- 能解释"为什么空内容必卡"`（`sub_BBBCD0(size==0)`）；
- 能解释"为什么客户端每次登录都重下 76 表"（泵的完成标志不持久化）；
- 76 表对照表完整、可核对。

## 6. 注意

- 这是**已有较多结论**的节点（`topics/13` 很完整），任务是**复核 + 补全**，重点补"泵状态机"与"映射表导出"。
- 若发现 `topics/13` 与静态实证冲突，**记录差异**，不要直接改 topics/13 的既有结论（可追加更正小节）。
