# 汇编证据 —— SC-0xD1B3-battle-game_respawn_post_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x7D4` @ `B2BC4D`）

```asm
; VA: B2BC4D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x7D4
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— post_num：偏移 0，长度 4，线类型 u32（重生点条目数（上限 50））
;   0xb2bc78|0xb2bca1
; 字段 2 —— post_progress：偏移 4，长度 25n，线类型 array<respawn_post,50>（重生点进度列表（日志串 `post_progress={`））
;   0xb2bcb3|0xb2bcd0
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2BCFB
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x41）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2BE3B —— `vt[0x118]`（2 实参）
```
