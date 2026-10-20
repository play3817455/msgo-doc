# 汇编证据 —— SC-0x377D-battle-bullet_supply

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB13F9D`）

```asm
; VA: 0xB13F9D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB13F9D  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— percent_val：偏移 0，长度 2，线类型 u16（补给百分比）
0xB13FD8  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "percent_val=" → 含义锚点：0xB140CE

; 字段 2 —— equip_idx：偏移 2，长度 2，线类型 u16（装备槽序号）
0xB14018  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "equip_idx=" → 含义锚点：0xB140F4

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB1404F
0xB1404F  push    <模块/错误码>
0xB1404F  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB14156
0xB14156  mov     edx, [obj]
;       mov     edx, [edx+0x278h]
;       call    edx          ; vt[0x278]（2 实参）
```
