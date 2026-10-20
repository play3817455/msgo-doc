# node-02 · N2 平台认证 authsv（HTTP 链）

> 执行前先读 `common.md` 与 `progress.json`。产出：`nodes/02-平台认证authsv.md`

## 1. 目标

把"登录时拉取认证服务器列表"的 **HTTP 链**完整静态讲清楚：URL 组装 → 请求 → 响应分发 → CSV 解析 →
服务器条目入库 → UI 呈现；以及失败重试与"默认地址池回落"。

## 2. 入口线索（已在知识库中确认）

| 地址 | 身份 |
|---|---|
| `0xBB1AF0` / `0xEEEF64` | `HttpMgrEx` ctor / vtable |
| `dword_120A974` / `sub_BAF820` | HttpMgrEx 单例 / getter |
| `0xBB22E0` | 请求入口（vtable+12） |
| `sub_747E10` | URL 组装（`off_DD1818/78/E8` + 时间戳） |
| `0xBB5480` | 响应分发（失败 → `throw 1` @`0xBB575A`，ThrowInfo `0xFFB8C0`） |
| `sub_AFD080` → `sub_7472E0` → `sub_746DC0` | case15（authsv）处理 |
| `sub_BBBB70` / `sub_746710` | CSV 解析 / 逐行回调（加服务器） |

## 3. 研究清单

1. **单例与生命周期**：`sub_BAF820` 获取链、HttpMgrEx 构造时机、线程模型（是否独立线程/每帧轮询）。
2. **URL 组装**：`sub_747E10` 里三个偏移表分别是什么 URL（authsv / config.txt / ClientCheck？），
   时间戳参数的作用（防缓存？）。
3. **请求与重试**：重试 ×4-6 的计数与退出条件；超时设置；`Status != 200` 的判定与 `throw 1` 后行为。
4. **响应 case 分发**：`0xBB5480` 的 switch 各 case 对应的 URL（authsv / remote/config.txt /
   ClientCheck/config.xml / wmode|fmode|dmode.txt）；本次聚焦 authsv（case15）与默认回落。
5. **CSV 解析**：`sub_BBBB70` 的分隔符/注释/# 行规则；`sub_746710` 逐行构造的**服务器条目内存结构**
   （组ID/组名/IP/端口/图标ID 各字段偏移与类型）。
6. **默认地址池回落**：什么时候读归档内置 CSV（`settings_0000.dat` 内的 authsv*.csv）？
   与 HTTP 成功/失败的先后关系（这解释"散装 CSV 无效、必须改归档"）。
7. **UI 呈现**：条目如何填充到登录/服务器选择界面的列表控件。

## 4. 产出要求

- 写 `nodes/02-平台认证authsv.md`；画"URL → case → 条目结构"的完整链。
- 服务器条目结构的字段表追加到 `formats\README.md` §一（本地文件）或新增 §（HTTP 资源）。
- 可信结论追加到 `topics\08-协议报文总表-已验证.md`（或 `topics\00` 阶段 3）。

## 5. 完成判据

- 能说明：客户端**先**试 HTTP、**失败后**回落归档内置池的确切代码路径；
- 服务器条目的内存结构逐字段明确；
- 能解释私服方案里"必须等长改写归档内 CSV"的原因（与回落机制对应）。

## 6. 注意

- 本节点只做静态分析；不需要真连 9you（域名已停服）。
- `研究知识库.md` §11.3 有实测 IP 清单，可用来**交叉验证**解析出的字段含义（不要当结论直接抄）。
