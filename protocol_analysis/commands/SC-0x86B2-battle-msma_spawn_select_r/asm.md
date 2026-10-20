# 汇编证据 —— SC-0x86B2-battle-msma_spawn_select_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x53` @ `B21F3F`）

```asm
; VA: B21F3F（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B21F3F  push    0x53          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B21F7A  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B220EC → 含义锚点

; 字段 2 —— ms_index：偏移 4，长度 4，线类型 u32（机体序号（日志串 `ms_index=`））
B21FB7  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B22116 → 含义锚点

; 字段 3 —— post_index：偏移 8，长度 4，线类型 u32（出生点序号（日志串 `post_index=`））
B21FDB  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B22140 → 含义锚点

; 字段 4 —— spt_spot_index：偏移 12，长度 4，线类型 u32（支援点位序号（日志串 `spt_spot_index=`））
B21FFF  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B2216A → 含义锚点

; 字段 5 —— respawn_ent_id：偏移 16，长度 2，线类型 u16（重生实体 ID（日志串 `respawn_ent_id=`））
B22027  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B22195 → 含义锚点

; 字段 6 —— script_ini：偏移 18，长度 65，线类型 str（脚本配置名（日志串 `script_ini="`））
B22043  call    sub_B02BA0     ; 读取 str
; 块内日志格式串 @B221BD → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2206C
B2206C  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B2221A —— `vt[0x13C]`（6 实参）
B2221A  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x13Ch]
;       call    <reg>
```
