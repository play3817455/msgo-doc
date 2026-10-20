# 汇编证据 —— SC-0x47C2-battle-conquer_spoint_change

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB155BA`）

```asm
; VA: 0xB155BA（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB155BA  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— conquer：偏移 0，长度 4，线类型 u32（原始 conquer 值；具体数值含义待定）
0xB155F5  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "conquer=" → 含义锚点：0xB1569F

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB1562C
0xB1562C  push    <模块/错误码>
0xB1562C  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB156F8
0xB156F8  mov     edx, [obj]
;       mov     edx, [edx+0x328h]
;       call    edx          ; vt[0x328]（1 实参）
```

## E5 客户端消费者（13338 正确 v15 IDB 静态复核，2026-10-11）

`CGVOProtoBattle` vtable `0xEED7AC + 0x328` 指向 `BAAA30→AFCB70`。业务函数将 u32 仅折成 `a1 != 0` 写入 `app+0x659E1`。该字节读取点 `66A2E0` 位于地图对象/玩家交互资格检查：当机关 `type==2` 且本地玩家满足相应分支时，字节为 0 会拒绝交互。开战初始化函数 `44B150` 在 `44B811` 写同一字节，值为 `game_begin_args+0x1C == 0`。包装函数 `BA9120` 将第7个参数（`0x1365.is_disable_conq_sp`，payload offset 24）复制到输入块 `+0x1C`，因此开战初值严格为 `is_disable_conq_sp==0`；之后 `0x47C2` 将它覆盖为 `conquer!=0`。这闭合了包字段到初始门控的映射，但没有解释服务端何时切换该门控。不能把报文字段当作连续积分或单据点进度。完整交叉记录见 `serverv/docs/data/ida-v15-conquer-spoint-gate-20261011.json`。
