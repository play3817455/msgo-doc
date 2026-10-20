# 分析笔记 —— CS-0x6FA1-battle-combat_operation_container_collect

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x6; call <reg>`（容量 `push` @ `0xb3f046`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2(opcode) + 4 = 6 == 容量 0x6 = 6`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x02D8-battle-combat_operation_container_collect_r` 构成请求/应答对。

## 未决 / 存疑

- `destination` 具体三类业务名及与物资资源池的映射未解。

## 2026-10-10 结论补证与修正

- IDA `sub_68D580` 是客户端附近对象筛选/交互路径；依内部类别 6、标志类别 8、类别 11 的三个分支，在距离条件满足时分别令 `v11=0/1/2`，再调用 `sub_B01760(v11)`。
- `sub_B01760` 唯一参数原样传给 `sub_B3F000`，后者原样写入 `0x6FA1.destination`。因此 `destination` 在线字段名仍保留，但实际调用值是 0/1/2 的交互类别，不是箱体实体 ID。哪个数值对应哪种物资、交互后资源增加多少，仍未知。
- 类别 11 分支的筛选字段已闭合：`sub_68D580` 命中类别 11 后调用 `sub_474BC0`；该函数从对象 `+0xD8` 取参数记录，再读记录 `+0x78` 并与 11 比较。`CHARA_PARAM` reader `sub_582390` 将 CSV7 `combat_role` 写入该记录偏移 +120；枚举转换器 `sub_5804F0` 将 `EX_TENDER` 映射为 11。因此 `destination=2` 来自满足其余资格/距离条件且 `combat_role=EX_TENDER` 的对象分支。此结论识别的是客户端筛选对象类别，不证明服务端资源奖励或所有补给舰都会触发。
- 服务端处理器只回 `0x02D8 result=0`，目前没有对象库存/玩家资源账；不能把成功回包解释为已实现物资系统。
- 旧结论「按作战目标记、具体语义未知」被本次调用链推翻；新结论如上。响应侧 `ent_id` 在业务处理函数 `vt[0x2F4]` 中的用途及 `result` 枚举仍待追。

## 2026-10-11 类别 11 对象类型来源补证

先前“6/8/11 与 `CHARA_PARAM.combat_role` 只数值对齐、尚未证明读取该字段”的记录已被正确 v15 指令数据流更新：类别 11 分支明确调用 `sub_474BC0`，该谓词读取与 `CHARA_PARAM` reader 写入偏移相同的 +120 字段，并比较枚举值 11；枚举表将 11 命名为 `EX_TENDER`。所以可确认 `destination=2` 是该分支发出的类别值，分支对象的 `combat_role` 为 `EX_TENDER`。类别 0/1 的分支来源仍未闭合；`EX_STRONGHOLD=6`、`EX_DEPLOY_ARMS=8` 目前只是数值巧合，不能据此命名。

证据：`serverv/tmp/r001-render-outer-gates-code-20261007.json` 的 `sub_474BC0 @ 0x474BC0` 指令；`db_design/schema/cfg/tables/CHARA_PARAM.json` 的 CSV7 reader/enum；`sub_68D580` 三分支调用记录。当前会话未调用 IDA MCP，此处复核的是此前由正确 v15 `ida-pro-mcp` 导出的指令记录。响应 `0x02D8` 的实际结算含义与服务端战术条账仍未闭合。

### 服务端个人回收记录的待接点

解包 `medal.csv` 有累计 `CONTAINER` 货柜回收章，服务端 `game.precord.container_cnt` 对应此类个人计数，但当前 battle settlement 只累计击杀/死亡。`0x6FA1` 上行没有货柜实体 ID，暂不能作为成功回收计数；需先闭合成功事件和重复请求去重规则。教程所述“部分机体不能搬运”也尚无 `CHARA_PARAM` 明确资格列；`deployable_type=CARRY` 是另一枚举域，不能用作该能力标志。详见 `serverv/docs/R001-地图玩法对象链.md` 新增段。
