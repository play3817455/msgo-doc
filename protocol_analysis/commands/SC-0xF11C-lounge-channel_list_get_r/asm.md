# 汇编证据 —— SC-0xF11C-lounge-channel_list_get_r

> 地址口径：完整 VA（ImageBase `0x400000`，无重定位），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x784` @ `0xB864BB`）

```asm
; VA: 0xB864BB（分配器指纹 `mov <reg>,[X+78h]` + `push IMM; call <reg>`）
0xB864BB  push    0x784          ; 容量（缓冲上限，非线长）
```

## E2 字段读取序列（按线序）

```asm
; 字段 1 —— list_num：线类型 u32，线长 4
0xB864EB  call sub_B02DD0          ; 读点（u32）

; 字段 2 —— list_chnl：线类型 array<channel,32>，元素线长 54、条数 = list_num（变长）
0xB86514  cmp ebx, 20h ; ' '       ; list_num 上限 32（>32 走错误出口 0xB864F7）
0xB86523  call sub_B41230          ; 按槽预留（槽步进 0x3C=60，容量记账，不是线长）
0xB8652A  test ebx, ebx            ; ebx = list_num
0xB8652C  jbe loc_B86567           ; list_num <= 0 ⇒ 不进循环
0xB86536  mov eax, [esp+..var_2C3C] ; 槽基址（循环 loc_B86536）
0xB86540  call sub_B420E0          ; 元素读取器（消费 54B）
0xB86548  test al, al
0xB8654A  jz loc_B8655A            ; 读失败 ⇒ 错误出口
0xB8654C  add [esp+..var_2C3C], 3Ch ; 槽步进 60
0xB86551  add edi, 1               ; i++
0xB86554  cmp edi, ebx             ; i < list_num
0xB86556  jb loc_B86536            ; ⇒ 循环次数 = list_num（不是固定 32）
0xB865F8  push offset alist_chnl   ; 日志格式串锚点 "list_chnl={"

```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB8656B
0xB86567  mov ecx, [esp+..var_2C44]  ; 游标
0xB8656B  cmp ecx, [esp+..var_2C40]  ; cmp <游标>, <报文末尾>
0xB86571  jz loc_B8658A              ; 相等走成功分支
```

## E4 去向（用途锚点）

```asm
; VA: 0xB866A8
; mov edx, [client]
; mov edx, [edx+70h]
; call edx          ; vt[0x70]（2 实参）
```
