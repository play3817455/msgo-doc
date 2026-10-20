# 汇编证据 —— SC-0x4D96-battle-game_client_signal_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB166F7`）

```asm
; VA: 0xB166F7（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB166F7  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— sigval：偏移 0，长度 4，线类型 u32（信号值）
0xB16732  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "sigval=" → 含义锚点：0xB167D6

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB16763
0xB16763  push    <模块/错误码>
0xB16763  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB1682F
0xB1682F  mov     edx, [obj]
;       mov     edx, [edx+0x108h]
;       call    edx          ; vt[0x108]（1 实参）
```
