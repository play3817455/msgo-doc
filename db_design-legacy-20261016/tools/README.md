# db_design 工具

## import_from_protocol.py

从 `protocol_analysis/commands/*/fields.csv` 扫描全部字段，生成：

- `schema/fields/index.json` — 扁平字段索引（唯一名、出现次数、命令引用、初稿 disposition）
- 更新 `schema/_meta.json` 统计

```powershell
python db_design/tools/import_from_protocol.py
```

## sync_structs_from_protocol.py

扫描 `protocol_analysis` README 中带 `struct.member` 或 §3.1 成员表的命令，生成：

- `schema/_meta/struct_manifest.json`（struct 清单，供后续批量建表）

```powershell
python db_design/tools/sync_structs_from_protocol.py
```

## build_site.py

从 `schema/` 生成静态 HTML 到 `site/`（烘焙，无需 fetch）：

```powershell
python db_design/tools/build_site.py
python -m http.server 8765 --directory db_design/site
```

生成完会**自检站内死链**（`check_site_links.py`，约 3 秒），有死链就非零退出；
`--no-link-check` 可跳过。死链一律**回生成器修**，不手改 `site/` 里的 HTML。

## check_site_links.py

站点是生成物，模型裁掉一个对象后，别处指向它的 `<a href>` 会静默变成死链（HTML 不报错）。
这个脚本把「谁链了不存在的页」连同**出处**（引用方页面 + 链接文本）列出来：

```powershell
python db_design/tools/check_site_links.py
python db_design/tools/check_site_links.py --exclude '\.json$'   # 只看页面级死链
python db_design/tools/check_site_links.py --quiet               # CI：有死链才输出
```

判据：`href` 去掉 `#fragment`/`?query` 后按**词法**归一化（`a/b.html` 相对引用方目录、
`/x/y.html` 从站点根、`foo/` 等价 `foo/index.html`），归一化后跑到站点外的路径
（`../…`）不算死链——那是刻意的仓库内文件链接（`.go` 源码、
`schema/commands/_verify/*.json` 原始证据切片，见下）。

2026-09 的战绩（930 条 / 922 目标，两个根因都修在生成器侧）：

- **915 条**是命令页的「原始证据切片」把 `schema/commands/_verify/<id>.json` 直接当 href。
  这些件不随站点发布（`_verify` 单目录 1830 个文件 / 113MB），改由 `repo_file_html()`
  解析成**仓库内真实路径**并链到站点外；两种写法（`commands/_verify/…`、
  `schema/commands/_overrides/…`）都按「哪条存在用哪条」解析，对不上就退化成纯 `<code>`
  （同时标注「仓库内路径，未随站点发布」），不留死链。
- **15 条**是页面级：① 名字被归位库收编后协议实体页已裁（`evflag3` / `ms_rokaku` /
  `equip_set` / `ms_set`）——`ref_page_html()` 按「协议实体页优先、其次归位对象页」解析；
  ② CS/SC 配对名与真实命令 id 差一个 `_r` 后缀——`fmt_pair()` 先试原名再试 `_r` 变体，
  落链时把「配对名记作 …」标出来（配对名本身是模型里的数据，这里只做显示侧兜底）。

## derive_homing.py / review_homing.py / _survey_homing.py

字段归位引擎（docs/05「域 → 对象 → 角色」三层模型）。读 `commands` + `composites` +
`entities` + `_legacy_tables`（旧表只作锚点）+ `_meta/legacy_evidence.json`（旧表声明/旧库实况），落：

- `schema/homing/objects/*.json` — 业务对象（含 `tables[]` 落库投影、角色、不落库成员）
- `schema/homing/{relations,roles,fields.jsonl,summary.json,unresolved.md}`

```powershell
python db_design/tools/derive_homing.py            # 重生成（幂等，保留 _overrides.json）
python db_design/tools/review_homing.py --check    # 校验人工裁决是否可解
python db_design/tools/review_homing.py --verify   # 校验引擎输出不变量
python db_design/tools/_survey_homing.py           # 结构守卫：断链/无出处/表名冲突/singleton 证据/发方表面/成员行归根表/孪生裁决/注入行键
```

守卫 14「发方表面」把 `schema/_meta/ida_send_names.txt`（客户端发方全集，IDA 扫 `send_<名>(`
断言串导出）与 `commands/` 的 CS 命令集重比：**必须一一对应**。这条是 docs/05 §9.7「0 个 CS 写方」
这类**否定断言**的地基——只要它恒成立，「发方全集里没有它」就等于「这个实体没有写方」。
任一侧出现差异就说明前提变了（漏了一条写命令，或客户端换了版本），§9.7 的裁决与 `no_writer`
那一桶都要重新过一遍。重导这份全集用 `tools/ida_export_send_names.py`（在 IDA 里跑），
**先 diff 再覆盖，删名字要说明理由**。

守卫 15「成员行归根表」校验 `member_rows_in_root` 的每条声明（成员/对象存在、目标有根表、退役子表
真的不在任何对象的 `tables[]` 里、父对象记了 `view_rows`、理由与 VA 齐备），见下节。

守卫 18「同形孪生逐组裁决」校验 `twin_verdicts`（docs/05 §9.10）：`verdict` 只认 `fold`/`keep`
且必须有 `reason`；`keep` 的组必须**仍在**引擎的孪生清单里；`fold` 的组必须真折进同一个对象、
且在 `fold` 段登记。这一门存在的意思是：`unlinked_layout_twins` 归零必须是因为**每一组都看过**，
而不是因为把没看过的组藏起来了。

守卫 19「注入行键 × `pk` 订正」校验 `inject_members` 里每条 `key: true` 的列**真的在最终主键里**
（docs/05 §9.11.1）：注入是「默认追加」、`pk` 段是「显式全量替换」，两者并存时后者赢——
一句 `"pk": {"x": ["pilot_id"]}` 就能把新注入的行键列静默盖成普通列，而 DDL 仍是合法 SQL、
所有页面仍自洽。批 20 的 `mshipbid_card` 就是这样被盖过一次。

`_survey_homing.py` 还会打印 `summary.json.writers_notes`（`writers` 登记解不开的条目，
见下节「写方点名登记」）——它不阻塞，但要当门看：登记错了等于给「0 CS 写方」这个负断言抹粉。

人工裁决只写 `schema/homing/_overrides.json`（fold / retire / colname / pk / disposition / new_objects …），
重跑引擎不会覆盖它。`disposition` 是**对象级分类订正**（例：自动导入随了 `PERSIST`、
实为战斗 ephemeral 的 `fire_point` 改判 `EVENT`）；判为非 `PERSIST` 的对象不建表，
模型里也不留幻影表（`serverv/tools/verify_no_blob.py` 的「表集合双向一致」门复核）。
`no_writer` 那一桶的收口口径（`DERIVED`/`EVENT`/`CONFIG`/`TBD`）与机师族折叠范围的修正
见 docs/05 §9.9；`TBD` 三件的落地与同形孪生的逐组裁决见 §9.10；
两条 113B 欠账的收口（`mshipbid_card` 行主改判、`friend_histories` 来源订正）见 §9.11。

### 写方点名登记（`writers`）：负断言的补丁

`no_writer` 的判据是「0 个 CS 写命令」。引擎认写方的口径是**命令线体里带了这个复合体**，
所以它只能证明「没有命令带这个复合体」，**证不了**「没有命令在写这份行集」——屏蔽名单
（`CS-0xECDA` / `CS-0x753A`）、好友名单（`CS-0xA30C` / `CS-0xBA4E`）就只带目标机师 id：

```json
"writers": {
  "block_detail": {
    "commands": ["CS-0xECDA-lounge-block_list_add", "CS-0x753A-lounge-block_list_remove"],
    "evidence_va": "0x00EEC138 / 0xeec168",
    "reason": "写方只带目标机师 id，报文里没有 113B 卡片结构，引擎认不出来（0 CS 写方是假阴性）。"
  }
}
```

- 校验（`derive_homing.declared_writers`）：对象存在、每条命令存在且方向确为 CS、`reason` 必填；
  写进对象 `writes`/`reads` 并带 `declared_reason`/`evidence_va`。
- 问题（命令写错、对象不在模型里…）进 `summary.json.writers_notes`，`_survey_homing.py` 打印。
- 用途是**点名**不是**平反**：条目本身必须写清「引擎为什么认不出来」，别拿它绕开批 17 的口径。

### 声明式根对象（`new_objects`）

自底向上推不出「只有引用、没有线体」的实体：`clan` / `cupteam` 在协议里从不作为整体下发，
只有一堆派生投影各带 id，于是 `clan_id` 一族只能判 `dangling`。`_overrides.json.new_objects`
用来声明这类根对象，**只写四件事**（详见 docs/05 §9.5）：

```json
"clan": {
  "title": "氏族（战队）", "domain": "lounge", "composite": "clan",
  "scope": ["world_id"], "writers": ["CS-0xA5BC-lounge-clan_create"],
  "readers": ["SC-0x143D-lounge-clan_create_r"], "reason": "…"
}
```

- `composite` 指向**手写复合体** `schema/composites/<id>.json`（`status=complete`），成员的类型/宽度/
  `meaning`/`wire_sources`（逐列 VA）都在那里 —— **成员不在 `new_objects` 里复述**，避免两处真相。
  `generate_all.py` 对这类手写件**只补缺不覆写**（登记在 `preserve_composites`）。
- `scope` 是**作用域列**：氏族/杯赛队伍跨机师共享，故 `["world_id"]`（默认 `["world_id","pilot_id"]`
  会按机师复制行）。这个值会一路贯通到 DDL 的 PK/唯一索引与 store 的 `ORDER BY`。
- 声明式对象没有单一线宽，DDL 头注释不写 `wire=` 段（别写假的 `0B`）。

新增这类对象后的顺序：手写复合体 → `new_objects` → `derive_homing.py` → `_survey_homing.py`
→ `serverv` 侧 `gen_migration` / `codecgen`（含 `gen_model.py`）→ `build_gm_catalog.py` → `go test ./...`。

### 外部行键注入（`inject_members`）与作用域订正（`scope`）

`clan` / `cupteam` / `party` 这类**跨机师共享**的对象还牵出两件事（详见 docs/05 §9.5/§9.6）：

```json
"inject_members": {
  "party_member.party_id": {
    "wire_type": "u32", "role": "ref", "fk_target": "party.party_id",
    "key": true, "meaning": "所属队伍 ID（外部行键：元素自身不带，身份写在兄弟字段上）",
    "evidence_va": "0xB4542D", "basis": "…不注入这一列，元素表就只剩 scope 行键…同队成员互相覆盖。"
  }
},
"scope": { "party_member": ["world_id"], "party_member_stat": ["world_id"] }
```

- **`inject_members`**：加**线上不存在、但库里必须有的列**（元素表的元素身份落在报文的**兄弟字段**上，
  `SC-0x305D` / `SC-0x76B1` 就是这种）。`wire_type` / `meaning` / `evidence_va` / `basis` 四项引擎**逐项校验非空**；
  `role=ref` + `fk_target` 让它同时是行键与真外键；`key: true` 把它并进 `pk_members`（`pk_kind=injected_key`）。
  注入列在模型里标 `synthetic`，`meaning`/`evidence_va` 会带进 DDL 列注释（生成器对 `synthetic` 列走兜底路径，
  没有这两项 GM 就只能读到「行键/兄弟字段」）。
- **`scope`**：订正对象的作用域列（默认 `["world_id","pilot_id"]`）。只允许 `SCOPE_ORDER` 的子集。
- **`scope` 收窄必须同步查 `pk` 段**：`pk` 订正一旦存在，它会**整体替换** `pk_members`
  （`apply_overrides` 里 `pk_kind=override` 的分支），注入列的 `key: true` 那步追加的值就被盖掉
  ——批 20 的 `mshipbid_card` 就是这样：`scope` 从 `(world_id,pilot_id)` 收窄到 `(world_id)`
  后，行主族换成氏族，`pk` 段必须同时改成 `["mclan_id","pilot_id"]`，否则 `mclan_id` 只当普通列、
  唯一索引仍是「每读方一套列表」。**口径**：`inject_members` 的 `key: true` 是「默认追加」，
  `pk` 段是「显式全量」，两者并存时以后者为准。
- **两个坑**（改这几处代码时别踩回去）：`pk` 订正**不得**把带 `fk_target` 的成员降级成 `identity`
  （`resolve_relations` 只看 `role`，降级 = 外键静默消失）；自键的列名必须**先查 `col_of`**，
  否则被前缀化避让固定列的成员（`party_member_pilot_id`）会当成作用域列本身而丢掉，键退回 `(world_id, party_id)`。

### 成员行归根表（`member_rows_in_root`）

数组元素类型**自己又是根对象**时（`ms_rokaku.weapons` 的元素 `unlockw`），引擎默认会建两张表装同一批行：
`game.<父表>__<成员>`（键 = 父行 + `elem_index`）与元素自己的根表（键 = 元素身份列）。写方只会落到其中一张，
另一张必然漂移。`member_rows_in_root` 声明「行归根表、父记录里那几格只是定长窗口」（详见 docs/05 §9.8）：

```json
"member_rows_in_root": [{
  "parent": "ms_rokaku", "member": "weapons", "object": "unlockw",
  "retire_child_table": "game.ms_rokaku__weapons",
  "writers": ["CS-0x550A-lounge-msma_weapon_unlock"],
  "readers": ["SC-0xA832-lounge-msma_add"],
  "fk": { "member": "uniqid_ms", "target": "ms_rokaku.uniqid", "evidence_va": "0xB70CEC",
          "reason": "…父对象显式指回，子表时代的结构继承不成立" },
  "reason": "…", "evidence_va": "0xB4A580"
}]
```

- 效果：目标对象形状**升为 `root`**；**不建**子表副本，改记 `view_of_root` 链接 + 父对象 `view_rows`；
  `fk` 进 `declared_fks` → `relations[]`。退役的表必须同时登记进 `retire_tables`（否则守卫 15 失败）。
- `plan_objects.py` 把这类成员记进 `TablePlan.view_stored`，与 `not_stored` 分开：
  **不是不落库，是行落在别的表**；`gen_store.py` 的 `TestRowModelRoundTrip` 据此把模型里那个成员整体清空再比对。
- 线体复合体（`composites/ms_rokaku.json` 的 `weapons[3]`）**保留**——线里真有这个成员，只是它不落这张表。

### 同形孪生裁决（`twin_verdicts`）

「逐字节同形」（线长 + 成员名序完全一致）只说明**元素字段**相同，不说明是同一业务对象：
`adop_get`/`adop_list` 行键不同、`clan_eff`/`clan_zeon` 缺侧别列、`bmgpack`/`item_list` 读命令不同。
引擎不擅自合并，但也不该让人每跑一次就重看一遍——**裁决一次、记在这里**（docs/05 §9.10）：

```json
"twin_verdicts": {
  "navi_entry+unlocked_navi": {
    "verdict": "fold", "as": "unlocked_navi",
    "reason": "同一批行：全量列表与单发解锁形，行键同为 (world_id,pilot_id,navi_id)，旧库只建了 unlocked_navi。"
  },
  "clan_eff+clan_zeon": {
    "verdict": "keep",
    "reason": "同一命令下发两军各一份，元素里没有侧别列，折了同 clan 两侧会撞行。"
  }
}
```

- 键 = 该组复合体 id **排序后用 `+` 连接**（与 `derive_homing.twin_key` 同源，别手写别的大小写）。
- `verdict=fold` 的组必须同时出现在 `fold` 段，并把退场的表登记进 `retire_tables`。
- `verdict=keep` 的组必须**仍在**引擎的孪生清单里（否则说明真折了/布局变了，裁决已过期）。
- 已裁决的组不再计入 `summary.json.gates.unlinked_layout_twins`，另记 `twins_reviewed`；
  `unresolved.md` §8 分「未裁决 / 已裁决·不折 / 已裁决·折叠」三张表（站点直接渲染）。
- 校验在守卫 18；改字节模型后若某组不再同形，守卫会报出来——**那是最该看的信号**（不是删掉裁决了事）。

## build_gm_catalog.py

解析迁移的 DDL 头注释（`entity` / `wire` / `多行(行键=…)` / `行键来源` / `slot 行键来源` /
`字段列=` / 子表头）与 `schema/_legacy_tables`、`schema/cfg/tables`，生成 GM 工具的
`serverv/static/gm_catalog.json`。DDL 是唯一真源：改了注释格式（如省略 `wire=`）必须同步改这里的解析。

```powershell
python db_design/tools/build_gm_catalog.py
python db_design/tools/build_gm_catalog.py --check   # 门禁：产物与来源一致 + 现役表都有说明
```

两件容易踩的事：

* **子表有两种头注释形状**：「元素数组 15×11B（x）→ 子表」（数组→子表）与
  「内嵌复合体 avatar（18B）→ 1:1 子表」（定长嵌套→1:1 子表）。只认前者会让后一种子表
  在 catalog 里**整条缺失**（GM 里点得到表、却没有用途说明）。`--check` 会用
  「现役 `game.*` 是否都有说明条目」把这类漏认顶出来（打印为 WARN，`--check` 下算失败）。
* **`retired` 标记**：catalog 是按**旧库表声明**建的，所以退场表会留下「有说明、没有这张表」
  的条目。这些条目带 `retired: true` + `retired_kind`（`folded` / `DERIVED` / `EVENT` /
  `CONFIG` / `TBD` / `never_live`）+ `retired_note`（一句为什么没了），来源按「越具体越优先」：
  `_overrides.json.disposition` → 归位对象的 `no_table_reason` → `retire_tables` → 冻结证据
  `live.exists=false`。没有这一节，读 JSON 的人会把 `game.pcard` 当成现役表。

## freeze_legacy.py

把「写在旧库上」的那部分裁决依据搬进模型：`_legacy_tables/tbl_*.json` 的声明 + 旧库 pg_dump
快照的列清单/唯一键列序/列注释 → `schema/_meta/legacy_evidence.json`（按表干索引，可 diff）。
旧库按「无兼容」口径删掉后，`singleton`/`slot`/`reserved` 这些判据只剩这一份（docs/05 §9.4）。

```powershell
python db_design/tools/freeze_legacy.py            # 重冻结（只增不减：无 dump 时 live 段复用冻结值）
python db_design/tools/freeze_legacy.py --check    # CI：声明侧有没有漂、live 段还在不在
python db_design/tools/reconcile_legacy_ddl.py     # 新自然键 vs 旧 UNIQUE 对账（读冻结证据，不连库）
```

旧表注册表 `schema/relations.json` **已退役**：它只是把 `_legacy_tables/` 的 id/status/purpose
抄一份（还得人工补字段），现由冻结证据统一承载，站点也改读它。

## report_b6.py

非 `PERSIST` 根对象（`EVENT`/`TBD`，共 21 个）的 B6 入口清单 →
`schema/_meta/b6_event_tables.md`：每个对象的域、线长、成员数、CS 写方、SC 读方、
现成身份候选列。战斗持久化（B6）开工时按它逐条定「身份列 + 写入方」。

```powershell
python db_design/tools/report_b6.py           # 重生成清单
python db_design/tools/report_b6.py --check   # CI：清单是否与模型一致
```

## build_homing_site.py

归位库站点的渲染器，由 `build_site.py` 调用（`from build_homing_site import generate_homing_site`），
产出 `site/homing/`：总览、逐列覆盖率、关联、未决清单、127 张对象页。DDL 侧事实直接解析
`serverv/migrations/0003_game_persist.up.sql`，与 homing JSON 对照渲染（漂移一眼可见）。
单独跑它可以只刷归位页：

```powershell
python -c "import sys; sys.path.insert(0,'db_design/tools'); import build_site, build_homing_site as h; print(h.generate_homing_site(build_site.page))"
```

## 典型工作流

1. 跑 import（协议有更新时）
2. 编辑 `schema/entities/*.json`（定 disposition、DB 映射）
3. 跑 build_site（刷新浏览页）
4. 动了字节级模型后：`derive_homing.py` → `review_homing.py --verify` → `_survey_homing.py`
   → `build_site.py` → `serverv` 侧 `gen_migration` / `codecgen`（再跑 `go test ./...` 守门）
5. 动了 `_legacy_tables/`（旧表声明）后：`freeze_legacy.py` → `freeze_legacy.py --check`
6. 动了根系（`scope` / 行键 / `inject_members` / 声明式对象）后：`build_gm_catalog.py` 也要跟（GM 表说明读 DDL 注释）
