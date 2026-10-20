# 未决问题 / 记录 —— SC-0xC4CB-lounge-clan_rokaku_ms_deck_set_r

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `uniq_msid` u64：读原语 `sub_B06200`（游标步进 8）与阵列预留 `sub_B41A10`（8/槽）双证；去向按 cdecl 拆低 32 位在前、高 32 位在后。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
