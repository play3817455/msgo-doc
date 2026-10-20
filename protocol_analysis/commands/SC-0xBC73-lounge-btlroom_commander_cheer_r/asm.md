# 汇编证据 —— SC-0xBC73-lounge-btlroom_commander_cheer_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x19` @ `B76C3B`）

```asm
; VA: B76C3B（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x19
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— cmdr_name：偏移 0，长度 L+1，线类型 bytes(≤24)（指挥官名（NUL 结尾 日志串 `cmdr_name="`））
;   0xb76c66
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B76C92
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x98）报错
```

## E4 去向（用途锚点）

```asm
; VA: B76D75 —— `vt[0x1C0]`（1 实参）
```
