# 汇编证据 —— SC-0xB313-lounge-system_message

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB9` @ `B735AF`）

```asm
; VA: B735AF（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xB9
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— msg：偏移 0，长度 变长(槽 181)，线类型 bytes(NUL 串)（系统消息正文（日志串 `msg="..."`））
;   B735F1|B735D7
; 字段 2 —— color：偏移 var，长度 4，线类型 u32（显示颜色（日志串 `color=`））
;   B73631
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B73641
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x221）报错
```

## E4 去向（用途锚点）

```asm
; VA: B73771 —— `vt[0x51C]`（2 实参）
```
