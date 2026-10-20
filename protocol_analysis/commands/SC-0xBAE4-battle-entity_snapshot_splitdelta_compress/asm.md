# 汇编证据 —— SC-0xBAE4-battle-entity_snapshot_splitdelta_compress

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x750C` @ `B29DDA`）

```asm
; VA: B29DDA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x750C
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— frame_count：偏移 0，长度 4，线类型 u32（快照帧号（日志串 `frame_count=`））
;   0xb29e04|0xb29e13
; 字段 2 —— remain_msec：偏移 4，长度 4，线类型 u32（剩余毫秒（日志串 `remain_msec=`））
;   0xb29e41|0xb29e50
; 字段 3 —— zbuff_num：偏移 8，长度 4，线类型 u32（压缩数据字节数（上限 30720））
;   0xb29e66|0xb29e8f
; 字段 4 —— zbuff：偏移 12，长度 n，线类型 array<u8,30720>（压缩快照字节串（日志串 `zbuff={` 逐字节打印））
;   0xb29ea4|0xb29ebd
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B29EE3
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x63）报错
```

## E4 去向（用途锚点）

```asm
; VA: B2A084 —— `vt[0x188]`（4 实参）
```
