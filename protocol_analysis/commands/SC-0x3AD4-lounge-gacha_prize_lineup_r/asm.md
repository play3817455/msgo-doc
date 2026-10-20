# 汇编证据 —— SC-0x3AD4-lounge-gacha_prize_lineup_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1C37` @ `0xB5C9CB`）

```asm
; VA: 0xB5C9CB（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5C9CB  push    0x1C37          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5CA09  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5CC27

; 字段 2 —— gacha_id：偏移 4，长度 4，线类型 u32（扭蛋 ID）
0xB5CA49  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "gacha_id=" → 含义锚点：0xB5CC51

; 字段 3 —— prize_count：偏移 8，长度 4，线类型 u32（奖品条数（上限 `0x12C`=300，`cmp ebx,12Ch`@`0xB5CA8B`））
0xB5CA5F  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "prize_count=" → 含义锚点：0xB5CC6C

; 字段 4 —— prize[]：偏移 12，长度 21，线类型 array<prize>（奖品数组（元素线长 21 / 槽步进 `0x18`=24，`sub_B416C0`））
0xB5CABA  call    复合读取器（元素/结构体，见 notes.md）     ; 读 array<prize>
; 块内日志格式串 "prize[]=" → 含义锚点：0xB5CC6C

; 字段 5 —— act_date：偏移 7212，长度 4，线类型 u32（活动日期）
0xB5CAED  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "act_date=" → 含义锚点：0xB5CCF3

; 字段 6 —— act_num：偏移 7216，长度 2，线类型 u16（活动编号）
0xB5CB15  call    sub_B02DF0     ; 读 u16
; 块内日志格式串 "act_num=" → 含义锚点：0xB5CD1E

; 字段 7 —— bEnableDiscount：偏移 7218，长度 1，线类型 u8（是否启用折扣）
0xB5CB3D  call    sub_B06230     ; 读 u8
; 块内日志格式串 "bEnableDiscount=" → 含义锚点：0xB5CD46

; 字段 8 —— servicePoint：偏移 7219，长度 4，线类型 u32（服务点数）
0xB5CB65  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "servicePoint=" → 含义锚点：0xB5CD6D

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5CBAF
0xB5CBAF  push    <模块/错误码>
0xB5CBAF  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5CDF5
0xB5CDF5  mov     edx, [obj]
;       mov     edx, [edx+0x3DCh]
;       call    edx          ; vt[0x3DC]（8 实参）
```
