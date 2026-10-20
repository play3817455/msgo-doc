# 汇编证据 —— SC-0xBDC6-battle-game_read_ahead_route_notice

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x104` @ `B2AAE7`）

```asm
; VA: B2AAE7（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x104
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— route_num：偏移 0，长度 4，线类型 u32（航路点数（上限 64））
;   0xb2ab12|0xb2ab3b
; 字段 2 —— read_ahead_route：偏移 4，长度 4n，线类型 array<u32,64>（预读航路点列表（日志串 `read_ahead_route={`））
;   0xb2ab4d|0xb2ab6a
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2AB95
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x34）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2ACCF —— `vt[0xF4]`（2 实参）
```
