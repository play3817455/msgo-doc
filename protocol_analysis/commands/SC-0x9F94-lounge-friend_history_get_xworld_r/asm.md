# 汇编证据 —— SC-0x9F94-lounge-friend_history_get_xworld_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x352C` @ `B6E8ED`）

```asm
; VA: B6E8ED（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x352C
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码（日志串 `result=`））
;   `B6E92E`、`B6EB09`
; 字段 2 —— friend_histories_cnt：偏移 4，长度 4，线类型 u32（好友履历个数（上界 `cmp ebx,64h` @`B6E98C` ⇒ ≤100））
;   `B6E960`
; 字段 3 —— friend_histories：偏移 8，长度 113·N1，线类型 array<struct,N1>（好友履历列表（日志 `friend_histories={pilot_id,name,last_in,troops,...}`））
;   `B6E99B`、`B6E9BA`、`B6EB24`
; 字段 4 —— block_widlist_cnt：偏移 var，长度 4，线类型 u32（屏蔽世界 ID 个数（上界 `cmp …,64h` @`B6EA01` ⇒ ≤100））
;   `B6E9F1`
; 字段 5 —— block_widlist：偏移 var，长度 4·N2，线类型 array<u32,N2>（屏蔽世界 ID 列表（日志 `block_widlist={...}`））
;   `B6EA1A`、`B6EA3A`、`B6EB9E`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B6EA6A
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x159）报错
```

## E4 去向（用途锚点）

```asm
; VA: B6EC60 —— `vt[0x368]`（5 实参）
```

## E5 补充证据

```asm
; 数组 1 预留：B6E99B  call sub_B415D0 ; 按 N1 推进，槽步进 0x84(=132)
; 数组 1 元素：B6E9BA  call sub_B43100 ; 整函数消费 113B
; 数组 2 预留：B6EA1A  call sub_B41850 ; 按 N2 推进，槽步进 4
; 数组 2 元素：B6EA3A  call sub_B02DD0 ; u32
```
