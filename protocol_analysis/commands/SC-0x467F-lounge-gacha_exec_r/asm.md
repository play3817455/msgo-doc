# 汇编证据 —— SC-0x467F-lounge-gacha_exec_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x115` @ `0xB5E1B1`）

```asm
; VA: 0xB5E1B1（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5E1B1  push    0x115          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5E1EF  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5E392

; 字段 2 —— gacha_id：偏移 4，长度 4，线类型 u32（扭蛋 ID）
0xB5E22F  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "gacha_id=" → 含义锚点：0xB5E3BC

; 字段 3 —— prize_count：偏移 8，长度 4，线类型 u32（奖品条数（上限 `0x0B`=11，`cmp ebx,0Bh`@`0xB5E271`））
0xB5E245  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "prize_count=" → 含义锚点：0xB5E3D7

; 字段 4 —— prize[]：偏移 12，长度 21，线类型 array<prize>（奖品数组（元素线长 21 / 槽步进 `0x18`=24，`sub_B416C0`））
0xB5E29D  call    复合读取器（元素/结构体，见 notes.md）     ; 读 array<prize>
; 块内日志格式串 "prize[]=" → 含义锚点：0xB5E3D7

; 字段 5 —— n_last1B：偏移 276，长度 1，线类型 u8（末位标志字节）
0xB5E2D0  call    sub_B06230     ; 读 u8
; 块内日志格式串 "n_last1B=" → 含义锚点：0xB5E459

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5E31A
0xB5E31A  push    <模块/错误码>
0xB5E31A  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5E4CD
0xB5E4CD  mov     edx, [obj]
;       mov     edx, [edx+0x3E0h]
;       call    edx          ; vt[0x3E0]（4 实参）
```
