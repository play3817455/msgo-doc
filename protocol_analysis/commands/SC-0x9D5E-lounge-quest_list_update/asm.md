# 汇编证据 —— SC-0x9D5E-lounge-quest_list_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B6E679`）

```asm
; VA: B6E679（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xC
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— quest_id：偏移 0，长度 4，线类型 u32（任务 ID（日志串 `quest_id=`））
;   `B6E6B7`、`B6E7CA`
; 字段 2 —— achieve_denom：偏移 4，长度 4，线类型 u32（达成度分母（日志串 `achieve_denom=`））
;   `B6E6F7`、`B6E7F4`
; 字段 3 —— achieve_num：偏移 8，长度 4，线类型 u32（达成度分子（日志串 `achieve_num=`））
;   `B6E71B`、`B6E819`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6E72B
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x182）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6E880 —— `vt[0x3C4]`（3 实参）
```
