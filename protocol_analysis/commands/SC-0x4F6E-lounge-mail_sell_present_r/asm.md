# 汇编证据 —— SC-0x4F6E-lounge-mail_sell_present_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `0xB5FD17`）

```asm
; VA: 0xB5FD17（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5FD17  push    0xC          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5FD52  call    sub_B02DD0     ; u32
; 块内日志格式串 "result=" → 含义锚点：0xB5FE5B

; 字段 2 —— mailid：偏移 4，长度 8，线类型 u64（邮件 ID（u64））
0xB5FD92  call    sub_B06200     ; u64
; 块内日志格式串 "mailid=" → 含义锚点：0xB5FE80

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5FDBE
0xB5FDBE  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB5FDBE  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5FEE4
0xB5FEE4  mov     <reg>, [obj]; mov <reg>, [<reg>+0x39Ch]
;       call    <reg>          ; vt[0x39C]（3 实参）
```
