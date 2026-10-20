# 汇编证据 —— SC-0x045C-lounge-season_rankerbattle_entry_term

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `4`）

```asm
; VA: 0xB52FA3 .. 0xB52FD9
0xB52FA3  call    sub_B41120               ; ← lounge case 收尾/开关（错误码随后给出）
0xB52FA8  test    al, al
0xB52FAA  jz      loc_B890FE
0xB52FB0  mov     ecx, [esi+0Ch]           ; 传输层对象
0xB52FB3  mov     eax, [ecx]
0xB52FB5  mov     edx, [eax+78h]           ; vt[0x78] = 申请解码缓冲
0xB52FB8  push    4                        ; ← 容量 4（= 负载长）
0xB52FBA  call    edx
0xB52FBC  mov     [esp+2C5Ch+var_2C3C], eax ; 缓冲基址（= 预留游标起点）
0xB52FC0  mov     eax, [esi+0Ch]
0xB52FC3  push    eax
0xB52FC4  lea     ecx, [esp+2C60h+var_26B4]
0xB52FCB  call    sub_ABB2F0               ; 用传输层缓冲初始化 {cur,end} 读游标
```

## E2 唯一字段：`term_sec`（u32）

```asm
; VA: 0xB52FD0 .. 0xB52FF8
0xB52FD0  lea     ecx, [esp+2C5Ch+var_2C3C]
0xB52FD4  push    ecx                      ; arg_0 = &缓冲游标
0xB52FD5  lea     ecx, [esp+2C60h+var_2C48] ; this = &槽
0xB52FD9  mov     [esp+2C60h+var_4], 29Ah
0xB52FE4  call    sub_B41470               ; 缓冲预留 u32（游标 +4，**非字段**）
0xB52FE9  mov     eax, [esp+2C5Ch+var_2C48]
0xB52FED  lea     edx, [esp+2C5Ch+var_2C44] ; 读游标
0xB52FF1  push    edx
0xB52FF2  push    eax
0xB52FF3  call    sub_B02DD0               ; ← 读 u32（term_sec，带「剩余 ≥ 4」边界检查）
```

宽度判定依据（读原语本体）：

```asm
; VA: 0xB02DD0 .. 0xB02DEE
0xB02DD0  mov     eax, [esp+arg_4]
0xB02DD4  mov     ecx, [eax]
0xB02DD6  lea     edx, [ecx+4]             ; ← 需要 4 字节
0xB02DD9  cmp     edx, [eax+4]
0xB02DDC  jbe     short loc_B02DE1
0xB02DDE  xor     al, al
0xB02DE0  retn
0xB02DE1  mov     ecx, [ecx]               ; ← 取 4 字节
0xB02DE3  mov     edx, [esp+arg_0]
0xB02DE7  mov     [edx], ecx
0xB02DE9  add     dword ptr [eax], 4       ; ← 游标 +4
0xB02DEC  mov     al, 1
0xB02DEE  retn
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5301B .. 0xB53023
0xB5301B  mov     ebx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB5301F  cmp     ebx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB53023  jnz     short loc_B53001            ; ← 不等 ⇒ push 256h 报错
```

## E4 含义取证：trace 日志 `term_sec=`

```asm
; VA: 0xB53049 .. 0xB530AD（节选）
0xB5304C  push    offset aProtoLoungeCli_5   ; ")->_proto_lounge_client::recv_season_ra…"
0xB53052  push    offset aId                 ; " (id:"
0xB5309A  mov     ecx, [eax]
0xB5309D  push    offset aTermSec            ; ← "term_sec="
0xB530AD  call    sub_B03580                ; 十进制打印器
```

## E5 去向：`vt[0x5A4]`（单实参）

```asm
; VA: 0xB530E5 .. 0xB53106
0xB530E5  mov     eax, [esp+2C5Ch+var_2C48]   ; 槽地址
0xB530E9  mov     ecx, [eax]                  ; term_sec
0xB530EB  mov     edx, [esi]                  ; 对象虚表
0xB530ED  mov     edx, [edx+5A4h]             ; ← vt[0x5A4]
0xB530F3  push    ecx                         ; 实参 = term_sec
0xB530F4  mov     ecx, esi                    ; this
0xB530F6  call    edx
0xB530F8  add     dword ptr [esi+7578h], 1    ; 本命令接收计数（64 位）
0xB53106  adc     dword ptr [esi+757Ch], 0
```
