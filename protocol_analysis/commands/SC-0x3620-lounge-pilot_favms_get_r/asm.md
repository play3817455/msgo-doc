# 汇编证据 —— SC-0x3620-lounge-pilot_favms_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xCA90` @ `0xB5C43F`）

```asm
; VA: 0xB5C43F（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5C43F  push    0xCA90          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5C47D  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5C610

; 字段 2 —— pilot_id：偏移 4，长度 4，线类型 u32（飞行员 ID）
0xB5C4BA  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "pilot_id=" → 含义锚点：0xB5C63A

; 字段 3 —— world_id：偏移 8，长度 4，线类型 u32（世界 ID）
0xB5C4DE  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "world_id=" → 含义锚点：0xB5C664

; 字段 4 —— favms_count：偏移 12，长度 4，线类型 u32（收藏机体数（上限 `0x2D0`=720，`cmp ebx,2D0h`@`0xB5C51D`））
0xB5C4F4  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "favms_count=" → 含义锚点：0xB5C67F

; 字段 5 —— favms_arr[]：偏移 16，长度 66，线类型 array<favms>（收藏机体数组（元素线长 66 / 槽步进 `0x48`=72，`sub_B413C0`））
0xB5C54C  call    复合读取器（元素/结构体，见 notes.md）     ; 读 array<favms>
; 块内日志格式串 "favms_arr[]=" → 含义锚点：0xB5C67F

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5C598
0xB5C598  push    <模块/错误码>
0xB5C598  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5C748
0xB5C748  mov     edx, [obj]
;       mov     edx, [edx+0x158h]
;       call    edx          ; vt[0x158]（5 实参）
```
