# 汇编证据 —— SC-0x315C-battle-roomlobby_xwar_commander_lot_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x7` @ `0xB13795`）

```asm
; VA: 0xB13795（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB13795  push    0x7          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB137D0  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB138DA

; 字段 2 —— is_lot：偏移 4，长度 1，线类型 u8（是否抽选）
0xB1380D  call    sub_B06230     ; 读 u8
; 块内日志格式串 "is_lot=" → 含义锚点：0xB13902

; 字段 3 —— lot_count：偏移 5，长度 2，线类型 u16（抽选数量）
0xB13831  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "lot_count=" → 含义锚点：0xB1392A

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB13862
0xB13862  push    <模块/错误码>
0xB13862  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB13993
0xB13993  mov     edx, [obj]
;       mov     edx, [edx+0x98h]
;       call    edx          ; vt[0x98]（3 实参）
```
