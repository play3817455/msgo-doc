# 汇编证据 —— SC-0x4632-lounge-replay_auth_get_downloadkey_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6E` @ `0xB5E505`）

```asm
; VA: 0xB5E505（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5E505  push    0x6E          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（结果码）
0xB5E540  call    sub_B02DD0     ; 读 u32
; 块内日志格式串 "result=" → 含义锚点：0xB5E644

; 字段 2 —— download_key：偏移 4，长度 41，线类型 str（下载密钥（槽位预算 `0x29`=41））
0xB5E581  call    sub_B02BA0     ; 读 str
; 块内日志格式串 "download_key=" → 含义锚点：0xB5E671

; 字段 3 —— secret_key：偏移 45，长度 65，线类型 str（校验密钥（槽位预算 `0x41`=65））
0xB5E595  call    sub_B02BA0     ; 读 str
; 块内日志格式串 "secret_key=" → 含义锚点：0xB5E6A4

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5E5CC
0xB5E5CC  push    <模块/错误码>
0xB5E5CC  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5E712
0xB5E712  mov     edx, [obj]
;       mov     edx, [edx+0x4E8h]
;       call    edx          ; vt[0x4E8]（3 实参）
```
