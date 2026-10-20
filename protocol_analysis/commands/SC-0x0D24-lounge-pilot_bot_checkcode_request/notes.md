# 未决问题 —— SC-0x0D24-lounge-pilot_bot_checkcode_request

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `vt[0xF0]` 的业务定名 | 未知（槽号 `0xF0` 已确证；本批内未出现同槽） | 未交叉 UI 侧实现 | 2026-09-20 |
| Q2 | `code` 的字符集（数字/字母）与是否固定 12 位 | 未知（线上只保证 NUL 结尾、`L ≤ 12`） | 未找到校验器 | 2026-09-20 |
| Q3 | 与 CS `0x93EE pilot_bot_checkcode_request_r`（容量 `0x12`）的字段对应 | 未知（该条仍 DRAFT） | C→S 侧本轮未分析 | 2026-09-20 |
| Q4 | 与 SC `0xCA2C pilot_bot_checkcode_result` 的时序关系 | 推测为「服务端下发验证码 → 客户端回填（`0x93EE`）→ 结果（`0xCA2C`）」 | 未分析后两条 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 配对请求：`../CS-0x93EE-lounge-pilot_bot_checkcode_request_r/`（`0x93EE`，声明容量 `0x12`）。
- 后续应答：`../SC-0xCA2C-lounge-pilot_bot_checkcode_result/`（`0xCA2C`）。
- 变长串口径例证：本命令是「**容量 == 串槽预算**」的干净样本（`capacity 0xD` == `sub_B02BA0` 的第 3 实参 `0xD` == 缓冲申请量 `0xD`）。
  `sub_B02BA0` 的消费量语义（整函数复核，`0xB02BA0..0xB02BF4`）：`eax = min(maxlen, end-cur)`，在其中找 NUL，
  成功则 `游标 = NUL+1`、`memcpy(dst, cur, 游标-cur)` ⇒ **消费 = 串长 + 1 ≤ maxlen**，且 `maxlen` 是**含 NUL 的最大字节数**。

## 取证来源

- 全部汇编证据取自 IDB `unpacked\GundamOnline_CHINA_v15.exe.i64`，块 `0xB550B7..0xB55234`（批次-4 落盘 `_b4_dump.txt`），无需要走 `unpacked\shell` dump 的情形。
