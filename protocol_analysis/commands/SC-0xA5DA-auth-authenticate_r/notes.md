# 未决问题 / 记录 —— SC-0xA5DA-auth-authenticate_r

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- auth 协议类的闭合点不在块尾收尾函数之前，而在「读取后的成功分支」上（本命令 = `B04A65`）。
- 与 `SC-0xA5DA-battle-authenticate_r` / `SC-0xA5DA-lounge-authenticate_r` 同 opcode、同协议族语义。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
