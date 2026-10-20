# 汇编证据 —— SC-0x35F6-lounge-party_clan_rate_get_notice

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1` @ `0xB5BD40`）

```asm
; VA: 0xB5BD40（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5BD40  push    0x1          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— is_enable：偏移 0，长度 1，线类型 u8（是否启用）
0xB5BD7B  call    sub_B06230     ; 读 u8
; 块内日志格式串 "is_enable=" → 含义锚点：0xB5BE23

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5BDB2
0xB5BDB2  push    <模块/错误码>
0xB5BDB2  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5BE7F
0xB5BE7F  mov     edx, [obj]
;       mov     edx, [edx+0x22Ch]
;       call    edx          ; vt[0x22C]（1 实参）
```
