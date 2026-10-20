# 汇编证据 —— SC-0x924C-lounge-clan_kick_member_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x9` @ `B6CDAB`）

```asm
; VA: B6CDAB（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x9
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B6CDE9`、`B6CEFC`
; 字段 2 —— pilot_id_kick：偏移 4，长度 4，线类型 u32（被踢驾驶员 ID（日志串 `pilot_id_kick=`））
;   `B6CE29`、`B6CF26`
; 字段 3 —— clan_kind：偏移 8，长度 1，线类型 u8（战队种类（日志串 `clan_kind=`，字节打印器））
;   `B6CE4D`、`B6CF49`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6CE5D
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x1CB）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6CFB3 —— `vt[0x458]`（3 实参）
```
