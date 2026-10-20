"""Rule-based Chinese labels for cfg enum symbol names."""

from __future__ import annotations

import json
import re
from pathlib import Path

MANUAL_PATH = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "enum_manual_zh.json"


def load_manual_zh() -> dict[str, str]:
    if not MANUAL_PATH.is_file():
        return {}
    data = json.loads(MANUAL_PATH.read_text(encoding="utf-8"))
    return dict(data.get("values") or {})


MANUAL_ZH: dict[str, str] = load_manual_zh()

# 整词优先（MANUAL_ZH 覆盖同键）
EXACT: dict[str, str] = {
    "0": "占位/无",
    "CN_LOCAL": "中国区货币",
    "CP_EX": "CP(EX)",
    "MAIN": "主武装",
    "EX": "EX武装",
    "SUB": "副武装",
    "SUB1": "副武装1",
    "UNKNOWN": "未知/不限",
    "NEAR": "近距",
    "MIDDLE": "中距",
    "FAR": "远距",
    "SHIELD": "护盾",
    "NEUTRAL": "中立",
    "EFF": "地球联邦",
    "ZEON": "吉翁",
    "NORMAL": "普通",
    "HIDDEN": "隐藏",
    "NONE": "无",
    "ALL": "全区",
    "JAPAN": "日本区",
    "CHINA": "中国区",
    "YES": "是",
    "NO": "否",
    "INVALID": "无效",
    "OTHER": "其他",
    "MS": "机体",
    "WEAPON": "武器",
    "ARMOR": "装甲",
    "ITEM": "道具",
    "MSMA": "机体",
    "ATTACK": "攻击",
    "DEFENSE": "防御",
    "MOVE": "移动",
    "SPECIAL": "特殊",
    "SUPPORT": "支援",
    "CANNON": "炮击",
    "SNIPE": "狙击",
    "WRESTLE": "格斗",
    "SOLID": "实弹",
    "BEAM": "光束",
    "BLAST": "爆炸",
    "DEAD": "即死",
    "BRONZE": "铜",
    "SILVER": "银",
    "GOLD": "金",
    "PLATINUM": "白金",
    "FIXED": "固定组合",
    "RANK1": "Rank1",
    "RANK2": "Rank2",
    "RANK3": "Rank3",
    "RANK4": "Rank4",
    "RANK5": "Rank5",
    "ONEHAND": "单手",
    "TWOHAND": "双手",
    "SHOLDER": "肩扛",
    "UNDERWATER": "水中",
    "AMPHIBIAN": "水陆两用",
    "AIRCRAFT": "飞行器",
    "DEBRIS": "残骸",
    "SNIPER": "狙击",
    "GATLINGGUN": "加特林",
    "MINOVSKYCRAFT": "米诺夫斯基飞行器",
    "BROADWAYONLY": "仅Broadway",
    "LANDLUBBERLY": "旱鸭子/陆地",
    "L_HAND": "左手",
    "R_HAND": "右手",
    "ACTIVE_WEAPON": "主动武装",
    "HACK_CHECK_EX": "Hack判定EX武装",
    "SACRIFICE": "牺牲/自爆",
    "CLOSE": "近战/CLOSE",
    "AAA": "AAA级",
    "COOP_WAVE_ALT": "合作波次(备用)",
    "COOP_CORE_DESTROY": "合作·核心破坏",
    "AREA_AIRCRAFT": "区域飞机",
    "AA_AIRCRAFT": "对空飞机",
    "BATTLEAREA": "战区",
    "HEADQUARTERS": "司令部",
    "CONQUEST": "征服模式",
    "DOT_DMG": "持续伤害",
    "RPOST_DIFF": "复活点难度",
    "PLAY_BUNDLE_BC_ONLY": "仅BC包播放",
    "FREE_PLAY_BUNDLE": "免费扭蛋包",
    "SINGLE_NORESET": "单次不重置",
    "SINGLE": "单次",
    "BUILDUP_MSMA": "强化机体",
    "GRENADE_LAUNCHER": "榴弹发射器",
    "KILL_DEPARMS": "击杀·破坏武装",
    "KILL_ASSIST": "击杀·助攻",
    "SCORE_ATK": "分数·攻击",
    "SCORE_SPT": "分数·支援",
    "SCORE_CON": "分数·控制",
    "SCORE_TOTAL": "分数·总计",
    "RESULT_GOLD": "结算·金",
    "RESULT_GOLD_RANK": "结算·金·排名",
    "RESULT_GOLD_SCORE": "结算·金·分数",
    "RESULT_GOLD_DSS": "结算·金·DSS",
    "RESULT_GOLD_CONQUER": "结算·金·征服",
    "RESULT_SILVER_RANK": "结算·银·排名",
    "RESULT_SILVER_SCORE": "结算·银·分数",
    "RESULT_BRONZE_RANK": "结算·铜·排名",
    "RESULT_BRONZE_SCORE": "结算·铜·分数",
    "RESULT_BLUE_RANK": "结算·蓝·排名",
    "RESULT_BLUE_SCORE": "结算·蓝·分数",
    "MOVE_LEN": "移动·距离",
    "RESPAWN_DEFEAT": "复活·败北",
    "RESPAWN_CONQUER": "复活·征服",
    "DMG_STGHOLD": "伤害·据点",
    "DMG_BTLSHIP": "伤害·战舰",
    "DMG_TENDER": "伤害·补给舰",
    "DMG_ACE": "伤害·ACE",
    "MAPOBJ_KILL": "地图对象·击杀",
    "BATTERY_KILL": "炮台·击杀",
    "STGARMS_SET": "关卡武装·设置",
    "STGARMS_LEN": "关卡武装·长度",
    "ORDER_COMP_PL": "命令·完成PL",
    "BADGE_GET": "徽章·获得",
    "MISSION_CLEAR": "任务·Clear",
    "VERSUS": "对战",
    "VERSUS_XWAR": "大规模对战",
    "VERSUS_COMMANDER": "指挥官对战",
    "WIN_XWAR": "大规模战胜利",
    "WIN_COMMANDER": "指挥官战胜利",
    "TIME_ATTACK": "竞速",
    "TIME_ATTACK_ALT": "竞速(备用)",
    "BASE_DEFENSE": "基地防御",
    "COOP_WAVE": "合作波次",
    "COOP_WAVE_ALT": "合作波次(备用)",
    "COOP_CORE_DESTROY": "合作·核心破坏",
    "VS_DOMINATION": "对战·支配",
    "VS_CORE_DESTROY": "对战·核心破坏",
    "VS_DEMOLITION": "对战·爆破",
    "VS_HEADQUARTERS": "对战·司令部",
    "VS_MARCH": "对战·行军",
    "AREA_AIRCRAFT": "区域飞机",
    "AA_AIRCRAFT": "对空飞机",
    "MISSION_EXP_UP": "任务·经验提升",
    "MISSION_GP_UP": "任务·GP提升",
    "MISSION_RITEM_UP": "任务·稀有道具提升",
    "MISSION_RARE_POP": "任务·稀有弹出",
    "RESPAWN_TIME_CUT": "复活时间缩短",
    "MSMA_PARAM_UP": "机体参数提升",
    "ALLOY_CHIP_GET": "合金芯片获得",
    "BUILDUP_UP": "强化提升",
    "LIMITEDTIME_AVATAR": "限时·头像",
    "LIMITEDTIME_MS_COLOR": "限时·机体配色",
    "LIMITEDTIME_MS_EMBLEM": "限时·机体徽章",
    "DAMAGE_FIELD": "伤害场",
    "SEARCH_GRENADE": "搜索手雷",
    "ANTI_AIR_BOMB": "对空炸弹",
    "ANTI_STEALTH_RADAR": "反隐雷达",
    "REFLECT_OBJ": "反射对象",
    "SHOT_MINE": "射击地雷",
    "BADSTATUS": "异常状态",
    "SENSOR_MINE": "感应地雷",
    "PERFECT": "Perfect/完美",
    "STGARMS1": "关卡武装1",
    "STGARMS2": "关卡武装2",
    "LUCKY_DX": "幸运DX",
    **{f"MECHANIC_LV{i}": f"机械师等级{i}" for i in range(12)},
    "DAILY_RECORD_CNT": "每日记录·计数",
    "NETCAFE_CHALLENGE_CNT": "网咖挑战·计数",
    "FORCE_SUCCESS": "强制·成功",
    "FORCE_GREATEST": "强制·最大",
    "BUILDUPWEAPON": "强化武器",
    "BUILDUPWEAPON_FGREATEST": "强化武器·最大失败",
    **{f"SHOP_LV{i}": f"商店等级{i}" for i in range(22)},
    **{f"ROKAKU_LV{i}": f"登录平台等级{i}" for i in range(6)},
    **{f"DECKCOST_LV{i}": f"卡组COST等级{i}" for i in range(6)},
    **{f"DISCOUNT_LV{i}": f"折扣等级{i}" for i in range(11)},
    "MACHINEGUN": "机枪",
    "MACHINEGUN2": "机枪2",
    "MACHINEGUN3": "机枪3",
    "SUBMACHINEGUN": "冲锋枪",
    "SHOTGUN": "霰弹枪",
    "BAZOOKA": "火箭筒",
    "HOWITZER": "榴弹炮",
    "MISSILE": "导弹",
    "BEAM_RIFLE": "光束步枪",
    "BEAM_SPRAYGUN": "光束散射枪",
    "CHARGE_RIFLE": "蓄力步枪",
    "CHARGE_BAZOOKA": "蓄力火箭筒",
    "SNIPER_RIFLE": "狙击步枪",
    "BEAM_SNIPE": "光束狙击",
    "TRENCH_MORTAR": "迫击炮",
    "LANDMINE": "地雷",
    "HAND_THROW": "手投",
    "HAND_THROW2": "手投2",
    "REPAIR": "修理",
    "RADARPOD": "雷达荚舱",
    "REPAIRPOD": "修理荚舱",
    "CAMERAGUN": "摄像枪",
    "BULLET_PACK": "弹药包",
    "AAGPOD": "防空炮荚舱",
    "AAG_POD": "防空炮荚舱",
    "REPAIR_PACK": "修理包",
    "CATEGORY_COMBINATION": "类别组合",
    "ID_COMBINATION": "ID组合",
    "PERMIT_ID_COMBINATION": "许可ID组合",
    "REQUIRED_ID_COMBINATION": "必需ID组合",
    "MSMA_STORAGE": "机体仓库",
    "MSMA_DECKCOST": "卡组COST上限",
    "LIMIT_MS_SET": "限制机体集",
    "NEWBIE_LIMIT_MS": "新手限制机体",
    "NEWBIE_VS_XWAR": "新手大规模战",
    "MS_COST": "机体COST",
    "BTLTYPE_ENABLE": "启用战斗类型",
    "BTLTYPE_DISABLE": "禁用战斗类型",
    "PECULIAR_1": "特殊挂点1",
    "PECULIAR_2": "特殊挂点2",
    "PECULIAR_3": "特殊挂点3",
    "MODELORIGIN": "模型原点",
    "TRAINING": "训练",
    "CLASS": "阶级",
    "SCORE": "分数",
    "COMMUNITY": "社区",
    "RESPAWNPOST": "复活点",
    "REPAIRPOST": "修理站",
    "STRONGHOLD": "据点",
    "ITEMBOX": "道具箱",
    "DOOR": "门",
    "LIFT": "升降机",
    "CONTROLLER": "控制器",
    "MASUMMON": "MS召唤点",
    "CARRY": "运输",
    "GUNTURRET": "炮塔",
    "SUBFLIGHT": "子飞行点",
    "MARCH": "行军",
    "AAG": "防空炮",
    "TENDER": "补给舰",
    "SEARCH": "搜索",
    "BOMB": "轰炸",
    "JAMMING": "干扰",
    "MINOVSKY": "米诺夫斯基粒子",
    "SOLAR_RAY": "太阳能炮",
    "ORATION": "演说",
    "WALL": "墙体",
    "TRANSPORT_SHIP": "运输舰",
    "ASSAULT_SHIP": "突击舰",
    "BATTLE_SHIP": "战舰",
    "PATROL_AIRCRAFT": "巡逻机",
    "CARPET_BOMB": "地毯轰炸",
    "DUMMY_BEACON": "诱饵信标",
    "GRENADE_NET": "捕网榴弹",
    "GRENADE_TUMBLE": "滚雷",
    "GENERATOR": "发电机",
    "FRAME": "框架",
    "MANIPULATOR": "操纵臂",
    "SENSOR": "传感器",
    "THRUSTER": "推进器",
    "VIP_ASSOCIATE": "VIP准会员",
    "VIP_SILVER": "VIP银",
    "VIP_GOLD": "VIP金",
    "VIP_PLATINUM": "VIP白金",
    "VIP_DIAMOND": "VIP钻石",
    "VIP_MASTER": "VIP大师",
    **MANUAL_ZH,
}


def exact_zh(name: str) -> str | None:
    if name in MANUAL_ZH:
        return MANUAL_ZH[name]
    if name in EXACT:
        return EXACT[name]
    return None


# 前缀 → 中文类别（长前缀优先）
PREFIX: list[tuple[str, str]] = [
    ("WEAPON_SLOT_ALL_", "武器槽·全"),
    ("WEAPON_SLOT_", "武器槽·"),
    ("WEAPON_", "武器·"),
    ("MS_EXAM", "机体·考试"),
    ("MS_TRANS", "机体·变形"),
    ("MS_HADES", "机体·Hades"),
    ("MS_ARMOR_PER", "机体·装甲%"),
    ("MS_ARMOR_NOW", "机体·当前装甲"),
    ("MS_ARMOR", "机体·装甲"),
    ("MS_BOOST_GAUGE_RECOV", "机体·BOOST回复"),
    ("MS_BOOST_GAUGE", "机体·BOOST槽"),
    ("MS_BOOST_SPEED", "机体·BOOST速度"),
    ("MS_BOOST_RECOVER", "机体·BOOST恢复"),
    ("MS_PAYLOAD", "机体·载荷"),
    ("MS_WARP", "机体·传送"),
    ("MS_DEF_", "机体·抗"),
    ("MS_", "机体·"),
    ("KILL_", "击杀·"),
    ("SCORE_", "分数·"),
    ("RESULT_", "结算·"),
    ("DMG_", "伤害·"),
    ("RESPAWN_", "复活·"),
    ("STGARMS_", "关卡武装·"),
    ("MISSION_", "任务·"),
    ("LIMITEDTIME_", "限时·"),
    ("VS_", "对战·"),
    ("EX_", "扩展·"),
    ("EQPARTS_EXEC_", "装备执行·"),
    ("USER_", "玩家·"),
    ("COMB_", "组合·"),
    ("DECKCOST_", "卡组COST·"),
    ("DISCOUNT_", "折扣·"),
    ("SHOP_", "商店·"),
    ("ROKAKU_", "登录平台·"),
    ("BOOST_", "BOOST·"),
    ("WARP_", "传送·"),
    ("ENERGY", "EN"),
    ("ORDER_", "命令·"),
    ("MAPOBJ_", "地图对象·"),
    ("BATTERY_", "炮台·"),
]

TOKEN: dict[str, str] = {
    "UP": "提升", "CUT": "缩短", "POP": "弹出", "RITEM": "稀有道具",
    "RARE": "稀有", "PARAM": "参数", "BUILDUP": "强化", "AVATAR": "头像",
    "EMBLEM": "徽章", "COLOR": "配色", "ASSIST": "助攻", "DEPARMS": "破坏武装",
    "WRESTLE": "格斗", "SHOT": "射击", "THROW": "投掷", "CANNON": "炮击",
    "ATK": "攻击", "SPT": "支援", "CON": "控制", "TOTAL": "总计",
    "ASSAULT": "突击", "SNIPE": "狙击", "SUPPORT": "支援", "GOLD": "金",
    "SILVER": "银", "BRONZE": "铜", "BLUE": "蓝", "RANK": "排名",
    "DSS": "DSS", "CONQUER": "征服", "DEFEAT": "败北", "LEN": "长度",
    "SET": "设置", "COMP": "完成", "PL": "PL", "BADGE": "徽章",
    "GET": "获得", "DESTROY": "摧毁", "PROTECT": "保护", "CONTAINER": "容器",
    "TENDER": "补给舰", "BTLSHIP": "战舰", "ACE": "ACE", "STGHOLD": "据点",
    "RESURRECT": "复活", "FIELD": "场", "MINE": "地雷", "PACK": "包",
    "DUMMY": "诱饵", "BALLOON": "气球", "SENTRYGUN": "哨戒炮",
    "REFLECT": "反射", "OBJ": "对象", "ANTI": "反", "STEALTH": "隐形",
    "RADAR": "雷达", "ARTILLERY": "炮击", "STATUS": "状态", "BAD": "异常",
    "SEARCH": "搜索", "GRENADE": "手雷", "REPAIR": "修理", "SENSOR": "感应",
    "SHOT": "射击", "DOMINATION": "支配", "CORE": "核心", "DEMOLITION": "爆破",
    "HEADQUARTERS": "司令部", "MARCH": "行军", "DIFF": "难度",
    "ENABLE": "启用", "DISABLE": "禁用", "COST": "COST", "BTLTYPE": "战斗类型",
    "LIMIT": "限制", "NEWBIE": "新手", "XWAR": "大规模战", "STORAGE": "仓库",
    "DECKCOST": "卡组COST", "WAVE": "波次", "COOP": "合作",
    "TIME": "时间", "ATTACK": "攻击", "BASE": "基地", "DEFENSE": "防御",
    "ALT": "备用", "AREA": "区域", "AA": "对空", "AIRCRAFT": "飞机",
    "LAND": "陆地", "WATER": "水中", "SPACE": "宇宙", "GROUND": "地面",
    "LANDINGPOINT": "着陆点", "LEADER": "领队", "GUARDIAN": "守护者",
    "BARRIER": "屏障", "REFLECTOR": "反射器", "BIT": "比特",
    "RIDEABLE": "可搭乘", "MOVABLE": "可移动", "FLOOR": "地板",
    "BREAKABLE": "可破坏", "DEBRIS": "残骸", "AIRFERRY": "空中渡运",
    "DEPLOY": "部署", "ARMS": "武装", "BEACON": "信标", "POD": "荚舱",
    "FUNNEL": "浮游炮", "RESURRECT": "复活", "BAKUDOSAKU": "爆击",
    "GLAUNCHER": "榴弹发射", "LAUNCHER": "发射器", "MORTAR": "迫击炮",
    "HAND": "手", "CHECK": "判定", "HACK": "Hack", "EXEC": "执行",
    "OLD": "旧", "SUMMON": "召唤", "STG": "关卡", "HOLD": "据点",
    "NET": "网", "TUMBLE": "滚", "JAMMING": "干扰", "TRANSPORT": "运输",
    "SHIP": "舰", "BATTLE": "战斗", "ASSAULT": "突击", "PATROL": "巡逻",
    "DUMMY": "诱饵", "GUIDE": "引导", "QUICK": "快速", "DEFENSE": "防卫",
    "INDOOR": "室内", "BROKEN": "破损", "BATTLEAREA": "战区", "POINT": "点",
    "ANYTIME": "随时", "SPAWN": "生成", "DEATH": "死亡", "REMAIN": "剩余",
    "STREAK": "连击", "LOCKON": "锁定", "READYTIME": "准备时间",
    "KEYACTION": "按键动作", "RATE": "比率", "REDUCE": "降低", "HIT": "命中",
    "MODEL": "模型", "INITIAL": "初始", "STYLE": "风格", "CHANGE": "变更",
    "ON": "开启", "OFF": "关闭", "RELEASE": "释放", "WARP": "传送",
    "TAKEOVER": "继承", "LEVEL": "等级", "GAUGE": "槽", "UK": "UK",
    "PER": "百分比", "NOW": "当前", "RECOV": "回复", "RECOVER": "恢复",
    "PAYLOAD": "载荷", "SPEED": "速度", "DEF": "防御", "SOLID": "实弹",
    "PERMIT": "许可", "REQUIRED": "必需", "CATEGORY": "类别", "COMBINATION": "组合",
    "FIXED": "固定", "ID": "ID", "FUNNEL": "浮游炮", "RESURRECT": "复活",
    "SENTRYGUN": "哨戒炮", "CAMERAGUN": "摄像枪", "RADAR": "雷达",
    "SHIELD": "盾", "SUBFLIGHT": "子飞行", "SVCTRL": "服务器控制",
    "MOVEATK": "移动攻击", "BA": "BA", "PLAY": "播放", "BUNDLE": "包",
    "BC": "BC", "ONLY": "仅", "FREE": "免费", "NORMAL": "普通",
    "NORESET": "不重置", "VERSUS": "对战", "COMMANDER": "指挥官",
    "WIN": "胜利", "KILL": "击杀", "MOVE": "移动", "ORDER": "命令",
}


def _translate_tail(tail: str) -> str:
    if not tail:
        return ""
    if tail in EXACT:
        return EXACT[tail]
    parts = [p for p in tail.split("_") if p]
    out = []
    for p in parts:
        if p in EXACT:
            out.append(EXACT[p])
        elif p in TOKEN:
            out.append(TOKEN[p])
        elif p.isdigit():
            out.append(p)
        else:
            out.append(p.title() if len(p) <= 4 else p)
    return "".join(out) if all(len(x) <= 2 for x in out) else "·".join(out)


def translate(name: str) -> str:
    if not name:
        return name
    hit = exact_zh(name)
    if hit:
        return hit
    if name.endswith("_CNT"):
        return translate(name[:-4]) + "·计数"
    for pref, zh in PREFIX:
        if name.startswith(pref):
            tail = name[len(pref):]
            t = _translate_tail(tail)
            if pref.endswith("_"):
                return f"{zh}{t}" if t else zh.rstrip("·")
            return f"{zh}{t}"
    return _translate_tail(name)


def is_rough(zh: str, name: str) -> bool:
    if not zh or zh == name:
        return True
    # 人工订案：SYMBOL（中文）— 保留缩写对照
    if name in MANUAL_ZH and zh == MANUAL_ZH[name]:
        return False
    if zh.startswith(name) and "（" in zh and zh.endswith("）"):
        return False
    hit = exact_zh(name)
    if hit and zh == hit:
        return False
    if zh in ("是", "否"):
        return False
    # 整词未译（如 CLOSE、UNDERWATER）
    if zh.isascii() and zh.upper() == name.upper():
        return True
    # 英文 token 拼接未译（GRENADE·LAUNCHER）
    if "·" in zh:
        parts = [p for p in re.split(r"[·\s]+", zh) if p]
        if parts and all(p.isascii() and p.upper() in name.upper() for p in parts):
            return True
    # 大段英文残留
    ascii_runs = re.findall(r"[A-Za-z]{5,}", zh)
    allowed = {"BOOST", "ROOKAKU", "DECKCOST", "BROADWAY", "HADES", "DUMMY"}
    if any(r not in allowed and r.upper() not in name.upper() for r in ascii_runs):
        return True
    return False
