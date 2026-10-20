# 汇编证据 —— SC-0xA72F-lounge-msma_sp_parts_level_update

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `B70AAA`）

```asm
; VA: B70AAA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0xC
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— uniqid_ms：偏移 0，长度 8，线类型 u64（机体唯一 ID（日志串 `uniqid_ms=`））
;   `B70AE8`、`B70BD7`
; 字段 2 —— sp_parts：偏移 8，长度 4，线类型 u32（SP 部件等级（日志串 `sp_parts=`））
;   `B70B28`、`B70BFC`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B70B38
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x124）报错
```

## E4 去向（用途锚点）

```asm
; VA: B70C60 —— `vt[0x2F4]`（3 实参）
```
