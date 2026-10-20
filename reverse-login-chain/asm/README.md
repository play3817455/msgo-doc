# 登录链 · 伪代码 / 汇编 全量导出

> 目的：把「输入账号密码 → 进入游戏大厅」这条链路上**被本项目文档引用过的全部函数**一次性导出成可离线检索的文本，
> 便于人工阅读、diff 与二次分析（**纯静态产物，不依赖联调**）。
>
> 来源：IDA Hex-Rays（IDB `unpacked\GundamOnline_CHINA_v15.exe.i64`，VA 基址 `0x400000`）。

## 一、内容

| 文件 | 内容 |
|---|---|
| `登录链-伪代码-01.md` … `-16.md` | **633 个函数的 Hex-Rays 伪代码**（每批 40 个）；每个函数带 `VA / 大小 / 调用者列表` |
| `登录链-汇编核心-01.md` … `-17.md` | **421 个核心函数的完整汇编**（= `nodes/*.md` 里引用过的函数；每批 25 个，单函数上限 4000 条指令） |
| `_index.json` | 机读索引：每个函数的 `fn / va / size / callers / file / pseudo` ＋ 核心函数列表 |
| `dump_login_chain.py` | **复现脚本**（在 IDA 的 `py_eval` 里整段粘贴执行即可重新生成全部产物） |

> 函数集合的取法：扫描 `reverse-login-chain/nodes/*.md`、`formats/*.md`、`.codebuddy/memory/topics/*.md`
> 里的全部 `sub_XXXXXX` 标记 → 去重 → 只保留 IDA 认可的函数（`get_func_attr(FUNCATTR_START)`）。
> 这样"文档提到过的"与"导出了的"严格一致，**不会漏**；未在文档中出现过的函数不在其中（需要时把地址加进 `_func_refs.json` 再跑一次）。

## 二、从这里开始读（关键入口）

| 环节 | 函数 | 说明 |
|---|---|---|
| 登录 FSM tick | `sub_A88920` | `this+4` = 状态（10~23 / 100~101 / 998~999） |
| 登录提交 | `sub_43E3F0` → `sub_430D00` | state15 提交 / `CGameStateStepUpdateLoginAuth` ctor |
| 建认证连接步骤 | `sub_43E2D0` | state13 → `CGameStateStepUpdateConnectAuth` |
| 帧分发（iVCE） | `sub_C84B60` | type 0~4 |
| 会话建立 | `sub_CA9B40` | createSession；Mode A = 两块 RSA |
| 握手状态机 | `sub_C9E810` / `sub_CA3030` | `会话+0x280`，1..6 |
| 加解密流 | `sub_C882F0` / `sub_C88510`、`sub_CB4580`/`sub_CB4970`/`sub_CB4AD0` | Camellia-128(counter) |
| auth 协议分发器 | `sub_B03D30` | 只认 8 个 ID |
| lounge 协议分发器 | `sub_B51930` | 巨型；`0xFB85`@`0xB87E8F`、`0xF11C`@`0xB864A2`、`0x063E`@`0xB53684`、`0xA5DA`@`0xB70138` |
| 选频道驱动 | `sub_A87E50` | `CGameStateStepUpdateGameModeSelectScene::step` |
| 跳转开关 | `sub_43BC70` | 断 30001 / 存 host+port+otp / 注册 tick |
| 频道登录 tick | `sub_43ADD0` | `app[+1396]` 2..21（进 30002 后的首屏状态机） |
| 数据表装载链 | `sub_576160` / `sub_BBBB70` / `sub_575FF0` | 表分发 → CSV 装载 → 定义名查表（表ID） |
| 逐列读取原语 | `sub_BBB370` / `sub_BBB470` / `sub_BBB3F0` / `sub_456D90` / `sub_BBB4F0` | u32 / float / i64 / str / str→enum |

## 三、复现

1. 打开 IDB（`unpacked\GundamOnline_CHINA_v15.exe.i64`），确认 `ida-pro-mcp` 端点 `127.0.0.1:13338` 可用；
2. 若文档有更新（新增 `sub_XXXXXX` 引用），先重算引用表（与 `formats/extract_table_spec.py` 同目录的做法）：
   扫描文档 → `_func_refs.json`；
3. 把 `dump_login_chain.py` 整段粘进 IDA 的 Python 控制台执行（或经 MCP 的 `py_eval`）。

> ⚠️ 单文件体积较大（合计约 2.3 MB），**不要整篇读进对话**；按 `_index.json` 查到函数名 → 再打开对应文件的具体小节。
