# 分析笔记 —— CS-0x44CD-auth-authenticate_bnpotp_input_r

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x206; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 513(串槽) = 515 ≤ 容量 0x206=518（富余 3，上限场景）`

## 与其他命令的关联

- 同一命令与 S→C `SC-0xA103-auth-authenticate_bnpotp_input` 构成请求/应答对（INDEX 反向表）。

## 未决 / 存疑

- 串槽预算 = `push 0x201`(513)，由写线原语前紧邻的 `push IMM` 给出；实际线长 = 串长 + 1。
- 同一命令与 S→C `SC-0xA103-auth-authenticate_bnpotp_input` 构成请求/应答对（INDEX 反向表）。

## 服务端实现（2026-09-30，§㊼ auth OTP 收尾）

- 实现：`serverv/internal/agent/otp.go` 的 `onAuthenticateBnpotpInputR`；注册点
  `registerOTPHandlers`（← `internal/agent/server.go` 的 `registerHandlers`）。
- 落点（裁决 `no_challenge`）：**只解码 + 留证**，**零回包、不落库**。本条是**出题
  `SC-0xA103`（0B 零负载）的回话**（CS 名里的 `_r` = reply；与已知方向的
  `authenticate_you9channeling`／`authenticate_you9channeling_r` 同一套命名约定），
  而本服**不出题**（无 OTP 密钥库 / 无口令生成器）⇒ 手里没有"应该是什么"，无从判分
  ⇒ 沿用 §㊹ 反外挂回话族的口径。
- 为什么零回包：协议里**没有 OTP 结果回执**（SC 段里除 `0xA103`/`0x60E0` 外没有任何
  `*otp*`），且客户端发完就拆对话框、**不等回包**（`sub_7497D0` 末尾直接释放对话框对象）。
- 凭据纪律：`input_otp` 是**凭据** ⇒ 日志**只记长度、不记内容**（`onLoginReq` 连口令都不写）。
- 验收测试：`TestRegisterOTPHandlersRegistered`（注册表）、`TestOTPHandlersSendNothing`
  （好包零帧）、`TestOTPHandlersTolerateBadBody`（脏包不崩）、`TestBnpotpInputLineShape`
  （变长往返 + 槽预算 512/513）—— 全部拿 `&Server{}`（`store == nil`）跑。
- 配对命令：出题 `SC-0xA103-auth-authenticate_bnpotp_input`（本服**故意不发**）。
- 留账（补它需要什么证据）：① OTP 密钥/口令来源（本服没有）；② 原服在哪个认证分支下发
  `SC-0xA103`；③ `input_otp` 的取值语义（本批不落内容）。见 docs/01 ㊼③。
