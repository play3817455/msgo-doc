# 汇编证据 —— CS-0x421B-battle-pos_move

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B351D0 @ `0x00b351d0`（`0x00b351d0`..`0x00b3597f`）
- 命令名字符串：`)<-_proto_battle_client::send_pos_move(` @ `0xee0b38`
- 声明容量：`0xAA`（分配器指纹 @ `0xB3521F`）

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B35234  call sub_ABB2F0
00B35239  lea eax, [esi+0AAh]
00B3523F  lea ecx, [esi+2]
00B35242  cmp ecx, eax
00B35244  mov [esp+54h+var_4], 0
00B3524C  mov [esp+54h+var_34], esi
00B35250  mov dword ptr [esp+54h+var_30], eax
00B35254  ja loc_B358F4
00B3525A  lea edx, [ecx+4]
00B3525D  cmp edx, eax
00B3525F  mov word ptr [esi], 421Bh
00B35264  ja loc_B358F4
00B3526A  mov esi, [ebp+arg_0]
00B3526D  mov [ecx], esi
00B3526F  lea ecx, [edx+2]
00B35272  cmp ecx, eax
00B35274  ja loc_B358F4
00B3527A  mov ax, word ptr [ebp+arg_4]
00B3527E  mov [esp+54h+var_34], ecx
00B35282  lea ecx, [esp+54h+var_34]
00B35286  mov [edx], ax
00B35289  push ecx
00B3528A  lea edx, [ebp+arg_8]
00B3528D  push edx
00B3528E  call sub_B02DA0
00B35293  add esp, 8
00B35296  test al, al
00B35298  jz loc_B358F4
00B3529E  lea eax, [esp+54h+var_34]
00B352A2  push eax
00B352A3  lea ecx, [ebp+arg_C]
00B352A6  push ecx
00B352A7  call sub_B02DA0
00B352AC  add esp, 8
00B352AF  test al, al
00B352B1  jz loc_B358F4
00B352B7  lea edx, [esp+54h+var_34]
00B352BB  push edx
00B352BC  lea eax, [ebp+arg_10]
00B352BF  push eax
00B352C0  call sub_B02DA0
00B352C5  add esp, 8
00B352C8  test al, al
00B352CA  jz loc_B358F4
00B352D0  lea ecx, [esp+54h+var_34]
00B352D4  push ecx
00B352D5  lea edx, [ebp+arg_14]
00B352D8  push edx
00B352D9  call sub_B02DA0
00B352DE  add esp, 8
00B352E1  test al, al
00B352E3  jz loc_B358F4
00B352E9  lea eax, [esp+54h+var_34]
00B352ED  push eax
00B352EE  lea ecx, [ebp+arg_18]
00B352F1  push ecx
00B352F2  call sub_B02DA0
00B352F7  add esp, 8
00B352FA  test al, al
00B352FC  jz loc_B358F4
00B35302  lea edx, [esp+54h+var_34]
00B35306  push edx
00B35307  lea eax, [ebp+arg_1C]
00B3530A  push eax
00B3530B  call sub_B02DA0
00B35310  add esp, 8
00B35313  test al, al
00B35315  jz loc_B358F4
00B3531B  lea ecx, [esp+54h+var_34]
00B3531F  push ecx
00B35320  lea edx, [ebp+arg_20]
00B35323  push edx
00B35324  call sub_B02DA0
00B35329  add esp, 8
00B3532C  test al, al
00B3532E  jz loc_B358F4
00B35334  lea eax, [esp+54h+var_34]
00B35338  push eax
00B35339  lea ecx, [ebp+arg_24]
00B3533C  push ecx
00B3533D  call sub_B02D80
00B35342  add esp, 8
00B35345  test al, al
00B35347  jz loc_B358F4
00B3534D  lea edx, [esp+54h+var_34]
00B35351  push edx
00B35352  lea eax, [ebp+arg_28]
00B35355  push eax
00B35356  call sub_B02DA0
00B3535B  add esp, 8
00B3535E  test al, al
00B35360  jz loc_B358F4
00B35366  lea ecx, [esp+54h+var_34]
00B3536A  push ecx
00B3536B  lea edx, [ebp+arg_2C]
00B3536E  push edx
00B3536F  call sub_B02DA0
00B35374  add esp, 8
00B35377  test al, al
00B35379  jz loc_B358F4
00B3537F  lea eax, [esp+54h+var_34]
00B35383  push eax
00B35384  lea ecx, [ebp+arg_30]
00B35387  push ecx
00B35388  call sub_B061C0
00B3538D  add esp, 8
00B35390  test al, al
00B35392  jz loc_B358F4
00B35398  lea edx, [esp+54h+var_34]
00B3539C  push edx
00B3539D  lea eax, [ebp+arg_34]
00B353A0  push eax
00B353A1  call sub_B061C0
00B353A6  add esp, 8
00B353A9  test al, al
00B353AB  jz loc_B358F4
00B353B1  lea ecx, [esp+54h+var_34]
00B353B5  push ecx
00B353B6  lea edx, [ebp+arg_38]
00B353B9  push edx
00B353BA  call sub_B02DA0
00B353BF  add esp, 8
00B353C2  test al, al
00B353C4  jz loc_B358F4
00B353CA  lea eax, [esp+54h+var_34]
00B353CE  push eax
00B353CF  lea ecx, [ebp+arg_3C]
00B353D2  push ecx
00B353D3  call sub_B02DA0
00B353D8  add esp, 8
00B353DB  test al, al
00B353DD  jz loc_B358F4
00B353E3  lea edx, [esp+54h+var_34]
00B353E7  push edx
00B353E8  lea eax, [ebp+arg_40]
00B353EB  push eax
00B353EC  call sub_B02DA0
00B353F1  add esp, 8
00B353F4  test al, al
00B353F6  jz loc_B358F4
00B353FC  lea ecx, [esp+54h+var_34]
00B35400  push ecx
00B35401  lea edx, [ebp+arg_44]
00B35404  push edx
00B35405  call sub_B02DA0
00B3540A  add esp, 8
00B3540D  test al, al
00B3540F  jz loc_B358F4
00B35415  lea eax, [esp+54h+var_34]
00B35419  push eax
00B3541A  lea ecx, [ebp+arg_48]
00B3541D  push ecx
00B3541E  call sub_B02DA0
00B35423  add esp, 8
00B35426  test al, al
00B35428  jz loc_B358F4
00B3542E  lea edx, [esp+54h+var_34]
00B35432  push edx
00B35433  lea eax, [ebp+arg_4C]
00B35436  push eax
00B35437  call sub_B02DA0
00B3543C  add esp, 8
00B3543F  test al, al
00B35441  jz loc_B358F4
00B35447  lea ecx, [esp+54h+var_34]
00B3544B  push ecx
00B3544C  lea edx, [ebp+arg_50]
00B3544F  push edx
00B35450  call sub_B061C0
00B35455  add esp, 8
00B35458  test al, al
00B3545A  jz loc_B358F4
00B35460  mov ebx, [ebp+arg_58]
00B35463  cmp ebx, 1
00B35466  ja loc_B358F4
00B3546C  lea eax, [esp+54h+var_34]
00B35470  push eax
00B35471  lea ecx, [ebp+arg_58]
00B35474  push ecx
00B35475  call sub_B02D80
00B3547A  add esp, 8
00B3547D  test al, al
00B3547F  jz loc_B358F4
00B35485  xor esi, esi
00B35487  test ebx, ebx
00B35489  jbe short loc_B354B8
00B3548B  mov edx, [ebp+arg_54]
00B3548E  mov [esp+54h+var_40], edx
00B35492  mov ecx, [esp+54h+var_40]
00B35496  lea eax, [esp+54h+var_34]
00B3549A  push eax
00B3549B  push ecx
00B3549C  call sub_B065D0
00B354A1  add esp, 8
00B354A4  test al, al
00B354A6  jz loc_B358F4
00B354AC  add [esp+54h+var_40], 58h ; 'X'
00B354B1  add esi, 1
00B354B4  cmp esi, ebx
00B354B6  jb short loc_B35492
00B354B8  mov esi, [edi+3D9Ch]
00B354BE  test esi, esi
00B354C0  jz loc_B3591C
00B354C6  lea edx, [esp+54h+var_2C]
00B354CA  push edx
00B354CB  call sub_CA0CE0
00B354D0  add esp, 4
00B354D3  mov ecx, [edi+8]
00B354D6  push offset aProtoBattleCli_204; ")<-_proto_battle_client::send_pos_move("...
00B354DB  push ecx
00B354DC  push offset aId; " (id:"
00B354E1  push eax
00B354E2  push esi
00B354E3  mov byte ptr [esp+68h+var_4], 1
00B354E8  call sub_B03020
00B354ED  add esp, 8
00B354F0  push eax
00B354F1  call sub_41D990
00B354F6  add esp, 8
00B354F9  mov ecx, eax
00B354FB  call sub_ADC810
00B35500  push eax
00B35501  call sub_41D990
00B35506  add esp, 8
00B35509  lea ecx, [esp+54h+var_2C]
00B3550D  mov byte ptr [esp+54h+var_4], 0
```

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B3591C  mov ebx, [esp+54h+var_3C]
00B35920  mov esi, [esp+54h+var_34]
00B35924  mov edx, [edi]
00B35926  mov eax, [edx+58h]
00B35929  sub esi, ebx
00B3592B  push esi
00B3592C  push ebx
00B3592D  mov ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3525F` | u16（2 字节） |
| `frame_count` | `0xB3526D` | u32（4 字节） |
| `pos_x` | `0xB35286` | u16（2 字节） |
| `pos_y` | `0xB3528E` | u16（2 字节） |
| `pos_z` | `0xB352A7` | u16（2 字节） |
| `dir` | `0xB352C0` | u16（2 字节） |
| `dir_eye` | `0xB352D9` | u16（2 字节） |
| `target_x` | `0xB352F2` | u16（2 字节） |
| `target_y` | `0xB3530B` | u16（2 字节） |
| `target_z` | `0xB35324` | u16（2 字节） |
| `spbits` | `0xB3533D` | u32（4 字节） |
| `spbits2` | `0xB35356` | u16（2 字节） |
| `lockon_ent_id` | `0xB3536F` | u16（2 字节） |
| `in_water_index` | `0xB35388` | u8（1 字节） |
| `layer_index` | `0xB353A1` | u8（1 字节） |
| `access_ent_id1` | `0xB353BA` | u16（2 字节） |
| `access_ent_id2` | `0xB353D3` | u16（2 字节） |
| `rideon_ent_id` | `0xB353EC` | u16（2 字节） |
| `spot_ent_id` | `0xB35405` | u16（2 字节） |
| `AI_ent_id` | `0xB3541E` | u16（2 字节） |
| `operate_ent_id` | `0xB35437` | u16（2 字节） |
| `is_under_water` | `0xB35450` | u8（1 字节） |
| `hack_check_count` | `0xB35475` | u32（4 字节） |
| `hack_check` | `0xB3549C` | array<struct,1>（79 字节） |

## E1 `spot_ent_id` 的发送参数边界（正确 v15 IDA，2026-10-11）

`sub_4D4270` 在 `0x4D4EA2` 调用适配器 `sub_B01B90`，后者调用 `sub_B351D0`。按 B01B90 prototype与逐项转发、caller的17次push及serializer offset交叉核对，关联槽对应：`var_240→access_ent_id1`、`var_23C→access_ent_id2`、`var_254→rideon_ent_id`、`var_238→spot_ent_id`。注意 caller stack argument序号与serializer wire field序号不同，不可按两边“第N个”直接等同。

`access_ent_id1` 的候选由 `D72564+0x2CC=sub_4E5C90` 经 `sub_442910` 从全局管理器 `dword_11E3EF8+0xB0` 复制到 `var_278`，再经候选状态、`sub_478C80` 和 vtable `+0x314=sub_4D1B00` 的 `0x800000` mask门控决定是否取 `[candidate+4]` 写入 `var_240`。其中 `+0x2D8=sub_4E23F0` 读取管理器 `+676` mask8，`+0x2E0=sub_4D12D0` 检查 `this+0x1184` 共享对象首DWORD。此链关联交互意图，但不证明具体玩法对象。

真正的 `spot_ent_id` 由 vtable `D72564+0x3C0=sub_4E6CE0` 提供共享指针：当 `sub_475620(controller) < *(float *)(this+0x1254)` 时复制 `[this+0x124C]`，caller在 `0x4D4402-0x4D4414` 对非空候选取 `[candidate+4]` 写入 `var_238`。新增更新链显示候选经 `sub_4B72E0` 构造方向性场景查询（向量乘 200000.0），通过 `sub_4B5250` 过滤；其更新器关联 `CTargetSightWindow` 和 `sound/SE/EVENT/40152020.ogg`。这支持视线/目标提示关联，但不证明敌机锁定、雷达或地图机关语义。比较阈值单位、候选类别和+4字段类型仍未知。access2的var23C来自控制器+0x1188句柄；rideon的var254来自控制器+0x790候选且另有状态门控。来源见 `serverv/docs/data/ida-v15-pos-move-spot-ent-id-source-20261011.json` 与 `serverv/docs/data/ida-v15-spot-sight-query-20261011.json`。
