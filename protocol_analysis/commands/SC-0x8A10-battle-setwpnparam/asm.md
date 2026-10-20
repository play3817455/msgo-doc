# 汇编证据 —— SC-0x8A10-battle-setwpnparam

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B22291`）

```asm
; VA: B22291（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B22291  push    0xC          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 4，线类型 u32（实体 ID（日志串 `ent_id=`））
B222CC  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B223DF → 含义锚点

; 字段 2 —— val：偏移 4，长度 4，线类型 f32（武器参数值（浮点；日志串 `val=`，打印器 `sub_B08660`））
B2230C  call    sub_B06250     ; 读取 f32
; 块内日志格式串 @B22409 → 含义锚点

; 字段 3 —— type：偏移 8，长度 4，线类型 u32（武器参数种类（日志串 `type=`））
B22330  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B22431 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B22340
B22340  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B22487 —— `vt[0x370]`（3 实参）
B22487  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x370h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; 字段 2 由 sub_B06250（f32）读取 @0xB2230C：fld dword ptr [ecx]; fstp dword ptr [dst]; add dword ptr [eax],4
; 去向以浮点实参下传：0xB22483  fld dword ptr [eax]；0xB22493  fstp [esp+1B44h+var_1B44]
```
