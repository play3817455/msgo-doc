# 汇编证据 —— SC-0x7BCC-lounge-item_add_dialog_show

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `B68CB9`）

```asm
; VA: B68CB9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B68CB9  push    0x6          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— item_id：偏移 0，长度 4，线类型 u32（获得道具 ID（日志串 `item_id=`））
B68CF4  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B68DE3 → 含义锚点

; 字段 2 —— stack：偏移 4，长度 2，线类型 u16（堆叠数量（日志串 `stack=`））
B68D34  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B68E09 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B68D44
B68D44  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B41110
```

## E4 去向（用途锚点）

```asm
; VA: B68E5E —— `vt[0x334]`（2 实参）
B68E5E  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x334h]
;       call    <reg>
```
