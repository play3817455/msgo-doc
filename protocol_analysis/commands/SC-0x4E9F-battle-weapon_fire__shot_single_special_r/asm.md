# 汇编证据 —— SC-0x4E9F-battle-weapon_fire__shot_single_special_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `0xB16A03`）

```asm
; VA: 0xB16A03（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB16A03  push    0x6          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— ent_id：偏移 0，长度 2，线类型 u16（实体 ID）
0xB16A3E  call    sub_B02DF0     ; u16
; 块内日志格式串 "ent_id=" → 含义锚点：0xB16B25

; 字段 2 —— itemid：偏移 2，长度 4，线类型 u32（武器道具 ID）
0xB16A7B  call    sub_B02DD0     ; u32
; 块内日志格式串 "itemid=" → 含义锚点：0xB16B4A

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB16A8B
0xB16A8B  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB16A8B  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB16BAB
0xB16BAB  mov     <reg>, [obj]; mov <reg>, [<reg>+0x1A4h]
;       call    <reg>          ; vt[0x1A4]（2 实参）
```
