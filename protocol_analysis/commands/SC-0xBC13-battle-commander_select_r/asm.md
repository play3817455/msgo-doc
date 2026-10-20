# 汇编证据 —— SC-0xBC13-battle-commander_select_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B2A45E`）

```asm
; VA: B2A45E（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x4
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb2a488|0xb2a497
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2A4C3
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0xD4）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2A59A —— `vt[0x294]`（1 实参）
```
