# 汇编证据 —— SC-0x986D-lounge-pilot_delete_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xD` @ `B6DB7E`）

```asm
; VA: B6DB7E（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xD
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B6DBBC`、`B6DCEE`
; 字段 2 —— pilot_id：偏移 4，长度 4，线类型 u32（驾驶员 ID（日志串 `pilot_id=`））
;   `B6DBF9`、`B6DD18`
; 字段 3 —— del_kind：偏移 8，长度 1，线类型 u8（删除种类（日志串 `del_kind=`，字节打印器））
;   `B6DC1D`、`B6DD40`
; 字段 4 —— del_remain_sec：偏移 9，长度 4，线类型 u32（删除剩余秒（日志串 `del_remain_sec=`））
;   `B6DC41`、`B6DD67`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6DC55
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x14）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6DDD6 —— `vt[0x90]`（4 实参）
```
