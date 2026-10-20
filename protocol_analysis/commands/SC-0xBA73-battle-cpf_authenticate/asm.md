# 汇编证据 —— SC-0xBA73-battle-cpf_authenticate

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x84` @ `B2A0B9`）

```asm
; VA: B2A0B9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x84
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— data_num：偏移 0，长度 4，线类型 u32（CPF 认证数据长度（上限 128））
;   B2A0EC|B2A118
; 字段 2 —— data：偏移 4，长度 n，线类型 array<u8,128>（CPF 认证数据字节串（日志串 `data={...}`，逐字节十六进制打印））
;   B2A12D|B2A14C
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B2A175
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x11B）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2A2B7 —— `vt[0x35C]`（2 实参）
```
