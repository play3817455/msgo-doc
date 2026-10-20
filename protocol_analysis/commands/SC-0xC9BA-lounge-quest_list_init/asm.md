# 汇编证据 —— SC-0xC9BA-lounge-quest_list_init

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1178` @ `B79D57`）

```asm
; VA: B79D57（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x1178
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— list_all_num：偏移 0，长度 4，线类型 u32（任务条目数（上限 31））
;   0xb79d82|0xb79dae
; 字段 2 —— list_all：偏移 4，长度 138n，线类型 array<quest_info,31>（任务列表（日志串 `list_all={`））
;   0xb79dbd|0xb79dda
; 字段 3 —— progress_id：偏移 var，长度 4，线类型 u32（当前进度任务 ID（日志串 `progress_id=`））
;   0xb79e10|0xb79e1f
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B79E4B
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x181）报错
```

## E4 去向（用途锚点）

```asm
; VA: B79FC7 —— `vt[0x3C0]`（3 实参）
```
