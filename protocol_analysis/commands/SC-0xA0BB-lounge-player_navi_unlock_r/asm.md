# 汇编证据 —— SC-0xA0BB-lounge-player_navi_unlock_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B6F597`）

```asm
; VA: B6F597（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xC
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B6F5D5`、`B6F6C4`
; 字段 2 —— unlocked_navi：偏移 4，长度 8，线类型 struct（解锁的导航信息（日志串 `unlocked_navi=`；成员 `navi_id`、`status`））
;   `B6F615`、`B6F6E7`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6F625
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x249）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6F747 —— `vt[0x580]`（2 实参）
```

## E5 补充证据

```asm
; 结构体读取：B6F615  call sub_B434B0 ; 2×u32 = 8B
; 元素打印器：sub_B49C80 成员名 `navi_id=` / `status=`（偏移 [edi]/[edi+4] 与线序一致）
```
