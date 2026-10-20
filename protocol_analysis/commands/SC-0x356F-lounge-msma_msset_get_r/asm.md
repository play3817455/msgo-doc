# 汇编证据 —— SC-0x356F-lounge-msma_msset_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x784` @ `0xB5BAFB`）

```asm
; VA: 0xB5BAFB（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5BAFB  push    0x784          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ms_set_count：偏移 0，长度 4，线类型 u32（机体套装数（上限 `0x14`=20，`cmp ebx,14h`@`0xB5BB57`））
0xB5BB2B  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "ms_set_count=" → 含义锚点：0xB5BC4B

; 字段 2 —— ms_set[]：偏移 4，长度 95，线类型 array<ms_set>（套装数组（元素线长 95 / 槽步进 `0x60`=96，`sub_B415A0`））
0xB5BB8A  call    复合读取器（元素/结构体，见 notes.md）     ; 读 array<ms_set>
; 块内日志格式串 "ms_set[]=" → 含义锚点：0xB5BC4B

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5BBDF
0xB5BBDF  push    <模块/错误码>
0xB5BBDF  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5BCFD
0xB5BCFD  mov     edx, [obj]
;       mov     edx, [edx+0x2FCh]
;       call    edx          ; vt[0x2FC]（2 实参）
```
