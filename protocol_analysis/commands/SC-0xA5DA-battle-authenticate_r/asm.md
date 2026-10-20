# 汇编证据 —— SC-0xA5DA-battle-authenticate_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x2DE` @ `B25A8F`）

```asm
; VA: B25A8F（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
; 容量（缓冲上限，非线长）= 0x2DE
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（认证结果码（日志串 `result=`））
;   `B25AD6`、`B25EA6`
; 字段 2 —— room_id：偏移 4，长度 4，线类型 u32（房间 ID（日志串 `room_id=`））
;   `B25B19`、`B25ED3`
; 字段 3 —— room_name：偏移 8，长度 L+1，线类型 string（房间名（日志串 `room_name='...'`；NUL 结尾，槽预算 73））
;   `B25B41`、`B25F03`
; 字段 4 —— mission_id：偏移 var，长度 4，线类型 u32（任务 ID（日志串 `mission_id=`））
;   `B25B7E`、`B25F38`
; 字段 5 —— extrule_id：偏移 var，长度 4，线类型 u32（扩展规则 ID（日志串 `extrule_id=`））
;   `B25BA2`、`B25F62`
; 字段 6 —— dc_node_id：偏移 var，长度 4，线类型 u32（数据中心节点 ID（日志串 `dc_node_id=`））
;   `B25BC6`、`B25F8C`
; 字段 7 —— is_rankerbattle：偏移 var，长度 4，线类型 u32（是否排位战（日志串 `is_rankerbattle=`））
;   `B25BEE`、`B25FB6`
; 字段 8 —— map_id：偏移 var，长度 4，线类型 u32（地图 ID（日志串 `map_id=`））
;   `B25C16`、`B25FE0`
; 字段 9 —— is_vsclan：偏移 var，长度 1，线类型 u8（是否战队战（日志串 `is_vsclan=`，字节打印器））
;   `B25C3E`、`B26008`
; 字段 10 —— comeback_stat：偏移 var，长度 4，线类型 u32（回归状态（日志串 `comeback_stat=`））
;   `B25C66`、`B26034`
; 字段 11 —— is_playing：偏移 var，长度 1，线类型 u8（是否在游戏中（日志串 `is_playing=`））
;   `B25C8E`、`B2605C`
; 字段 12 —— is_netcafe：偏移 var，长度 1，线类型 u8（是否网咖（日志串 `is_netcafe=`））
;   `B25CB6`、`B26086`
; 字段 13 —— team：偏移 var，长度 1，线类型 u8（队伍（日志串 `team=`））
;   `B25CDE`、`B260B0`
; 字段 14 —— is_practice：偏移 var，长度 1，线类型 u8（是否演习（日志串 `is_practice=`））
;   `B25D06`、`B260DA`
; 字段 15 —— config：偏移 var，长度 34，线类型 struct（战斗配置（日志串 `config=`；claim 40 / 线长 34））
;   `B25D1F`、`B25D2E`、`B26104`
; 字段 16 —— progress：偏移 var，长度 46，线类型 struct（战斗进程（日志串 `progress=`；claim 64 / 线长 46））
;   `B25D47`、`B25D56`、`B2612E`
; 字段 17 —— expup_fgauge：偏移 var，长度 2，线类型 u16（经验加成槽（日志串 `expup_fgauge=`））
;   `B25D7E`、`B2615B`
; 字段 18 —— is_ev_caravan：偏移 var，长度 1，线类型 u8（是否活动商队（日志串 `is_ev_caravan=`））
;   `B25DA6`、`B26183`
; 字段 19 —— flag_wideuse：偏移 var，长度 1，线类型 u8（是否宽用标志（日志串 `flag_wideuse=`））
;   `B25DCE`、`B261AD`
; 字段 20 —— extrarule_xwar_info：偏移 var，长度 514，线类型 struct（跨服战扩展规则信息（日志串 `extrarule_xwar_info=`；claim 516 / 线长 514））
;   `B25DE7`、`B25DF6`、`B261D2`
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B25E0A
;   cmp 游标, 报文末尾；不等则走 vt[0x64]（push 1; push 0x3）报错
```

## E4 去向（用途锚点）

```asm
; VA: B262CD —— `vt[0x70]`（15 实参）
```

## E5 补充证据

```asm
; config：B25D1F call sub_B418C0 ; +0x28(=40)   /  B25D2E call sub_B077B0 ; 34B
; progress：B25D47 call sub_B05ED0 ; +0x40(=64) /  B25D56 call sub_B07880 ; 46B
; extrarule：B25DE7 call sub_B05EE0 ; +0x204(=516) / B25DF6 call sub_B08160 ; 514B
; 串槽：B25B2B push 49h ; B25B41 call sub_B02BA0
```
