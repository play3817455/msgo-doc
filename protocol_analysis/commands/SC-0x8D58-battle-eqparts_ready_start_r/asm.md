# 汇编证据 —— SC-0x8D58-battle-eqparts_ready_start_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xD` @ `B22FBA`）

```asm
; VA: B22FBA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B22FBA  push    0xD          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
B22FF5  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B23158 → 含义锚点

; 字段 2 —— frame_count：偏移 4，长度 4，线类型 u32（帧数（日志串 `frame_count=`））
B23035  call    sub_B02DD0     ; 读取 u32
; 块内日志格式串 @B23182 → 含义锚点

; 字段 3 —— AI_ent_id：偏移 8，长度 2，线类型 u16（AI 实体 ID（日志串 `AI_ent_id=`））
B23059  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B231AD → 含义锚点

; 字段 4 —— group_id：偏移 10，长度 2，线类型 u16（分组 ID（日志串 `group_id=`））
B2307D  call    sub_B02DF0     ; 读取 u16
; 块内日志格式串 @B231D8 → 含义锚点

; 字段 5 —— reason：偏移 12，长度 1，线类型 u8（原因（日志串 `reason=`））
B230A5  call    sub_B06230     ; 读取 u8
; 块内日志格式串 @B231FB → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B230B9
B230B9  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B05D90
```

## E4 去向（用途锚点）

```asm
; VA: B23252 —— `vt[0x214]`（5 实参）
B23252  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x214h]
;       call    <reg>
```
