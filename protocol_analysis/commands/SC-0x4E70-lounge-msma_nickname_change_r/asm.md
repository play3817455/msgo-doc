# 汇编证据 —— SC-0x4E70-lounge-msma_nickname_change_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x49` @ `0xB5FAD3`）

```asm
; VA: 0xB5FAD3（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5FAD3  push    0x49          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5FB0E  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5FC15

; 字段 2 —— uniqid：偏移 4，长度 8，线类型 u64（机体唯一 ID（u64））
0xB5FB4E  call    sub_B06200     ; 读 u64
; 块内日志格式串 "uniqid=" → 含义锚点：0xB5FC43

; 字段 3 —— nickname：偏移 12，长度 61，线类型 str（机体昵称（槽位预算 `0x3D`=61））
0xB5FB66  call    sub_B02BA0     ; 读 str
; 块内日志格式串 "nickname=" → 含义锚点：0xB5FC6B

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5FB9D
0xB5FB9D  push    <模块/错误码>
0xB5FB9D  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5FCDF
0xB5FCDF  mov     edx, [obj]
;       mov     edx, [edx+0x284h]
;       call    edx          ; vt[0x284]（4 实参）
```
