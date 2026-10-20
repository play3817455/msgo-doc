#!/usr/bin/env python3
"""Expand enum_glossary_zh.json global_values from enums_ida.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

ENUMS_IDA = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "enums_ida.json"
GLOSSARY = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "enum_glossary_zh.json"

EXTRA_ZH: dict[str, str] = {
    "GRENADE_LAUNCHER": "榴弹发射器", "FIXED": "固定组合", "CATEGORY_COMBINATION": "类别组合",
    "ID_COMBINATION": "ID 组合", "PERMIT_ID_COMBINATION": "许可 ID 组合",
    "REQUIRED_ID_COMBINATION": "必需 ID 组合", "RANK1": "Rank1", "RANK2": "Rank2",
    "RANK3": "Rank3", "RANK4": "Rank4", "RANK5": "Rank5", "LIMIT_MS_SET": "限制机体集",
    "NEWBIE_LIMIT_MS": "新手限制机体", "NEWBIE_VS_XWAR": "新手大规模战",
    "MS_COST": "机体 COST", "BTLTYPE_ENABLE": "启用战斗类型", "BTLTYPE_DISABLE": "禁用战斗类型",
    "VERSUS": "对战", "VERSUS_XWAR": "大规模对战", "VERSUS_COMMANDER": "指挥官对战",
    "WIN_XWAR": "大规模战胜利", "WIN_COMMANDER": "指挥官战胜利", "KILL_WRESTLE": "格斗击杀",
    "KILL_SHOT": "射击击杀", "KILL_CANNON": "炮击击杀", "KILL_THROW": "投掷击杀",
    "ASSAULT_A": "突击 A", "ASSAULT_B": "突击 B", "EX_STRONGHOLD": "扩展·据点",
    "PLAY_BUNDLE_BC_ONLY": "仅 BC 包播放", "FREE_PLAY_BUNDLE": "免费扭蛋包",
    "SINGLE_NORESET": "单次不重置", "BUILDUP_MSMA": "强化机体",
    "CARPET_BOMB": "地毯轰炸", "MINOVSKY": "米诺夫斯基粒子", "SOLAR_RAY": "太阳能炮",
    "ORATION": "演说", "JAMMING": "干扰", "MISSION_EXP_UP": "任务经验提升",
    "MISSION_GP_UP": "任务 GP 提升", "ALLOY_CHIP_GET": "合金芯片获取",
    "PECULIAR_1": "特殊挂点1", "MODELORIGIN": "模型原点",
    "INVALID": "无效", "TIME_ATTACK": "竞速", "BASE_DEFENSE": "基地防御",
    "COOP_WAVE": "合作波次", "RESPAWN_TIME": "复活时间", "WARP_TIME": "传送时间",
    "BOOST_GAUGEMAX": "BOOST 上限", "BOOST_GAUGEHEAL": "BOOST 回复",
    "VIP_ASSOCIATE": "VIP 准会员", "VIP_MASTER": "VIP 大师", "VIP_DIAMOND": "VIP 钻石",
}


def token_guess(name: str) -> str:
    if name in EXTRA_ZH:
        return EXTRA_ZH[name]
    parts = re.split(r"[_\-/]+", name)
    m = {
        "EX": "EX", "STG": "关卡", "ARMS": "武装", "MS": "机体", "MA": "MA",
        "GP": "GP", "UP": "提升", "CUT": "缩短", "OLD": "旧", "NET": "网",
        "TUMBLE": "滚动", "DUMMY": "诱饵", "BEACON": "信标", "TRANSPORT": "运输",
        "DECKCOST": "卡组 COST", "DISCOUNT": "折扣", "SHOP": "商店", "ROKAKU": "登录平台",
        "DEATH": "死亡", "SPAWN": "生成", "STREAK": "连击", "LOCKON": "锁定",
        "WARP": "传送", "REDUCE": "降低", "HIT": "命中", "MODEL": "模型",
        "GENERATOR": "发电机", "FRAME": "框架", "MANIPULATOR": " manipulator/操纵臂",
        "THRUSTER": "推进器", "STORAGE": "仓库", "DECK": "卡组",
    }
    bits = [m.get(p, p if len(p) <= 3 else p.title()) for p in parts if p]
    return "·".join(bits)


def main() -> None:
    ida = json.loads(ENUMS_IDA.read_text(encoding="utf-8"))
    gloss = json.loads(GLOSSARY.read_text(encoding="utf-8")) if GLOSSARY.is_file() else {}
    gv = gloss.setdefault("global_values", {})
    cv = gloss.setdefault("converters", {})
    gv.update(EXTRA_ZH)

    for conv, meta in ida.get("converters", {}).items():
        cmeta = cv.setdefault(conv, {})
        if meta.get("title_zh"):
            cmeta["title_zh"] = meta["title_zh"]
        if meta.get("desc_zh"):
            cmeta["desc_zh"] = meta["desc_zh"]
        vals = cmeta.setdefault("values", {})
        for v in meta.get("values") or []:
            nm = v.get("name", "")
            if not nm:
                continue
            zh = EXTRA_ZH.get(nm) or gv.get(nm) or v.get("label_zh") or token_guess(nm)
            if nm in EXTRA_ZH:
                zh = EXTRA_ZH[nm]
            if zh and zh != nm:
                gv[nm] = zh
                vals[nm] = zh

    GLOSSARY.write_text(json.dumps(gloss, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"global_values: {len(gv)} entries")


if __name__ == "__main__":
    main()
