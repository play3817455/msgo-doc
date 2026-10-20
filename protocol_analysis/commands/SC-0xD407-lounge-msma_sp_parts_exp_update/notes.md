# 未决问题 / 记录 —— SC-0xD407-lounge-msma_sp_parts_exp_update

- 本批（批次-14）定稿：按 SOP §5 复核，类型全部由汇编判定。
- 预留原语：`sub_B41A10`（u64 单槽 claim 8）、`sub_B41470`（u32 单槽 claim 4），两者仅推游标、不是字段。
- `uniqid_ms`（u64）去向按 cdecl 拆「低 32 位在前、高 32 位在后」两个实参（同上批口径）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
