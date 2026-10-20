# 分析笔记 —— CS-0x5C82-auth-authenticate_you9otp_input_r

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x26; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 17 + 9 = 32 ≤ 容量 0x26=38（富余 6）`

## 与其他命令的关联

- 与 S→C `SC-0x60E0-auth-authenticate_you9otp_input` 构成请求/应答对。

## 未决 / 存疑

- 日志名序（`otp_type=`→`otp_matrix_code=`→`input_otp=`）与线序一致。
- ★ 串槽预算书写形态：第一个为 `push 11h`（带 `h` 后缀），第二个为 `push 9`（**十进制无后缀**）⇒ 立即数解析须同时接受两种写法（承批次-17 第 ⑤ 坑）。
- 与 S→C `SC-0x60E0-auth-authenticate_you9otp_input` 构成请求/应答对。

## 服务端实现（2026-09-30，§㊼ auth OTP 收尾）

- 实现：`serverv/internal/agent/otp.go` 的 `onAuthenticateYou9otpInputR`；注册点
  `registerOTPHandlers`（← `internal/agent/server.go` 的 `registerHandlers`）。
- 落点（裁决 `no_challenge`）：**只解码 + 留证**，**零回包、不落库**。本条是**出题
  `SC-0x60E0`（`otp_type` + 矩阵码）的回话**：客户端把出题那两格**原样回显**、外加用户
  输入（`sub_7497D0` 回调里 `sub_AFE630(otp_type, matrix, input)`）⇒ 题是服务端出的，
  而本服**不出题**（无 OTP 密钥库 / 无矩阵生成器）⇒ 无从判分 ⇒ 沿用 §㊹ 反外挂回话族口径。
- 为什么零回包：协议里**没有 OTP 结果回执**，且客户端发完就拆对话框、**不等回包**
  （`sub_7497D0` 末尾直接释放对话框对象）。
- 凭据纪律：`input_otp` 是**凭据** ⇒ 日志**只记长度、不记内容**；`otp_matrix_code` 也
  只记长度（它是服务端自己下过的题、被回显上来）。`otp_type` 是小枚举照记、**不翻译**。
- 验收测试：`TestRegisterOTPHandlersRegistered`、`TestOTPHandlersSendNothing`、
  `TestOTPHandlersTolerateBadBody`、`TestYou9otpInputLineShape`（变长往返 + 槽预算
  矩阵 16/17、输入 8/9）—— 全部拿 `&Server{}`（`store == nil`）跑。
- 配对命令：出题 `SC-0x60E0-auth-authenticate_you9otp_input`（本服**故意不发**）。
- 留账（补它需要什么证据）：① OTP 密钥/口令来源（本服没有）；② `otp_type` 的**取值表**
  （客户端只看到 `==99` 走 BNPO 分支、其余走 you9 分支，`sub_7497D0`）；③ 原服在哪个
  认证分支下发 `SC-0x60E0`。见 docs/01 ㊼③。
