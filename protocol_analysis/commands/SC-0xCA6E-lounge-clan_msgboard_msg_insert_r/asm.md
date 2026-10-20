# 汇编证据 —— SC-0xCA6E-lounge-clan_msgboard_msg_insert_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `B7A66D`）

```asm
; VA: B7A66D（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x5
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb7a697|0xb7a6a6
; 字段 2 —— clan_kind：偏移 4，长度 1，线类型 u8（公会类别（日志串 `clan_kind=`））
;   0xb7a6d7|0xb7a6e6
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7A6F6
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1D8）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7A81B —— `vt[0x474]`（2 实参）
```
