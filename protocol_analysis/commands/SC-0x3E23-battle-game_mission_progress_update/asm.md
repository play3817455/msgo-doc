# 汇编证据 —— SC-0x3E23-battle-game_mission_progress_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x40` @ `0xB14DF9`）

```asm
; VA: 0xB14DF9（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB14DF9  push    0x40          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— mprogress：偏移 0，长度 46，线类型 struct（任务进度结构（claim `0x40`=64 / 线长 46，读取器 `sub_B07880`））
0xB14E34  call    复合读取器（元素/结构体，见 notes.md）     ; 读 struct
; 块内日志格式串 "mprogress=" → 含义锚点：0xB14ED6

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB14E65
0xB14E65  push    <模块/错误码>
0xB14E65  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB14F2F
0xB14F2F  mov     edx, [obj]
;       mov     edx, [edx+0x114h]
;       call    edx          ; vt[0x114]（1 实参）
```
