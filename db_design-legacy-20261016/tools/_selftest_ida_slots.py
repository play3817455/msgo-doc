#!/usr/bin/env python3
"""`ida_extract_memory_slots.parse_decompile_slots` 的夹具自测（不需要 IDA）。

夹具是**真伪代码**（从 IDA 抄下来、只删掉了行尾注释），覆盖 2026-09-24 修的两类漏判：
偏移 0 的裸 `a1`、定长文本槽循环的两种次序；外加 `(_T *)a1 + N` 的步长换算。

    python tools/_selftest_ida_slots.py
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

# 桩掉 idc / ida_hexrays：本工具设计成在 IDA 进程里跑，夹具测试只要解析函数。
_idc = types.ModuleType("idc")
_idc.get_name_ea_simple = lambda _n: 0xFFFFFFFF  # 不提供 get_idb_path ⇒ 不触发批量抽取
_idc.BADADDR = 0xFFFFFFFF
sys.modules["idc"] = _idc
sys.modules["ida_hexrays"] = types.ModuleType("ida_hexrays")

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ida_slots", ROOT / "tools" / "ida_extract_memory_slots.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# ── 夹具 ──────────────────────────────────────────────────────────────────────
MS_SET_WRITER = """
char __cdecl sub_B41B10(int a1, int a2)
{
  v2 = *(_WORD **)a2;
  if ( (unsigned int)(*(_DWORD *)a2 + 8) > *(_DWORD *)(a2 + 4) )
    return 0;
  *(_DWORD *)v2 = *(_DWORD *)a1;
  *((_DWORD *)v2 + 1) = *(_DWORD *)(a1 + 4);
  *(_DWORD *)a2 += 8;
  **(_WORD **)a2 = *(_WORD *)(a1 + 8);
  *(_DWORD *)a2 += 2;
  **(_WORD **)a2 = *(_WORD *)(a1 + 10);
  *(_DWORD *)a2 += 2;
  for ( i = 0; i < 0x2B; ++i )
  {
    *(_BYTE *)(*(_DWORD *)a2)++ = *(_BYTE *)(i + a1 + 12);
  }
  v4 = 0;
  for ( j = (_DWORD *)(a1 + 56); ; j += 2 )
  {
    v6 = *(_DWORD **)a2;
    *v6 = *j;
    if ( (unsigned int)++v4 >= 4 )
    {
      v7 = 0;
      v8 = (_WORD *)(a1 + 88);
      while ( (unsigned int)(*(_DWORD *)a2 + 2) <= *(_DWORD *)(a2 + 4) )
      {
        **(_WORD **)a2 = *v8;
        ++v7;
        ++v8;
        if ( v7 >= 4 )
          return 1;
      }
      return 0;
    }
  }
  return 0;
}
"""

PILOT_READER = """
bool __cdecl sub_B06980(int a1, _DWORD *a2)
{
  if ( (unsigned int)(*a2 + 4) > a2[1] )
    return 0;
  *(_DWORD *)a1 = *(_DWORD *)*a2;
  *a2 += 4;
  for ( i = 0; i < 0x19; ++i )
  {
    *(_BYTE *)(i + a1 + 4) = *(_BYTE *)(*a2)++;
  }
  *(_BYTE *)(a1 + 29) = *(_BYTE *)v3;
  *(_BYTE *)(a1 + 30) = *(_BYTE *)*a2;
  *(_BYTE *)(a1 + 31) = *(_BYTE *)*a2;
  *(_WORD *)(a1 + 32) = *(_WORD *)*a2;
  *(_DWORD *)(a1 + 36) = *(_DWORD *)*a2;
  if ( !sub_B02DF0((_WORD *)(a1 + 40), (int)a2)
    || !sub_B02DF0((_WORD *)(a1 + 42), (int)a2)
    || !sub_B02DF0((_WORD *)(a1 + 44), (int)a2)
    || !sub_B02DD0((_DWORD *)(a1 + 48), (int)a2)
    || !(unsigned __int8)sub_B068B0(a1 + 52, a2)
    || !sub_B02DD0((_DWORD *)(a1 + 76), (int)a2) )
  {
    return 0;
  }
  v5 = 0;
  while ( sub_B06230((_BYTE *)(a1 + v5 + 80), a2) )
  {
    if ( (unsigned int)++v5 >= 0x1F )
    {
      if ( sub_B06230((_BYTE *)(a1 + 111), a2)
        && sub_B06230((_BYTE *)(a1 + 112), a2)
        && sub_B06230((_BYTE *)(a1 + 113), a2)
        && sub_B02DD0((_DWORD *)(a1 + 116), (int)a2) )
      {
        v6 = 0;
        while ( sub_B06230((_BYTE *)(a1 + v6 + 120), a2) )
        {
          if ( (unsigned int)++v6 >= 0x1F )
          {
            return sub_B02DD0((_DWORD *)(a1 + 168), (int)a2) != 0;
          }
        }
      }
      return 0;
    }
  }
  return 0;
}
"""

TOTAL_RESULT_WAVE_READER = """
bool __cdecl sub_B45650(int a1, _BYTE **a2)
{
  *(_BYTE *)a1 = *(*a2)++;
  result = *a2 + 1 <= a2[1]
        && (*(_BYTE *)(a1 + 1) = **a2, ++*a2, *a2 + 1 <= a2[1])
        && (*(_BYTE *)(a1 + 2) = **a2, ++*a2, *a2 + 4 <= a2[1])
        && (*(_DWORD *)(a1 + 4) = *(_DWORD *)*a2, *a2 += 4, (unsigned __int8)sub_B02DD0(a1 + 8, a2))
        && (unsigned __int8)sub_B02DD0(a1 + 12, a2)
        && (unsigned __int8)sub_B02DD0(a1 + 16, a2) != 0;
  return result;
}
"""

DWORD_PTR_READER = """
int __cdecl sub_B00000(_DWORD *a1, int a2)
{
  a1[3] = 7;
  *((_WORD *)a1 + 1) = 9;
  return *(_DWORD *)(a1 + 2);
}
"""

# BATCH_FN 里 `pilot` 实际映射的是这条（sub_B06360），不是上面那条 sub_B06980。
# 差别不是风格：这里的文本槽是**逗号收尾的 helper 实参**（`sub_B061C0(a1 + v5 + 80, a2)`），
# 旧模式只认「数字后紧跟右括号」⇒ 80/120 两条实证槽被判无证据。
PILOT_WRITER_COMMA = """
bool __cdecl sub_B06360(int a1, _DWORD *a2)
{
  *(_DWORD *)*a2 = *(_DWORD *)a1;
  for ( i = 0; i < 0x19; ++i )
  {
    *(_BYTE *)(*a2)++ = *(_BYTE *)(i + a1 + 4);
  }
  *v3 = *(_BYTE *)(a1 + 29);
  *(_BYTE *)*a2 = *(_BYTE *)(a1 + 30);
  *(_BYTE *)*a2 = *(_BYTE *)(a1 + 31);
  *(_WORD *)*a2 = *(_WORD *)(a1 + 32);
  *(_DWORD *)*a2 = *(_DWORD *)(a1 + 36);
  if ( !(unsigned __int8)sub_B02DA0(a1 + 40, a2)
    || !(unsigned __int8)sub_B02DA0(a1 + 42, a2)
    || !(unsigned __int8)sub_B02DA0(a1 + 44, a2)
    || !(unsigned __int8)sub_B02D80(a1 + 48, a2)
    || !sub_B06290(a1 + 52, a2)
    || !(unsigned __int8)sub_B02D80(a1 + 76, a2) )
  {
    return 0;
  }
  v5 = 0;
  while ( (unsigned __int8)sub_B061C0(a1 + v5 + 80, a2) )
  {
    if ( (unsigned int)++v5 >= 0x1F )
    {
      if ( (unsigned __int8)sub_B061C0(a1 + 111, a2)
        && (unsigned __int8)sub_B061C0(a1 + 112, a2)
        && (unsigned __int8)sub_B061C0(a1 + 113, a2)
        && (unsigned __int8)sub_B02D80(a1 + 116, a2) )
      {
        v6 = 0;
        while ( (unsigned __int8)sub_B061C0(a1 + v6 + 120, a2) )
        {
          if ( (unsigned int)++v6 >= 0x1F )
          {
            if ( (unsigned __int8)sub_B02D80(a1 + 152, a2)
              && (unsigned __int8)sub_B02D80(a1 + 156, a2)
              && (unsigned __int8)sub_B02D80(a1 + 160, a2)
              && (unsigned __int8)sub_B02D80(a1 + 164, a2) )
            {
              return (unsigned __int8)sub_B02D80(a1 + 168, a2) != 0;
            }
            return 0;
          }
        }
      }
      return 0;
    }
  }
  return 0;
}
"""

# ── 2026-09-24 第二批：三处「数组/文本槽认不全」的真伪代码 ─────────────────────
# 全都是**审计报 fail 时从 IDA 现查的**，不是凭空写的。

# ① 外层是 if-continue 的步进循环（`v2 += 3; if (v2 < 6)`），上界不在 for 里。
POINTDMG_WRITER = """
char __cdecl sub_B45760(int a1, int a2)
{
  v2 = 0;
  while ( 2 )
  {
    for ( i = 0; i < 3; ++i )
    {
      *(_DWORD *)(a1 + 4 * (v2 + i)) = **(_DWORD **)a2;
      *(_DWORD *)a2 += 4;
    }
    v2 += 3;
    if ( v2 < 6 )
      continue;
    break;
  }
  return 1;
}
"""

# ② 同型但**下标起点非 0**：v4 从 2 起、按 +4 递增到 <0xA。
EXT_SUBRULE_WRITER = """
char __cdecl sub_B456F0(int a1, int a2)
{
  for ( i = 0; i < 2; ++i )
  {
    *(_WORD *)(a1 + 2 * i) = **(_WORD **)a2;
    *(_DWORD *)a2 += 2;
    v3 = *(_WORD **)a2;
  }
  v4 = 2;
  while ( 2 )
  {
    for ( j = 0; j < 4; ++j )
    {
      *(_WORD *)(a1 + 2 * (v4 + j)) = *v3;
      *(_DWORD *)a2 += 2;
      v3 = *(_WORD **)a2;
    }
    v4 += 4;
    if ( v4 < 0xA )
      continue;
    break;
  }
  return 1;
}
"""

# ③ 起点非 0 的整数数组：v29 = 47、按 +4 递增到 <0x3B ⇒ 下标 47..58（字节 188..232）。
MS_ARRAY_WRITER = """
char __cdecl sub_B00010(int a1, int a2)
{
  v29 = 47;
LABEL_61:
  v30 = 0;
  while ( (unsigned int)(v22 + 1) <= a2[1] )
  {
    *(_DWORD *)(a1 + 4 * (v29 + v30)) = *v22;
    *a2 += 4;
    if ( (unsigned int)++v30 >= 4 )
    {
      v29 += 4;
      if ( v29 < 0x3B )
        goto LABEL_61;
      return 1;
    }
  }
  return 0;
}
"""

# ④ 带转型的定长文本槽：`((_BYTE *)a1 + v10 + 204)` ⇒ 字节 204、宽 0x41（不是 204×4）。
CHECK_QUEST_READER = """
bool __cdecl sub_B06C00(_DWORD *a1, _DWORD **a2)
{
  *a1 = *(*a2)++;
  for ( i = 0; i < 0x61; ++i )
  {
    *((_BYTE *)a1 + i + 4) = *(_BYTE *)*a2;
    *a2 = (_DWORD *)((char *)*a2 + 1);
    v3 = *a2;
  }
  a1[26] = *v3;
  a1[31] = *(*a2)++;
  if ( !sub_B02DD0(a1 + 32, (int)a2) )
    return 0;
  return sub_B02DD0(a1 + 33, (int)a2) != 0;
}
"""

XWAR_EXT_RULE_WRITER = """
char __cdecl sub_B08160(_WORD *a1, _DWORD **a2)
{
  *a1 = *(_WORD *)*a2;
  *a2 = (_DWORD *)((char *)*a2 + 2);
  v2 = 0;
  while ( 2 )
  {
    for ( i = 0; i < 0x20; ++i )
    {
      *(_DWORD *)&a1[2 * v2 + 2 + 2 * i] = *(*a2)++;
    }
    v2 += 32;
    if ( v2 < 0x80 )
      continue;
    break;
  }
  return 1;
}
"""

CASES = [
    # (名字, 伪代码, 必须命中的偏移, 说明, 禁止出现的偏移)
    (
        "ms_set 写方 sub_B41B10",
        MS_SET_WRITER,
        {0, 4, 8, 10, 12, 56, 88},
        "12＝定长文本槽 setname（循环变量 i 在前）；0＝uniq_id 的裸 a1",
        set(),
    ),
    (
        "pilot 读方 sub_B06980",
        PILOT_READER,
        {0, 4, 29, 30, 31, 32, 36, 40, 42, 44, 48, 52, 76, 80, 111, 112, 113, 116, 120, 168},
        "80/120＝clan_name/cupteam_name（循环变量 v5/v6 在后）",
        set(),
    ),
    (
        "pilot 写方 sub_B06360（BATCH_FN 实际映射）",
        PILOT_WRITER_COMMA,
        {0, 4, 29, 30, 31, 32, 36, 40, 42, 44, 48, 52, 76, 80, 111, 112, 113, 116, 120, 152, 156, 160, 164, 168},
        "80/120＝clan_name/cupteam_name（helper 实参，数字后是逗号）",
        set(),
    ),
    (
        "total_result_wave 读方 sub_B45650",
        TOTAL_RESULT_WAVE_READER,
        {0, 1, 2, 4, 8, 12, 16},
        "三个 u8 在 0/1/2 —— 旧映射抽的是别的函数，才只剩 4",
        set(),
    ),
    (
        "量了 a1 声明类型的换算式",
        DWORD_PTR_READER,
        {2, 8, 12},
        "_DWORD *a1：a1[3]=12、(_WORD *)a1 + 1=2、(_DWORD *)(a1 + 2)=8",
        {0, 4},
    ),
    (
        "pointdmg 写方 sub_B45760（if-continue 上界）",
        POINTDMG_WRITER,
        {0, 4, 8, 12, 16, 20},
        "上界写在 `if (v2 < 6)` 里 ⇒ 数组摊出 0..20 步长 4（旧实现只剩 4）",
        set(),
    ),
    (
        "ext_subrule 写方 sub_B456F0（下标起点非 0）",
        EXT_SUBRULE_WRITER,
        {0, 2, 4, 6, 8, 10, 12, 14, 16, 18},
        "v4 从 2 起、+4 递增到 <0xA ⇒ 2*(v4+j) 覆盖 4..18",
        set(),
    ),
    (
        "ms 写方数组段（下标起点 47）",
        MS_ARRAY_WRITER,
        set(range(188, 236, 4)),
        "4*(v29+v30)：v29=47 起 +4 到 <0x3B ⇒ adop_items_eq@188 整段 48 字节",
        set(),
    ),
    (
        "check_quest 读方 sub_B06C00（带转型文本槽）",
        CHECK_QUEST_READER,
        {0, 4, 104, 124, 128, 132},
        "`((_BYTE *)a1 + i + 4)` ⇒ 槽起点 4（旧实现漏掉 title@4）",
        set(),
    ),
    (
        "xwar_ext_rule 写方 sub_B08160（和式下标）",
        XWAR_EXT_RULE_WRITER,
        {0} | set(range(4, 516, 4)),
        "`&a1[2 * v2 + 2 + 2 * i]`（_WORD *）⇒ 字节 4..512 步长 4，"
        "覆盖 param@4 / row0@8 / row1@132 / row2@256 / row3@380",
        set(),
    ),
]


def main() -> int:
    bad = 0
    for name, text, want, why, forbid in CASES:
        segs = mod.parse_decompile_slots(text)
        got = set(mod.expand_slots(segs))
        elem = mod.a1_elem_size(text)
        miss = sorted(want - got)
        extra = sorted(forbid & got)
        ok = not miss and not extra
        print(f"[{'OK ' if ok else 'FAIL'}] {name}  a1步长={elem} 槽={sorted(got)}")
        print(f"       {why}")
        for s in segs:
            print(f"         +{s['offset']:<4} {s['kind']:<14} {s.get('cast', '') or ''}{s.get('fn', '') or ''}")
        if miss:
            print(f"       ✗ 缺 {miss}")
        if extra:
            print(f"       ✗ 不该有 {extra}（签名行的 `*a1` 不许当偏移 0）")
        if not ok:
            bad += 1
    print(f"\nRESULT: {len(CASES) - bad}/{len(CASES)} fixtures passed")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
