# 汇编证据 —— SC-0x36D9-lounge-msma_missionunit_get_list_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10C` @ `0xB5C780`）

```asm
; VA: 0xB5C780（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5C780  push    0x10C          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— missionunit_count：偏移 0，长度 4，线类型 u32（编队单位数（上限 `0x16`=22，`cmp ebx,16h`@`0xB5C7DC`））
0xB5C7B0  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "missionunit_count=" → 含义锚点：0xB5C8CB

; 字段 2 —— missionunit_set[]：偏移 4，长度 12，线类型 array<missionunit>（编队单位数组（元素线长 12 / 槽步进 `0x0C`=12，`sub_B06060`））
0xB5C80A  call    复合读取器（元素/结构体，见 notes.md）     ; 读 array<missionunit>
; 块内日志格式串 "missionunit_set[]=" → 含义锚点：0xB5C8CB

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5C85F
0xB5C85F  push    <模块/错误码>
0xB5C85F  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5C97D
0xB5C97D  mov     edx, [obj]
;       mov     edx, [edx+0x31Ch]
;       call    edx          ; vt[0x31C]（2 实参）
```
