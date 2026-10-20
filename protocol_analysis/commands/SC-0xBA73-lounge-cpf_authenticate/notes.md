# 未决问题 / 记录 —— SC-0xBA73-lounge-cpf_authenticate

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 与已 DONE 的 `SC-0xBA73-battle-cpf_authenticate` **同 opcode、同结构**（容量 `0x84`、2 字段、`data[128]`），互为协议类对照。
- 打印段用 `sub_ADCBF0` 逐字节十六进制输出；块内日志串 `recv_cpf_authenticate(` / ` (id:` / `data={` / `,` / `}`。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
