# 汇编证据 —— SC-0xCE1A-lounge-block_list_get_idwlist_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x32C` @ `B7B3D7`）

```asm
; VA: B7B3D7（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x32C
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   0xb7b401|0xb7b410
; 字段 2 —— block_id_num：偏移 4，长度 4，线类型 u32（屏蔽 ID 个数（上限 100））
;   0xb7b442|0xb7b46e
; 字段 3 —— block_idlist：偏移 8，长度 4n，线类型 array<u32,100>（屏蔽 ID 列表（日志串 `block_idlist={`））
;   0xb7b47d|0xb7b49e
; 字段 4 —— block_wid_num：偏移 var，长度 4，线类型 u32（屏蔽世界 ID 个数（上限 100））
;   0xb7b4d2|0xb7b4e6
; 字段 5 —— block_widlist：偏移 var，长度 4m，线类型 array<u32,100>（屏蔽世界 ID 列表（日志串 `block_widlist={`））
;   0xb7b4f9|0xb7b51a
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7B548
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x15F）报错
```

## E4 去向（用途锚点）

```asm
; VA: B7B730 —— `vt[0x374]`（5 实参）
```
