# 汇编证据 —— SC-0xA90E-lounge-chat_all_down

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xD6` @ `B7141F`）

```asm
; VA: B7141F（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xD6
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id：偏移 0，长度 4，线类型 u32（发言驾驶员 ID（日志串 `pilot_id=`））
;   B71460
; 字段 2 —— troops：偏移 4，长度 4，线类型 u32（所属阵营/部队（日志串 `troops=`））
;   B7149D
; 字段 3 —— pilot_name：偏移 8，长度 变长(槽 25)，线类型 bytes(NUL 串)（发言者名（日志串 `pilot_name="..."`））
;   B714C2|B714AF
; 字段 4 —— msg：偏移 var，长度 变长(槽 181)，线类型 bytes(NUL 串)（聊天内容（日志串 `msg="..."`））
;   B714D9|B714CE
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B714E9
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x4A）报错
```

## E4 去向（用途锚点）

```asm
; VA: B71681 —— `vt[0x10C]`（4 实参）
```
