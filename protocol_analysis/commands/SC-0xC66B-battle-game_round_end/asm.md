# 汇编证据 —— SC-0xC66B-battle-game_round_end

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x42` @ `B2B072`）

```asm
; VA: B2B072（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x42
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— win_team：偏移 0，长度 1，线类型 u8（获胜阵营（日志串 `win_team=`））
;   0xb2b09c|0xb2b0ab
; 字段 2 —— win_troops：偏移 1，长度 1，线类型 u8（获胜部队（日志串 `win_troops=`））
;   0xb2b0d9|0xb2b0e8
; 字段 3 —— progress：偏移 2，长度 46，线类型 struct(64)（战局进度快照（日志串 `progress=` 打印器 `sub_B0A820`））
;   0xb2b0fd|0xb2b10c
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2B11C
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x36）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2B26B —— `vt[0xFC]`（3 实参）
```
