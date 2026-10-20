# 汇编证据 —— SC-0xA103-authenticate_bnpotp_input

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 opcode 的读取与分发（证明 opcode = 0xA103）

```asm
; VA: 0xB03D5F .. 0xB03D8A（分发器序言）
0xB03D5F  mov     ebp, [esp+124h+arg_0]      ; ebp = 缓冲区基址 buf
0xB03D66  mov     eax, [esp+124h+arg_4]      ; eax = 长度 len
0xB03D6D  lea     edi, [eax+ebp]             ; edi = buf + len（末尾）
0xB03D70  lea     ebx, [ebp+2]               ; ebx = buf + 2（负载游标）
0xB03D73  cmp     ebx, edi
0xB03D7D  ja      loc_B03E2B                 ; len < 2 ⇒ 整帧非法
0xB03D83  movzx   eax, word ptr [ebp+0]      ; ← opcode 读取，u16（零扩展 ⇒ 无符号）
0xB03D87  movzx   eax, ax
; ... 比较树 ...
0xB047D3  cmp     eax, 0A103h                ; ← opcode 判定
0xB047D8  jz      loc_B04B61                 ; ⇒ 处理块 = 0xB04B61
```

## E2 处理块起始的长度校验（证明负载 0 字节）

```asm
; VA: 0xB04B61 .. 0xB04B8E
0xB04B61  push    4
0xB04B63  call    sub_B02C90                 ; 本 case 的开关/阈值判定
0xB04B68  test    al, al
0xB04B6A  jz      loc_B04C46                 ; 关闭时直接返回
0xB04B70  cmp     ebx, edi                   ; 负载游标 vs 缓冲区末尾
0xB04B72  jz      short loc_B04B86           ; ← 相等 ⇒ 负载长度必须为 0
0xB04B74  mov     eax, [esi]
0xB04B76  mov     edx, [eax+64h]
0xB04B79  push    1
0xB04B7B  push    4                          ; 错误码 4：长度不符
0xB04B7D  mov     ecx, esi
0xB04B7F  call    edx                        ; vt[0x64] = 报错
0xB04B81  jmp     loc_B04C46
```

**结论**：本处理块内不存在任何读取器调用，且唯一长度约束是 `游标 == 末尾`
⇒ 报文体 = 2 字节（仅 opcode）。

## E3 非字段代码：日志与计数（避免被误判为字段）

```asm
; VA: 0xB04B86 .. 0xB04BF2（trace：名字 + id）
0xB04B86  mov     edi, [esi+398h]            ; 对象成员（非线字段）
0xB04B94  lea     eax, [esp+124h+var_28]
0xB04B9C  call    sub_CA0CE0
0xB04BA4  mov     ecx, [esi+8]               ; 对象成员，仅用于打印 " (id:"
0xB04BA7  push    offset aProtoAuthClien_13  ; ")->_proto_auth_client::recv_authenticate_bnpotp_input( "
0xB04BAD  push    offset aId                ; " (id:"
0xB04BBF  call    sub_B03020

; VA: 0xB04BF7 .. 0xB04C1D（打印已消费字节数）
0xB04BF7  push    offset aByte               ; "]byte"
0xB04BFC  sub     ebx, ebp                   ; 已消费字节数 = 游标 - buf（此处 = len）
0xB04BFE  push    ebx
0xB04BFF  push    offset asc_EDAD58          ; " ) ["

; VA: 0xB04C38 .. 0xB04C3F（64 位接收计数自增）
0xB04C38  add     dword ptr [esi+160h], 1
0xB04C3F  adc     dword ptr [esi+164h], 0

; VA: 0xB04C2F .. 0xB04C36（通知上层）
0xB04C2F  mov     edx, [esi]
0xB04C31  mov     eax, [edx+70h]
0xB04C34  mov     ecx, esi
0xB04C36  call    eax                        ; vt[0x70]
```
