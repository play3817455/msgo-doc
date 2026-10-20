# MODULE ｜ `module/module.csv`

- **用途**：模块（固有模块）定义
- 表ID `50` ｜ 下载序 `50` ｜ 类名 `CModuleTable` ｜ 全局 `dword_11EB5A0`
- 逐列读取函数 `sub_5A2DB0` ｜ **列数 8**（★2026-10-05 n3 批次订正；旧文档写 7）

> ★★ **本表尾段曾整体错位 1 格**，见文末「订正节」。下表是按 `disasm` 的 push 常量**重列**的权威映射。

| 读序 | push 常量（CSV 字段号） | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `module_id` | u32 | `+0` | 主键；模块 ID（`0x5a2dc7`） |
| 2 | `2` | `linked_item_id` | u32 | `+20` | 关联 ITEM 行（`0x5a2dd1`） |
| 3 | `3` | `slot_index` | u32 | `+4` | 槽位序号（循环第 1 次，`0x5a2deb`） |
| 4 | `4` | `param_a` | u32 | `+8` | 参数 A（循环第 2 次，`0x5a2deb`） |
| 5 | `5` | `param_b` | u32 | `+16` | 参数 B（`0x5a2e00`） |
| 6 | **`7`** | `param_c` | u32 | **`+12`** | **被 `sub_61D3A0` 求和的列**（`0x5a2e0d`） |
| 7 | **`8`** | `module_category` | enum `sub_5A2CC0` | **`+24`** | 模块类别（`0x5a2e31`，**读的是原串**） |
| 8 | **`9`** | `unlock_level` | u32 | **`+28`** | 解锁等级（`0x5a2e3b`） |

- 客户端**跳过**的字段：`1`、`6`（不读；填什么都无害）。越界列 = 0。
- `sub_5A2CC0` 的枚举表（`off_D7EC0C`/`dword_D7EC10`）：
  `ATTACK 0 / DEFENSE 1 / MOVE 2 / SPECIAL 3 / AID 4 / FIXED 5`，`UNKNOWN(-1)` 为终止项；
  **名字对不上返回 `-1`**（不是 0）。

**行格式**（写到字段 9，保留尾逗号）：
`<module_id>,<?>,<linked_item_id>,<slot_index>,<param_a>,<param_b>,<?>,<param_c>,<CATEGORY>,<unlock_level>,`

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。

---

## 订正节（2026-10-05，n3 批次）

### 1. 病：文档把尾段三列整体写早了一格

旧文档（本文件旧版 + `07-模块与能量攻关.md` §4.1）给出两套**互不相同**且都与 ASM 不符的列号：

| 来源 | 声称的读列 |
|---|---|
| 本文件旧版 | `0,2,3,4,5,7,8`（并把 `7`=category、`8`=unlock） |
| `07-` §4.1 | `0,2,3,4,6,7,8`（把 `7` 写成 enum、`8` 写成普通参数） |
| **ASM 实测** | **`0,2,3,4,5,7,8,9`** |

⇒ 正确读法是 **8 个字段**：`+12` 那一列（字段 7）在两张文档里**都丢了**。

### 2. 证据

**(a) `sub_5A2DB0` 逐条 push 常量**（`0x5a2db0`–`0x5a2e4a`）：

```asm
push 0  ; +0
push 2  ; [ebx+14h] = +20
loop×2: push 3 → [ebx+4]  ; push 4 → [ebx+8]
push 5  ; [ebx+10h] = +16
add esi,2 → push 7 → mov [ebx+0Ch], eax          ; ★ +12 ← 字段 7
add esi,1 → sub_BBB4F0(dst, tbl, 8) → sub_5A2CC0 → mov [ebx+18h], eax   ; ★ +24 ← 字段 8（枚举名）
add esi,1 → push 9 → mov [ebx+1Ch], eax          ; ★ +28 ← 字段 9
```

辅助函数（本轮一并取证）：`sub_BBB370(tbl,n)` = 第 n 字段 **atoi**；
`sub_BBB4F0(dst,tbl,n)` = 第 n 字段**原串**（越界 ⇒ 空串）；`sub_5A2CC0(str)` = 枚举名→整数（未命中 `-1`）。

**(b) 消费者交叉验证 `sub_61D3A0`**（8 个调用点，如 `0x802aa8`）对最多 10 + 1 个已装模块：

```c
if ( *(_DWORD *)(row_data + 24) != 5 || a2 )   // +24 与 5(=FIXED) 比较 ⇒ +24 = module_category
    v13 += *(_DWORD *)(row_data + 12);         // +12 被求和 ⇒ 字段 7 确实被消费
```

调用点 `0x802aaf lea edx, [ebp+eax*4+0C0h]` ⇒ 这个"和"被当**下标**用（`+0xC0` = 武器组数组）。

### 3. 后果（订正前）

种子/manifest/库都是 `<id>,,1,1,1,,1,ATTACK,1,`（`ATTACK` 落在字段 **7**）⇒ 客户端实际读到：

| 列 | 实际 | 应为 |
|---|---|---|
| `module_category`(`+24`) | `sub_5A2CC0("1")` = **-1（无效）** | `ATTACK`/`DEFENSE`/`MOVE` |
| `+12`（字段 7） | `atoi("ATTACK")` = `0` | 未知 |
| `unlock_level`(`+28`) | 字段 9 = 空 ⇒ `0` | `1` |

### 4. 处置（**已执行并落库**，2026-10-06 复核）

按 `16-` §12.2(d)：字段 7 前插一列，尾部后移 ⇒ 行变
`<id>,,1,1,1,,1,,ATTACK,1,`；同步改 `cfg_schema.json`（`column_count` 7→8、
`module_category.csv_index` 7→8、`unlock_level.csv_index` 8→9、新增 `param_c.csv_index=7`）+ 复跑 `cfgsync`。

| 检查（`_b8x_moduledb.py`，只读可复跑） | 结果 |
|---|---|
| schema 宽度 / GM `cfg_schema.json` `MODULE.column_count` | **10 / 10** ✓（`param_c`→`csv_index 7`、`module_category`→`8`、`unlock_level`→`9`） |
| 种子 CSV（`module/module.csv`）8 行 | 行形 `4011301,,1,1,1,,1,,ATTACK,1,` ⇒ `module_category` 落在字段 **8** ✓ |
| 库 / manifest 逐格 vs 种子（8 行 × 10 字段） | **差异 0** ✓（`cfg."MODULE"` 8 行 = `meta.cfg_manifest.raw_csv`） |
| 客户端实读 | `sub_5A2CC0("ATTACK") = 0`（不再是 `-1`）；`+12` = 字段 7、`unlock_level`(=`+28`) = 1 ✓ |

> 即：`16-` §12.2(d) 的「字段 7 前插一列」**已落库**，三类载体（schema / 种子 / 库+manifest）一致。
> 遗留只剩**取值层**：`param_c`、`linked_item_id`、`param_a/b` 的值仍是批量占位 `1`（无来源，按铁律不猜）。
