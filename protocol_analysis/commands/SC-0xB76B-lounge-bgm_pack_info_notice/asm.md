# 汇编证据 —— SC-0xB76B-lounge-bgm_pack_info_notice

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x48` @ `B75187`）

```asm
; VA: B75187（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x48
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— pack_num：偏移 0，长度 4，线类型 u32（BGM 包条目数（上限 16））
;   B751B7|B751E3
; 字段 2 —— bgm_pack：偏移 4，长度 4·n，线类型 array<u32,16>（已拥有 BGM 包 ID 列表（日志串 `bgm_pack={...}`））
;   B751F2|B7520F|B7521B
; 字段 3 —— tmp：偏移 var，长度 4，线类型 u32（附加数值（日志串 `tmp=`））
;   B75251
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B7527D
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x202）报错
```

## E4 去向（用途锚点）

```asm
; VA: B753F0 —— `vt[0x4D0]`（3 实参）
```
