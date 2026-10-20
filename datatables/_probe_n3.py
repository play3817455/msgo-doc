# -*- coding: utf-8 -*-
"""n3 批次（发育/成长近亲）交叉取证探针。
1) 键域合法性：MECHANIC_MSMA.col0 / MODULE.module_id / OVER_CUSTOM* 键是否落在上游键域内
2) 常量列取证：MECHANIC_MSMA col1..col12 是否全 = 10
"""
import sys
import psycopg

sys.stdout.reconfigure(encoding="utf-8")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"


def keys(cur, table, col):
    try:
        cur.execute(f'select btrim({col}::text) from cfg."{table}"')
        return [r[0] for r in cur.fetchall()]
    except Exception as e:
        print(f"  ! 读 {table}.{col} 失败: {str(e).splitlines()[0]}")
        return []


def cols_of(cur, table):
    cur.execute(f'select * from cfg."{table}" limit 0')
    return [d.name for d in cur.description]


def bodies(cur, table):
    """返回 (列名, 去掉 _row_id 后的行)"""
    cur.execute(f'select * from cfg."{table}" order by _row_id')
    cs = [d.name for d in cur.description]
    rows = [r for r in cur.fetchall()]
    return cs, rows


def main():
    with psycopg.connect(DSN, autocommit=True) as c:
        cur = c.cursor()

        # ---- 上游键域 ----
        print("CHARA_PARAM 列:", cols_of(cur, "CHARA_PARAM"))
        print("MSMA_MODULE 列:", cols_of(cur, "MSMA_MODULE"))
        cpk = None
        for cand in ("chara_id", "unit_id", "param_id", "col0", "id"):
            if cand in cols_of(cur, "CHARA_PARAM"):
                cpk = cand
                break
        cp = set(keys(cur, "CHARA_PARAM", cpk)) if cpk else set()
        print(f"CHARA_PARAM 键列={cpk} 键域={len(cp)}")

        # ---- #20 MECHANIC_MSMA ----
        print("\n=== #20 MECHANIC_MSMA ===")
        cs, rows = bodies(cur, "MECHANIC_MSMA")
        print("列:", cs)
        for r in rows:
            print("  行:", r)
        for r in rows:
            k = str(r[1]).strip()
            print(f"  键 col0={k!r}: 在 CHARA_PARAM({cpk}) 中 = {k in cp}")
        if rows:
            trans = list(zip(*[r[2:] for r in rows]))
            consts = [(cs[i + 2], set(t)) for i, t in enumerate(trans)]
            print(f"  col1..col12 常量列 {sum(1 for _, s in consts if len(s)==1)}/{len(consts)}: " +
                  ",".join(f"{n}={list(s)[0]}" for n, s in consts))

        # ---- #50 MODULE ----
        print("\n=== #50 MODULE ===")
        cs, rows = bodies(cur, "MODULE")
        print("列:", cs)
        for r in rows:
            print("  行:", r)
        cur.execute('select module_category, count(*) from cfg."MODULE" group by 1 order by 1')
        print("  module_category 分布:", cur.fetchall())
        # module_id 是否落在練度ID 域
        mid = [str(r[1]).strip() for r in rows]
        hit = [m for m in mid if m in cp]
        print(f"  module_id 命中 CHARA_PARAM 的: {len(hit)}/{len(mid)} {hit[:3]}")

        # ---- 其它四表键域抽样 ----
        for t, col in [("MSMA_FAVMS", "fav_id"), ("MECHANIC_SUCCESS", "odds_key"),
                       ("OVER_CUSTOM", "custom_id"), ("OVER_CUSTOM_DEVELOP", "recipe_id")]:
            ks = keys(cur, t, col)
            print(f"\n=== {t}.{col} === n={len(ks)} 唯一={len(set(ks))} 样本={sorted(set(ks))[:12]}")

        # ---- MECHANIC_MSMA 键溯源 ----
        print("\n=== 1124102 上游溯源 ===")
        for t, col in [("CHARA_PARAM", cpk), ("MSMA_MODULE", "col0"),
                       ("MECHANIC_WEAPON", "col0"), ("BUILDUP_WEAPON", "col0"),
                       ("MSMA_MODULE", "module_id")]:
            if not col:
                continue
            ks = set(keys(cur, t, col))
            if ks:
                print(f"  {t}.{col}: {'命中' if '1124102' in ks else '未命中'} (n={len(ks)})")


if __name__ == "__main__":
    main()
