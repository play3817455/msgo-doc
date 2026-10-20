# 汇编证据 —— SC-0x8C24-battle-roomlobby_pick_vote_cancel_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B226B9`）

```asm
; VA: B226B9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B226B9  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B226F4  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B22798 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2271D
B2271D  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B227E8 —— `vt[0xBC]`（1 实参）
B227E8  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0xBCh]
;       call    <reg>
```
