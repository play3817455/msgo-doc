# 汇编证据 —— SC-0x5290-lounge-datafile_download_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8000112` @ `0xB605DD`）

```asm
; VA: 0xB605DD（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB605DD  push    0x8000112          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB6061B  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB607FD

; 字段 2 —— filepath：偏移 4，长度 256，线类型 str（文件路径（槽位预算 `0x100`=256，`push 100h`@`0xB60646`））
0xB6065E  call    sub_B02BA0     ; str
; 块内日志格式串 "filepath=" → 含义锚点：0xB6082A

; 字段 3 —— hashval：偏移 260，长度 4，线类型 u32（哈希值）
0xB6069B  call    sub_B02DD0     ; u32
; 块内日志格式串 "hashval=" → 含义锚点：0xB6085F

; 字段 4 —— src_bytes：偏移 264，长度 4，线类型 u32（源字节数）
0xB606BF  call    sub_B02DD0     ; u32
; 块内日志格式串 "src_bytes=" → 含义锚点：0xB60889

; 字段 5 —— compress：偏移 268，长度 2，线类型 u16（压缩标志）
0xB606E3  call    sub_B02DF0     ; u16
; 块内日志格式串 "compress=" → 含义锚点：0xB608B4

; 字段 6 —— bin_count：偏移 270，长度 4，线类型 u32（二进制块长度（上限 `0x8000000`，`cmp ebx,8000000h`@`0xB60711`））
0xB606FD  call    sub_B02DD0     ; u32
; 块内日志格式串 "bin_count=" → 含义锚点：0xB608CF

; 字段 7 —— bin[]：偏移 274，长度 4+4N，线类型 array<u8>（二进制块（元素 1B / 槽步进 1B，预留 `sub_B05EA0`；无终止符，长度由 `bin_count` 给出））
0xB60727  call    复合读取器（元素/结构体，见 notes.md）     ; array<u8>
; 块内日志格式串 "bin[]=" → 含义锚点：0xB608CF

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB60764
0xB60764  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB60764  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB609A5
0xB609A5  mov     <reg>, [obj]; mov <reg>, [<reg>+0x78h]
;       call    <reg>          ; vt[0x78]（7 实参）
```
