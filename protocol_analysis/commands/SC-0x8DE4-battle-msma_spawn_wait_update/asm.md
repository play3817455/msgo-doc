# 汇编证据 —— SC-0x8DE4-battle-msma_spawn_wait_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `B22A31`）

```asm
; VA: B22A31（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B22A31  push    0x5          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— deck_index：偏移 0，长度 1，线类型 u8（卡组槽序号（日志串 `deck_index=`））
B22A6C  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B22B74 → 含义锚点

; 字段 2 —— respawn_wait_sec：偏移 1，长度 2，线类型 u16（重出等待秒数（日志串 `respawn_wait_sec=`））
B22AA9  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B22BA1 → 含义锚点

; 字段 3 —— respawn_wait_max：偏移 3，长度 2，线类型 u16（重出等待上限（日志串 `respawn_wait_max=`））
B22ACD  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B22BC7 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B22ADD
B22ADD  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B22C1C —— `vt[0x138]`（3 实参）
B22C1C  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x138h]
;       call    <reg>
```
