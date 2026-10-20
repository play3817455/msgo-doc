#!/usr/bin/env python3
import json
from pathlib import Path

BATCH4 = [
    "MISSION_VS", "MISSION_COOP", "MISSION_GROUP", "MISSION_SAFETY_AREA", "MISSION_EXTRULE",
    "MISSION_XWAR_BANPICK", "COMMANDER_NPC", "COMMANDER_SUPPORT", "COMBAT_OPERATION",
    "AI_PARAM", "AI_WEAPON_PARAM", "GACHA", "BYWORD", "QUEST", "BUFF", "DAILY_RECORD",
    "CLAN_CHALLENGE", "TROOP_CHALLENGE", "NETCAFE_CHALLENGE", "CHALLENGE_HIGHSCORE",
    "PLAY_BONUS_REWARD", "BANNER_INFO", "BEGINNER_CHALLENGE", "MONTHLY_BONUS_REWARD",
    "FORCEGAUGE_INFO", "ACTION_MODULE_INFO", "PLAYER_NAVI",
    "SEASON_CLASS_IMFORMATION", "SEASON_CLASS_UP_REWARD", "SEASON_RANKERBATTLE_REWARD",
    "TREND_DATA_WEAPON", "SCORE_CONFIG_CATEGORY", "BGMPACKAGE", "AUTOEXEC",
]
d = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "tables"
complete = partial = pending = 0
tc = tp = tn = 0
for t in BATCH4:
    data = json.loads((d / f"{t}.json").read_text(encoding="utf-8"))
    st = data.get("asm_status", "?")
    c = data.get("column_confirmed", 0)
    pt = data.get("column_partial", 0)
    pn = data.get("column_pending", 0)
    tc += c
    tp += pt
    tn += pn
    if st == "complete":
        complete += 1
    elif st == "partial":
        partial += 1
    else:
        pending += 1
    print(f"{t:30} asm={st:8} conf={c:3} part={pt:3} pend={pn:3} reader={data.get('asm_reader')}")
print("---")
print(f"tables={len(BATCH4)} complete={complete} partial={partial} pending={pending}")
print(f"columns confirmed={tc} partial={tp} pending={tn}")
