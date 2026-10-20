# 汇编证据 —— SC-0x97EC-battle-roomlobby_pick_vote_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B2488D`）

```asm
; VA: B2488D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x4
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（选择投票结果码（日志串 `result=`））
;   `B248CB`、`B2496F`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B248F4
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1D）报错
```

## E4 去向（用途锚点）

```asm
; VA: B249C8 —— `vt[0xB8]`（1 实参）
```
