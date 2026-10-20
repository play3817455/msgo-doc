# 汇编证据 —— SC-0xB92F-lounge-clan_mshipbid_request_cancel_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `B761A0`）

```asm
; VA: B761A0（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x5
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   B761DE
; 字段 2 —— clan_kind：偏移 4，长度 1，线类型 u8（公会类别（日志串 `clan_kind=`））
;   B7621E|B7633E
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7622E
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1B7）报错
```

## E4 去向（用途锚点）

```asm
; VA: B76353 —— `vt[0x430]`（2 实参）
```
