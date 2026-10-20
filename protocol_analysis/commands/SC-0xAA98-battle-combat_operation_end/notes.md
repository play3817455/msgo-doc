# 未决问题 / 记录 —— SC-0xAA98-battle-combat_operation_end

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 顶层 1 字节字段 `is_completed` 依据派发侧 `movzx eax, byte ptr [eax]`@`B2777B` 判为 `u8`（SOP §6 / 批次-5 口径）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。


2026-10-11正确v15消费校正：EED7AC+2F0→BAA790→AFC820→639A90。在STGARMS1/type25完成且app模式bit2清的分支，第三字段经639B27..32交664510，66453B加载完整实参后66454B查4B59B0实体表，取actor名字格式化str_table 60,180,2（战略兵器启动 %s）。因此旧“毫秒”含义在此分支错误；保留原字段名和u32线型，其他支援回调用途待核。证据serverv/docs/data/ida-v15-strategic-operation-end-20261011.json。
