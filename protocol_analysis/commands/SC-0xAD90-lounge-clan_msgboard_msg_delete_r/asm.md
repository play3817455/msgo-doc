# 汇编证据 —— SC-0xAD90-lounge-clan_msgboard_msg_delete_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `B72123`）

```asm
; VA: B72123（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x5
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B72161
; 字段 2 —— clan_kind：偏移 4，长度 1，线类型 u8（公会类别（日志串 `clan_kind=`；顶层 1B 由 `movzx` ⇒ u8））
;   B721A1|B722C1
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B721B1
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1DA）报错
```

## E4 去向（用途锚点）

```asm
; VA: B722D6 —— `vt[0x478]`（2 实参）
```
