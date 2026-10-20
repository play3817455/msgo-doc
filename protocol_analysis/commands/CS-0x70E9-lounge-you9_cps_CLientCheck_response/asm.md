# 汇编证据 —— CS-0x70E9-lounge-you9_cps_CLientCheck_response

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA57D0 @ `0xba57d0`（`0xba57d0`..`0xba5bd6`）
- 命令名字符串：`)<-_proto_lounge_client::send_you9_cps_CLientCheck_response(` @ `0xeed168`
- opcode 写入：`0xba5852`
- 声明容量：`0xA42`（分配器容量 `push` @ `0xba5816`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xba581d  mov     ebp, eax
  0xba581f  mov     eax, [edi+0Ch]
  0xba5822  push    eax
  0xba5823  lea     ecx, [esp+4Ch+var_34]
  0xba5827  call    sub_ABB2F0
  0xba582c  lea     ecx, [ebp+0A42h]
  0xba5832  lea     eax, [ebp+2]
  0xba5835  cmp     eax, ecx
  0xba5837  mov     [esp+48h+var_4], 0
  0xba583f  mov     [esp+48h+var_30], ebp
  0xba5843  mov     dword ptr [esp+48h+var_2C], ecx
  0xba5847  ja      loc_BA5BC1
  0xba584d  lea     edx, [eax+4]
  0xba5850  cmp     edx, ecx
  0xba5852  mov     word ptr [ebp+0], 70E9h
  0xba5858  ja      loc_BA5BC1
  0xba585e  mov     ecx, [esp+48h+arg_0]
  0xba5862  mov     [esp+48h+var_30], edx
  0xba5866  push    61h ; 'a'
  0xba5868  lea     edx, [esp+4Ch+var_30]
  0xba586c  mov     [eax], ecx
  0xba586e  mov     eax, [esp+4Ch+arg_4]
  0xba5872  push    edx
  0xba5873  push    eax
  0xba5874  call    sub_B02B40
  0xba5879  add     esp, 0Ch
  0xba587c  test    al, al
  0xba587e  jz      loc_BA5BC1
  0xba5884  mov     edx, [esp+48h+arg_8]
  0xba5888  push    61h ; 'a'
  0xba588a  lea     ecx, [esp+4Ch+var_30]
  0xba588e  push    ecx
  0xba588f  push    edx
  0xba5890  call    sub_B02B40
  0xba5895  add     esp, 0Ch
  0xba5898  test    al, al
  0xba589a  jz      loc_BA5BC1
  0xba58a0  lea     eax, [esp+48h+var_30]
  0xba58a4  push    eax
  0xba58a5  lea     ecx, [esp+4Ch+arg_C]
  0xba58a9  push    ecx
  0xba58aa  call    sub_B02D80
  0xba58af  add     esp, 8
  0xba58b2  test    al, al
  0xba58b4  jz      loc_BA5BC1
  0xba58ba  mov     eax, [esp+48h+arg_10]
  0xba58be  push    61h ; 'a'
  0xba58c0  lea     edx, [esp+4Ch+var_30]
  0xba58c4  push    edx
  0xba58c5  push    eax
  0xba58c6  call    sub_B02B40
  0xba58cb  add     esp, 0Ch
  0xba58ce  test    al, al
  0xba58d0  jz      loc_BA5BC1
  0xba58d6  mov     edx, [esp+48h+arg_14]
  0xba58da  push    301h
  0xba58df  lea     ecx, [esp+4Ch+var_30]
  0xba58e3  push    ecx
  0xba58e4  push    edx
  0xba58e5  call    sub_B02B40
  0xba58ea  add     esp, 0Ch
  0xba58ed  test    al, al
  0xba58ef  jz      loc_BA5BC1
  0xba58f5  mov     ecx, [esp+48h+arg_18]
  0xba58f9  push    301h
  0xba58fe  lea     eax, [esp+4Ch+var_30]
  0xba5902  push    eax
  0xba5903  push    ecx
  0xba5904  call    sub_B02B40
  0xba5909  add     esp, 0Ch
  0xba590c  test    al, al
  0xba590e  jz      loc_BA5BC1
  0xba5914  mov     eax, [esp+48h+arg_1C]
  0xba5918  push    301h
  0xba591d  lea     edx, [esp+4Ch+var_30]
  0xba5921  push    edx
  0xba5922  push    eax
  0xba5923  call    sub_B02B40
  0xba5928  add     esp, 0Ch
  0xba592b  test    al, al
  0xba592d  jz      loc_BA5BC1
  0xba5933  mov     esi, [edi+822Ch]
  0xba5939  test    esi, esi
  0xba593b  mov     ebx, [esp+48h+var_30]
  0xba593f  jz      loc_BA5B62
  0xba5945  lea     ecx, [esp+48h+var_28]
  0xba5949  push    ecx
  0xba594a  call    sub_CA0CE0
  0xba594f  add     esp, 4
  0xba5952  mov     edx, [edi+8]
  0xba5955  push    offset aProtoLoungeCli_596; ")<-_proto_lounge_client::send_you9_cps_"...
  0xba595a  push    edx
  0xba595b  push    offset aId; " (id:"
  0xba5960  push    eax
  0xba5961  push    esi
  0xba5962  mov     byte ptr [esp+5Ch+var_4], 1
  0xba5967  call    sub_B03020
  0xba596c  add     esp, 8
  0xba596f  push    eax
  0xba5970  call    sub_41D990
  0xba5975  add     esp, 8
  0xba5978  mov     ecx, eax
  0xba597a  call    sub_ADC810
  0xba597f  push    eax
  0xba5980  call    sub_41D990
  0xba5985  add     esp, 8
  0xba5988  lea     ecx, [esp+48h+var_28]
  0xba598c  mov     byte ptr [esp+48h+var_4], 0
  0xba5991  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba59a0  push    offset aCpsResult; "cps_result="
  0xba59c7  push    offset asc_EDAD54; "\""
  0xba59cd  push    offset aCallAddress; "call_address=\""
  0xba59ff  push    offset asc_EDAD54; "\""
  0xba5a05  push    offset aCallerMdBase; "caller_md_base=\""
  0xba5a38  push    offset aCallerMdSize; "caller_md_size="
  0xba5a5f  push    offset asc_EDAD54; "\""
  0xba5a65  push    offset aCallerMdEntry; "caller_md_entry=\""
  0xba5a97  push    offset asc_EDAD54; "\""
  0xba5a9d  push    offset aCallerMdBaseNa; "caller_md_base_name=\""
  0xba5acf  push    offset asc_EDAD54; "\""
  0xba5ad5  push    offset aCallerMdFullNa; "caller_md_full_name=\""
  0xba5b02  push    offset asc_EDAD54; "\""
  0xba5b08  push    offset aDesc; "desc=\""
  0xba5b28  push    offset aByte; "]byte"
  0xba5b32  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xba5b64  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xba5852` | u16 |
| `cps_result` | `0xBA586C` | u32 |
| `call_address` | `0xBA5874` | bytes |
| `caller_md_base` | `0xBA5890` | bytes |
| `caller_md_size` | `0xBA58AA` | u32 |
| `caller_md_entry` | `0xBA58C6` | bytes |
| `caller_md_base_name` | `0xBA58E5` | bytes |
| `caller_md_full_name` | `0xBA5904` | bytes |
| `desc` | `0xBA5923` | bytes |
