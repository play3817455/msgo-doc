# 汇编证据 —— SC-0x9F9B-lounge-season_rankerbattle_get_entitled_pilot_list_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x3B72` @ `B6EED9`）

```asm
; VA: B6EED9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x3B72
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B6EF1A`、`B6F098`
; 字段 2 —— ranking_info：偏移 4，长度 10，线类型 struct（排行检索条件（日志串 `order=`；5 × u16，无线上计数））
;   `B6EF4B`、`B6EF5A`、`B6F0C0`
; 字段 3 —— ranking_cnt：偏移 14，长度 4，线类型 u32（排行条目数（上界 `cmp ebx,0C8h` @`B6EF9C` ⇒ ≤200））
;   `B6EF70`
; 字段 4 —— ranking：偏移 18，长度 73N，线类型 array<struct,N>（排行列表（日志 `ranking={score,pilot_id,name,troops,...}`））
;   `B6EFAE`、`B6EFCB`、`B6F0DD`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6EFF9
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x259）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6F19D —— `vt[0x5AC]`（4 实参）
```

## E5 补充证据

```asm
; 定长结构体预留：B6EF4B  call sub_B41220 ; +0x0A(=10)
; 结构体读取：B6EF5A  call sub_B46420 ; 5×u16 = 10B
; 数组预留：B6EFAE  call sub_B41A60 ; 按 N 推进，槽步进 0x4C(=76)
; 元素读取：B6EFCB  call sub_B469F0 ; 73B
```
