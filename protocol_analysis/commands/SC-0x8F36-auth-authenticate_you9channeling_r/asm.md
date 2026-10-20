# 汇编证据 —— SC-0x8F36-auth-authenticate_you9channeling_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `B0467E`）

```asm
; VA: B0467E（分配器指纹 `mov edx,[eax+78h]` + `push IMM; call edx`）
B0467E  push    0x4          ; 容量（缓冲上限，非线长）
; 紧随其后：call edx（vt[0x78] 解码缓冲分配器）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— result：偏移 0，长度 4，线类型 u32（认证结果码（日志串 `result=`））
B046B5  ; 内联读取（内联拷贝（`mov ecx,[ebx]; mov [edx],ecx`））
; 块内日志格式串 @B04729 → 含义锚点

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: B046AB
B046AB  cmp     cursor, end      ; 不等则走 vt[0x64] 报错
; 收尾：push <模块id>; call sub_B02C90
```

## E4 去向（用途锚点）

```asm
; VA: B0477E —— `vt[0x78]`（1 实参）
B0477E  mov     <reg>, [obj]
;       mov     <reg>, [<reg>+0x78h]
;       call    <reg>
```

## E5 复合读取器 / 预留原语（本命令专用取证）

```asm
; 0xB04693  lea     edi, [ebx+4]                  ; 游标 ebx + 4
; 0xB04696  cmp     edi, [esp+124h+var_108]      ; 与报文末尾比较
; 0xB046A5  ja      loc_B047AD                  ; 越界 → vt[0x64](1, 9)
; 0xB046AB  cmp     edi, [esp+124h+var_108]      ; 入口闭合校验
; 0xB046AF  mov     ecx, [ebx]                  ; 内联读 4 字节
; 0xB046B5  mov     [edx], ecx                  ; 写入预留缓冲
; 0xB046B7  jnz     loc_B047AD                  ; 不相等 → 报错
; 0xB04776  mov     eax, [esp+124h+var_110]
; 0xB0477A  mov     ecx, [eax]
; 0xB0477C  mov     edx, [esi]
; 0xB0477E  mov     edx, [edx+78h]              ; 去向：客户端对象 vt[0x78]
; 0xB04784  call    edx                         ; 1 实参
; 0xB04667  push    9 / call sub_B02C90         ; auth 协议类守卫
```
