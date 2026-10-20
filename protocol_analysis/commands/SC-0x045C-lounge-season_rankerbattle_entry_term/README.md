# SC-0x045C-season_rankerbattle_entry_term

> 状态：`DONE`（2026-09-20，批次-2）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x045C` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `season_rankerbattle_entry_term` |
| 名字符串 | `)->_proto_lounge_client::recv_season_rankerbattle_entry_term( ` @ `0xEEA050`，引用点 `0xB5304C` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB52FA3` .. `0xB53112`（块首 `0xB52FA3 call sub_B41120`，错误码 `0x256`） |
| 关联命令 | 同族（非配对请求）：`../SC-0xD286-lounge-season_rankerbattle_entry_info/`、`../SC-0x63D3-lounge-season_rankerbattle_config_update/`、`../SC-0xD18B-lounge-season_rankerbattle_state_update/`；同族发送侧 `../CS-0x511B-lounge-season_rankerbattle_team_info_get/` |

## 2. 结论摘要

- **报文体总长：定长 `4` 字节**（单个 u32）。
- 负载 = 1 个 u32（`term_sec`）。
- 长度校验：`0xB5301F mov ebx,[esp+2C5Ch+var_2C44]`（读完后的游标）、`0xB5301F cmp ebx,[esp+2C5Ch+var_2C40]`（vs 报文末尾）、`0xB53023 jnz`（不等 ⇒ `push 256h` 报错）⇒ **整包精确消费完**。
- 声明容量 `push 4`（`0xB52FB8`）= 4，**与线长相等**（单一定长字段，容量 == 负载，符合 `_meta/环境与工具约定.md` §7.5）。
- 是否分帧：否。
- 关键结论：该命令只把「赛季排位战参战期限」一个 u32 交给 `vt[0x5A4]`（`0xB530F6`）；除该值与一条 trace 日志外无其它副作用。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x045C` | `0xB5304C`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `term_sec` | 参战期限（秒） | 交 `vt[0x5A4]`（`0xB530ED` 取虚表项、`0xB530F6` 调用，实参即本值）；日志 `term_sec=`（`0xB5309D`） | `?`（绝对时刻 vs 剩余秒数未定，见 `notes.md` Q1） | `0xB52FF3`（`sub_B02DD0`）；`0xB02DE9 add [eax],4`；日志 `0xB5309D` | 类型确证 / 语义待定 |
| — | 4 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB5301F`（`cmp`）、`0xB53023`（`jnz` 错误） | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEEA050` 的引用点 `0xB5304C` 落在 `sub_B51930` 的 case 块 `0xB52FA3..0xB53112` 内。
2. 块首 `0xB52FA3 call sub_B41120`（lounge case 收尾/开关）与全部错误路径（`0xB5300D`、`0xB53023`）一致使用错误码 `0x256`。
3. 读取路径：`0xB52FD5 lea ecx,&var_2C48` → `0xB52FE4 call sub_B41470`（解码缓冲预留 4B，**非字段**）→ `0xB52FF3 call sub_B02DD0`（唯一字段）。

### 4.2 长度闭合
- 唯一字段为 u32：读取器 `sub_B02DD0` 自身带「剩余 ≥ 4」边界检查（`0xB02DD6 lea edx,[ecx+4]`），成功分支 `0xB02DE9 add dword ptr [eax],4` ⇒ 游标 +4。
- 4（字段）== 4（声明容量）== 校验点游标增量 ⇒ 闭合 ✓。

### 4.3 存疑点
见 `notes.md`（`term_sec` 语义、`vt[0x5A4]` 实现去向）。

## 5. 质量门自检

- [x] G1 字段表总长（4）与 `0xB53023` 处「游标 == 末尾」校验一致（容量 4 == 负载 4）。
- [x] G2 线类型指回汇编 VA（u32：`0xB52FF3` 读 + `0xB02DE9` 游标 +4）；未使用伪代码类型。
- [x] G3 字段含义取自块内日志串 `term_sec=`（`0xB5309D`），用途追到 `vt[0x5A4]`（`0xB530F6`）。
- [x] G4 不确定项（枚举/语义）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 本命令无同名配对请求（已链接同族命令）。
