# node-03 · N3 access 握手与会话加密

> 执行前先读 `common.md` 与 `progress.json`。产出：`nodes/03-access握手与会话加密.md`

## 1. 目标

把 30000（以及后续 30001/30002 共用的）连接建立与会话加密层，整理成**离线可复现的静态规格**：
握手时序、密钥块处理、密码算法、帧格式、计数器、报文类型表、状态机。

> 这是全链的公共底座，后面 N4~N9 都依赖它。要求"精确到字节"。

## 2. 入口线索（已在知识库中确认）

| 地址 | 身份 |
|---|---|
| `0xF3EFAC` / `0x00CABD30` | `ivce::iVCE` vtable / ctor |
| `0xF3F06C` / `0x00CAFE90` | `ivce::iSession` vtable / ctor（`+0xA0`=port WORD、`+0xC4`=256B 主机名） |
| `sub_CA9B40` / `sub_CA9BC0` / `sub_CA9C40` / `sub_CA9C80` | 建会话 + 主机名 / UTF-16→ANSI / createSession 封装 |
| `sub_CAD510` | 会话状态机（`this+0x258`，状态 0..13） |
| `sub_CA3030` | 驱动 step#2（`this+640`/`+624`；state3 收 32B ⇒ `sub_CA11D0`；state6 ⇒ `sub_C88510`） |
| `sub_C9E810` | 驱动 step#1（状态 6 ⇒ `sub_C882F0` 加密流=发送） |
| `sub_CA2F20` | `ivce::RSAContext<128>` ctor（e=65537，模数 4 dwords） |
| `sub_C9FA00` / `sub_C9F820` | 客户端 RSA 加密发送 / RSA 解密入口 |
| `sub_CA11D0` | state3 双块处理（`sub_C9F820`×2 → `sub_CB4580`×2） |
| `sub_CB4580` / `sub_CB4970` / `sub_CB4AD0` | Camellia 密钥扩展 / 加密块 / 解密块 |
| `sub_C84B60` | 游戏层消息分发器（type 0~4） |
| `sub_CAD400` / `sub_CAD240` / `sub_CB7950` | 分发循环 / 置 state11 / close |

## 3. 研究清单

1. **连接建立**：从 `sub_AF73E0`（连大厅包装）到 `iSession` 建连的完整调用路径；
   `iSession` 的 `+0xA0`(port) / `+0xC4`(host 256B) 由谁写入。
2. **状态机逐状态**：`sub_CAD510` 的 0..13 每个状态的进入条件、动作、下一状态；
   `sub_CA3030` 的 state 3/4/5/6 分支（尤其 state3 vs state4 的判定依据 `[this+0x9C]`）。
3. **密钥交换**：客户端 16B 首包的**确切含义**（模数 n_C？小端？）与构造点；
   服务器 32B 的消费点（`sub_CA11D0` 读两块）；**block1 做 RSA、block2 原样**在代码里的体现。
4. **密码算法**：确认 `sub_CB4580/4970/4AD0` = Camellia-128（S 盒表地址 `0xF3F330/0xF3F730/0xF3FB30/0xF3FF30`，
   常量 `0xF40330/0xF40340`），并记录子密钥布局。
5. **帧与计数器**：`sub_C882F0`（加密发送流）与 `sub_C88510`（解密流）的头部解析、块计数、
   计数器自增位置（`ctx[0]`）、归零条件（收到 16B 密钥交换）。
6. **报文类型表**：`sub_C84B60` 的 type 0~4 每个分支的**最小长度、长度字段宽度 k、语义**；
   `return -1 → 关闭` 的条件。
7. **与实现的对照**：对照 `server\camellia128.py` 的 `wrap_message` 与 `server\access_sticky.py` 的
   `keyblocks()`，指出任何不一致（这是发现隐藏坑的最佳方式）。

## 4. 产出要求

- 写 `nodes/03-access握手与会话加密.md`，要求：**给一个"服务器实现清单"**（收到什么、回什么、按什么格式）。
- 帧格式/密钥块格式更新到 `formats\README.md` §2.2。
- 与 `topics\08 §D` 有冲突的地方，**逐条列出差异**（不要擅自改 topics/08，先记录）。

## 5. 完成判据

- 一个没读过知识库的人，仅凭本节点文档 + `server\camellia128.py`，能独立写出能通过握手的服务器；
- 状态机 0..13 与 3/4/5/6 **每个状态**都有明确条件与动作；
- `sub_C84B60` 类型表与 `topics\08 §D6` 逐条一致（或列出差异）。

## 6. 注意

- 这一节历史上反复翻车（AES↔Camellia、计数器起点、RSA 与否），**每条都要拿代码证据**，不要复述旧结论。
