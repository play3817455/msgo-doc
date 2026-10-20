# AUTOEXEC ｜ `autoexec_sv.cfg`

- **用途**：服务端启动脚本（autoexec_sv.cfg 脚本方言，**不是 CSV**；控制服务端初始化、表加载顺序与调试开关）
- 表ID `0` ｜ 下载序 `0` ｜ disposition `SCRIPT`
- **不是 CSV 数据表**：无列定义；服务端启动时按脚本方言执行（见 `server/autoexec_sv.cfg`）

> 本表无需列定义。脚本控制：表加载、调试开关、服务端初始化流程。

**填写规则**：
- 文件编码 **UTF-8**；`#` 开头为注释行
- 语法为服务端 autoexec 脚本方言（非 CSV 列格式）
