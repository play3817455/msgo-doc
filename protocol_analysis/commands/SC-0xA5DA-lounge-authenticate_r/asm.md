# 汇编证据 —— SC-0xA5DA-lounge-authenticate_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x8` @ `B70159`）

```asm
; VA: B70159（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x8
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（认证结果码（日志串 `result=`））
;   `B70197`、`B7027D`
; 字段 2 —— admin_lv：偏移 4，长度 4，线类型 u32（管理员等级（日志串 `admin_lv=`））
;   `B701D4`、`B702A2`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B701E4
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x3）报错
```

## E4 去向（用途锚点）

```asm
; VA: B702FF —— `vt[0x6C]`（2 实参）
```
