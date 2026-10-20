# 汇编证据 —— SC-0xBA73-lounge-cpf_authenticate

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x84` @ `B76A11`）

```asm
; VA: B76A11（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x84
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— data_num：偏移 0，长度 4，线类型 u32（CPF 认证数据长度）
;   0xb76a3c|0xb76a68
; 字段 2 —— data：偏移 4，长度 n，线类型 array<u8,128>（CPF 认证数据字节串（日志串 `data={` 逐字节十六进制打印））
;   0xb76a7a|0xb76a91
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B76ABA
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x212）报错
```

## E4 去向（用途锚点）

```asm
; VA: B76C01 —— `vt[0x500]`（2 实参）
```
