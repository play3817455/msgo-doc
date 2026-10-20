# 未决问题 / 记录 —— SC-0xD5E6-lounge-result_info

- 本批（批次-14）定稿：★**容量反推一击命中**——`0xD518` 逐项等于 20 个字段的 claim 之和，据此唯一确定 5 个计数上限（104 / 104 / 8 / 38108 / 5）与全部结构体 claim。
- ★**定长数组（无线上 count）**：`examination_list` 固定 5 元（`sub_B418C0` 一次推进 `0x28`=40 = 5×8，循环上界字面量 5 @`B7DD9E`）；`pointdmg.gaugedmg` 固定 3 元（`sub_B45760` 内 `cmp …,3`）。
- ★**「槽步进 ≠ 元素线长」**：`score_ranking`/`favms_add` 元素线长 61/66，槽步进 72（`sub_B413C0`）；`result_wave` 20/28（`sub_B41710`）。
- 结构体 claim ≠ 线长：`progress` 64/46、`result` 600/555、`totalresult_wave` 20/19、`dcpoint` 68/41、`pointdmg` 24/12、`adop_get` 16/13。
- **未定案项**：① `result`（`sub_B44B70` 555B 结构）内部成员未逐一命名（打印器 `sub_B4C650` 体积 >3000B，本批未展开）；② `dcpoint` 的 41B 内部线序未逐一拆分（打印器打印 7 组名，与 5 次读取未一一对位）；③ `adop_get.adop_set` 的 `u16` 循环上界（读取器内 `cmp …,4`）与打印器成员数未交叉验证。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
