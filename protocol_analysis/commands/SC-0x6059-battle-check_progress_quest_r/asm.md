# 汇编证据 —— SC-0x6059-battle-check_progress_quest_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x88` @ `0xB1B6A6`）

```asm
; VA: 0xB1B6A6（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB1B6A6  push    0x88          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— check_quest：偏移 0，长度 133，线类型 struct<check_quest>（任务进度检查结构（claim 136 / 线长 133，读取器 `sub_B06C00`））
0xB1B6D5  call    复合读取器（元素/结构体，见 notes.md）     ; struct<check_quest>
; 块内日志格式串 "check_quest=" → 含义锚点：0xB1B78C

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB1B710
0xB1B710  mov     <reg>, [esp+…+游标]; cmp <reg>, [esp+…+末尾]
0xB1B710  call    sub_B05D90     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB1B7E5
0xB1B7E5  mov     <reg>, [obj]; mov <reg>, [<reg>+0x348h]
;       call    <reg>          ; vt[0x348]（1 实参）
```
