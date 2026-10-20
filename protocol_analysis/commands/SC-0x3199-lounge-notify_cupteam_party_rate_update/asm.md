# 汇编证据 —— SC-0x3199-lounge-notify_cupteam_party_rate_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `0xB5B914`）

```asm
; VA: 0xB5B914（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5B914  push    0x8          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— cupteam_rate：偏移 0，长度 4，线类型 u32（组队倍率）
0xB5B94F  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "cupteam_rate=" → 含义锚点：0xB5BA3E

; 字段 2 —— last_bracket_id：偏移 4，长度 4，线类型 u32（最近分档 ID）
0xB5B98F  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "last_bracket_id=" → 含义锚点：0xB5BA63

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5B9C6
0xB5B9C6  push    <模块/错误码>
0xB5B9C6  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5BAC3
0xB5BAC3  mov     edx, [obj]
;       mov     edx, [edx+0x4FCh]
;       call    edx          ; vt[0x4FC]（2 实参）
```
