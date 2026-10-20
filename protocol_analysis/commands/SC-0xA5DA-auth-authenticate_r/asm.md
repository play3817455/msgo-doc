# 汇编证据 —— SC-0xA5DA-auth-authenticate_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B04A04`）

```asm
; VA: B04A04（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x4
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（认证结果码（日志串 `result=`））
;   `B04A2F`、`B04ADD`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B04A65
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x3）报错
```

## E4 去向（用途锚点）

```asm
; VA: B04B38 —— `vt[0x6C]`（1 实参）
```

## E5 补充证据

```asm
; 闭合（成功分支）：B04A61  mov ebx,[var_10C]
;                B04A65  cmp ebx,[var_108]
;                B04A69  jnz 0xB04A3B（错误出口）
; 收尾：无 sub_B05D90/sub_B41110（auth 协议类口径）
```
