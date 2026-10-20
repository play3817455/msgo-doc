# 未决问题 / 记录 —— SC-0xB463-battle-msma_AI_install

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 后续复核已在 `db_design/schema/composites/AI.json` 拆出 `AI` 结构体成员；其中包含初始出现坐标/朝向 (`pop_init_x/y/z/dir`)，射击和移动目标、行为状态及编组字段。旧的“成员未逐一命名”记录只代表本批最初的协议文档状态，现已过时。
- 尚未闭合的是业务语义：`AI_ent_id` 对应实体的注册/创建先后关系、客户端收包时缺少该实体的处理、`param_id` 模板来源，以及坐标单位/符号编码。不能用成员名直接推断完整 NPC 生成流程。
- 2026-10-11 用正确 v15 `ida-pro-mcp` 13338 继续追 `B296D1` 的 `vt+0x240`：两张引用 `sub_B0CC20` 的表分别是 `D91CE0` 和 `EED800`。`D91CE0+0x240` 为 `nullsub_28`；`EED800+0x240` 为 `BAA4A0→AFC4C0→62EC10`，后者仅比较一个32位 ID，ID=0 时打开 `IF::CCommanderSelectWindow`，并不读取 AI 参数结构。调用点对 `AI_ent_id:u16` 用 `movzx`，因此 `0xA8E2` 不会匹配 `62EC10` 的有符号常量 `-22302`；之前如将该常量直接解释成可达的 16 位 sentinel，应以此更正。
- 因而两张已找到的回调表都没有证明将 `AI` payload 用于世界实体创建/AI安装；仍未证明运行时 receiver 选择、ID=0 回调的战场上下文、以及表外其他消费路径。`README.md` 原“2 实参”仅描述 parser 的调用点形态，不代表该虚函数覆盖读取了两个参数。
- 兄弟命令：`0xB604`（`msma_AI_resume`）、`0x1165`（`msma_AI_uninstall`）仅携带 `AI_ent_id`（2B），本命令携带完整 AI 参数（168B）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
