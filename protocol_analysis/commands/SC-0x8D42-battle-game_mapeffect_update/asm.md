# 汇编证据 —— SC-0x8D42-battle-game_mapeffect_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `B22855`）

```asm
; VA: B22855（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B22855  push    0x5          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— fx_id：偏移 0，长度 4，线类型 u32（地图特效 ID（日志串 `fx_id=`））
B22890  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B22976 → 含义锚点

; 字段 2 —— is_scale：偏移 4，长度 1，线类型 u8（是否缩放（日志串 `is_scale=`））
B228CD  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B22999 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B228DD
B228DD  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B229F0 —— `vt[0x120]`（2 实参）
B229F0  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x120h]
;       call    <reg>
```
