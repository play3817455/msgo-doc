# 未决问题 / 记录 —— SC-0xB43F-lounge-party_recruit_list_get_r

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `recruits` 元素读取器 `sub_B45400` 内含 `cmp eax,3Dh`(61) 的定长循环 ⇒ 线长 80（整函数展开）；`leaders` 元素读取器 `sub_B454D0` 含 `cmp eax,19h`(25) 循环 + 内嵌 `sub_B068B0`(18) ⇒ 线长 52。
- 两元素内部成员名可用打印器 `sub_B4D840`(recruits)、`sub_B4D9D0`(leaders) 后续拆分（本批未逐一命名）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
