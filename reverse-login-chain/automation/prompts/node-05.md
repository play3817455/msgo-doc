# node-05 · N5 世界选择 → 大厅跳转（30000 → 30001）

> 执行前先读 `common.md` 与 `progress.json`。产出：`nodes/05-世界选择到大厅跳转.md`

## 1. 目标

把"选世界成功之后，客户端如何断开 30000、创建登录大厅步骤、主动连 30001"这段**连接切换逻辑**
静态讲清楚，包括 OTP 的来源与用途。

## 2. 入口线索（已在知识库中确认）

| 地址 | 身份 |
|---|---|
| `sub_A88920` | 登录 FSM（state 18 等待选择 → 19 → **20**） |
| `sub_43E660` | "开始登录大厅"：`sub_43A350(4,1.0)` 切主状态 + `new CGameStateStepUpdateLoginLounge(host=app+1168, otp=app+1297, port=app+1340)` + `sub_43E130` 激活 |
| `sub_42D3D0` | `CGameStateStepUpdateLoginLounge` ctor（vtable `0xD67B54`） |
| `sub_43BAC0` | 该状态机 tick（槽 2）：case0=connect(host,port)、case1=`sub_AF6FB0()`、case2=OTP 校验 `sub_BAAF60` |
| `sub_AF73E0` | 连大厅包装（2 个调用者：`sub_43ADD0` case4 / `sub_43BAC0` case0） |
| `sub_43ADD0` | 旧状态机（`app+1348` 注册，**从未被触发** ✗） |

## 3. 研究清单

1. **触发时机**：state 18 的三个条件（窗口结果==1 && `sub_74AAA0` && `sub_42D360()`）各自含义；
   `sub_42D360` 发 0x3B8F 防沉迷查询的作用与"卡在 18"的历史成因。
2. **host/port/otp 三字段**：`app+1168`/`+1340`/`+1297` 的**写入者**（应回到 N4 的 `sub_439030`）、
   内存里的编码与长度；otp 由服务端下发还是客户端生成。
3. **状态机全量**：`sub_43BAC0` 的 case0..caseN 全部（不只 0/1/2），特别是 case2 OTP 校验 `sub_BAAF60`
   的输入/输出/失败分支。
4. **两条连接的交替**：何时关 30000（`sub_AF6F30`）、何时连 30001；是否存在并存窗口。
5. **`sub_AF73E0` 内部**：它如何调用 N3 的 iSession 建连（与 N3 衔接，指明复用点）。
6. **失败回退**：连 30001 失败/OTP 失败会回到哪个 state。

## 4. 产出要求

- 写 `nodes/05-世界选择到大厅跳转.md`；画一张状态图：`state18 → 19 → 20 → LoginLounge.case0..N`。
- host/port/otp 字段的存储表更新到 `formats\README.md`（或节点文档 §1.3）。
- 地址结论追加到 `topics\10`。

## 5. 完成判据

- 能精确回答"客户端在第几步、由哪个函数、用哪三个字段去连 30001"；
- `sub_43BAC0` 每个 case 都有结论；
- 能说明 OTP 在新私服场景下是否可以直接给空/固定值（给出代码依据）。

## 6. 注意

- ⚠️ `sub_43ADD0` 是**死代码**（从未触发），别把它当主路径。
- 与 N4 的 `sub_439030` 强耦合，若 N4 已完成请直接引用其结论。
