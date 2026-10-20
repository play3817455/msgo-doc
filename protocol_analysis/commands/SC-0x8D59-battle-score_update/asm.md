# 汇编证据 —— SC-0x8D59-battle-score_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1C` @ `B232AD`）

```asm
; VA: B232AD（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B232AD  push    0x1C          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— reason：偏移 0，长度 4，线类型 u32（得分原因（日志串 `reason=`））
B232E8  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B234C3 → 含义锚点

; 字段 2 —— point_gain：偏移 4，长度 2，线类型 u16（本次得分（日志串 `point_gain=`））
B23328  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B234EE → 含义锚点

; 字段 3 —— point_total：偏移 6，长度 4，线类型 u32（总分（日志串 `point_total=`））
B2334C  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B23518 → 含义锚点

; 字段 4 —— is_taskforce_aux：偏移 10，长度 2，线类型 u16（是否机动部队辅助（日志串 `is_taskforce_aux=`））
B23370  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B23543 → 含义锚点

; 字段 5 —— point_atk：偏移 12，长度 4，线类型 u32（攻击得分（日志串 `point_atk=`））
B23398  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B2356D → 含义锚点

; 字段 6 —— point_spt：偏移 16，长度 4，线类型 u32（支援得分（日志串 `point_spt=`））
B233C0  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B23597 → 含义锚点

; 字段 7 —— point_con：偏移 20，长度 4，线类型 u32（贡献得分（日志串 `point_con=`））
B233E8  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B235C1 → 含义锚点

; 字段 8 —— kill_streak_chain_num：偏移 24，长度 4，线类型 u32（连杀链数（日志串 `kill_streak_chain_num=`））
B23410  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B235E6 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B23424
B23424  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B23648 —— `vt[0x224]`（8 实参）
B23648  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x224h]
;       call    <reg>
```
