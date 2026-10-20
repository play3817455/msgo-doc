# 汇编证据 —— SC-0xB8F4-lounge-heroms_exp_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x14` @ `B758E2`）

```asm
; VA: B758E2（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x14
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pilot_id：偏移 0，长度 4，线类型 u32（驾驶员 ID（日志串 `pilot_id=`））
;   B75920
; 字段 2 —— favms_id：偏移 4，长度 4，线类型 u32（喜爱机体 ID（日志串 `favms_id=`））
;   B75960
; 字段 3 —— exp_mine：偏移 8，长度 4，线类型 u32（我的经验值（日志串 `exp_mine=`））
;   B75984
; 字段 4 —— exp_top：偏移 12，长度 4，线类型 u32（榜首经验值（日志串 `exp_top=`））
;   B759A8
; 字段 5 —— my_rank：偏移 16，长度 4，线类型 u32（我的名次（日志串 `my_rank=`））
;   B759D0
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B759E4
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x242）报错
```

## E4 去向（用途锚点）

```asm
; VA: B75B9B —— `vt[0x574]`（5 实参）
```
