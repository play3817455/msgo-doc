# 汇编证据 —— SC-0xD18B-lounge-season_rankerbattle_state_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B7BF6D`）

```asm
; VA: B7BF6D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— state：偏移 0，长度 4，线类型 u32（排位战状态（日志串 `state=`））
;   0xb7bf97|0xb7bfa6
; 字段 2 —— rb_rank：偏移 4，长度 4，线类型 u32（排位名次（日志串 `rb_rank=`））
;   0xb7bfd7|0xb7bfe6
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7BFF6
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x255）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7C11A —— `vt[0x5A0]`（2 实参）
```
