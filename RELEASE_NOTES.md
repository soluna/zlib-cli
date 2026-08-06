# zlib-anna-skill 0.2.0

## 中文

`0.2.0` 将项目从“Skill + 独立 CLI”重构为单次安装的自包含 Agent Skill，并统一更名为
`zlib-anna-skill`。

主要变化：

- 用户只安装 GitHub Skill，不再安装 `pipx` 或全局命令。
- 运行代码放入 `scripts/zlib_anna/`，由 `scripts/run.py` 启动。
- 首次命令在用户缓存创建专用虚拟环境；依赖固定版本并校验 SHA-256。
- Skill、Python 和依赖锁变化时自动使用新缓存，不修改系统 Python。
- JSON schema 升至 2，版本字段改为 `skill_version`。
- 新增 `ZLIB_ANNA_*` 环境变量；旧 `ZLIB_CLI_*` 在 `0.x` 期间保留兼容。
- 保留 Z-Library、Anna、下载、安全、域名和无账号降级能力。

这是不兼容升级。旧 `zlib-cli` 用户应按 [INSTALL.md](INSTALL.md) 迁移，并删除旧 `pipx`
环境。安装与无账号验证不会登录、搜索或下载。

## English

`0.2.0` changes the project from a separate Skill-plus-CLI setup into a single-install,
self-contained Agent Skill named `zlib-anna-skill`.

Highlights:

- Install one GitHub Skill; no pipx or global command is required.
- Bundled execution code lives under `scripts/zlib_anna/` and starts through `scripts/run.py`.
- First use creates a cache-local virtual environment with pinned, SHA-256-checked dependencies.
- Skill, Python, or lock changes select a new cache without modifying system Python.
- JSON schema 2 replaces `cli_version` with `skill_version`.
- New `ZLIB_ANNA_*` settings are canonical; legacy `ZLIB_CLI_*` aliases remain during `0.x`.
- Z-Library, Anna, download, safety, domain, and account-free fallback behavior remain.

This is a breaking upgrade. Existing `zlib-cli` users should follow [INSTALL.md](INSTALL.md)
and remove the old pipx environment. Installation and account-free verification do not log in,
search, or download.
