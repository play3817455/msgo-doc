#!/usr/bin/env python3
"""Simulate sub_B06D80 wire consumption to verify 244B."""

def u64(): return 8
def u32(): return 4
def u16(): return 2
def u8(): return 1

total = 0
parts = []

def add(name, n):
    global total
    parts.append((name, total, n))
    total += n

add("uniqid", u64())
add("msma_id", u32())
add("crew_msma_id", u32())
add("decal", u32())
add("color", u8())
add("deck_index", u8())
add("cost", u32())
add("is_costover", u8())
add("energy_now", u32())
add("weight_balance", u16())
add("shield_weight", u16())
add("sp_parts", u32())
for n in ("armor_up", "warp_up", "boost_offset", "boost_offset_ns", "over_custom_armor", "over_custom_warp", "over_custom_level"):
    add(n, u16())
add("witem_id[3]", u32() * 3)
add("sitem_id", u32())
add("spitem_id", u32())
for stat in ("power", "stability", "rapid", "shot_range", "shield_hp", "eff_time", "eff_range"):
    add(f"wbu_{stat}[3]", u16() * 3)
add("eq_modules[10]", u32() * 10)
add("eq_bonus_modules", u32())
add("eq_rental_modules", u32())
add("adop_items_ms[4]", u32() * 4)
add("adop_items_eq[12]", u32() * 12)  # reader v29 loop: 3 groups × 4 u32
add("is_exdeck", u8())
add("is_rokaku", u8())
add("rokakums_limit_use", u32())
add("respawn_wait_sec", u16())
add("respawn_wait_max", u16())
add("is_reduce_respawn_wait", u8())
add("is_extrule_invalid", u8())
add("is_heroms", u8())
add("level_gauge_now_level", u32())

print("total", total)
for p in parts:
    print(p)
