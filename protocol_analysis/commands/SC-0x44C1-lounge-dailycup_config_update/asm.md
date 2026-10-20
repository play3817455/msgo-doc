# 汇编证据 —— SC-0x44C1-lounge-dailycup_config_update

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xA0` @ `0xB5DD05`）

```asm
; VA: 0xB5DD05（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
0xB5DD05  push    0xA0          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— dailycup_conf：偏移 0，长度 73，线类型 struct（当日每日杯配置（claim `0x50`=80 / 线长 73，读取器 `sub_B46E80`））
0xB5DD43  call    复合读取器（元素/结构体，见 notes.md）     ; 读 struct
; 块内日志格式串 "dailycup_conf=" → 含义锚点：0xB5DE30

; 字段 2 —— dailycup_conf_next：偏移 80，长度 73，线类型 struct（次日每日杯配置（claim `0x50`=80 / 线长 73））
0xB5DD83  call    复合读取器（元素/结构体，见 notes.md）     ; 读 struct
; 块内日志格式串 "dailycup_conf_next=" → 含义锚点：0xB5DE55

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5DDBA
0xB5DDBA  push    <模块/错误码>
0xB5DDBA  call    sub_B41110     ; 取解码缓冲/收尾
```

## E4 去向（用途锚点）

```asm
; VA: 0xB5DEB3
0xB5DEB3  mov     edx, [obj]
;       mov     edx, [edx+0x540h]
;       call    edx          ; vt[0x540]（2 实参）
```
