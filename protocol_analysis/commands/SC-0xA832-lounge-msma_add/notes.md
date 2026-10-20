# 未决问题 / 记录 —— SC-0xA832-lounge-msma_add

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `ms` 内部成员已逐一拆分：`db_design/schema/composites/ms_lounge.json`（303B，读取器 `sub_B43570`、打印器 `sub_B49DE0`）；三个列表元素的成员见 `unlockw.json`、`equip_set.json`、`adop_get.json`（打印器 `sub_B4A580`/`sub_B4AA30`/`sub_B4AC50`）。
- ⚠ 早期口径「ms 线长 299」作废：`sub_B43570` 整函数展开实算 **303B**（8 处定长循环：61+2+2+1+3+10+3+7×4 段），并与 48A4 的 `sub_B43A80`（401 = 303 + 3×30 + 8）交叉校验一致。
- 本命令为 `msma_add`（服务端新增机体后下发全量机体数据），与本批 `0xB5D6`（抽选）语义不同，勿混。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
