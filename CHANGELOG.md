# Changelog / 变更记录

本项目遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)；`0.x` 可能包含不兼容
调整。

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Breaking
changes may occur during `0.x`.

## 0.3.0 - 2026-08-06

### Changed / 调整

- 项目、GitHub 仓库和 Skill 标识缩短为 `zlib-skill` / Shortened the project,
  repository, and Skill identifier to `zlib-skill`.
- README 推荐安装请求缩短为一句，详细验证步骤下沉至安装文档 / Reduced the recommended
  install request to one line and moved detailed verification into the installation guide.
- 默认运行缓存迁移到 `~/.cache/zlib-skill`；账号配置路径保持兼容 / Moved the default
  runtime cache while preserving the account-config path.
- 规范环境变量改为 `ZLIB_SKILL_*`，旧名称保留兼容 / Made `ZLIB_SKILL_*` canonical while
  retaining previous aliases.
- 无 Z-Library 登录时继续使用 Anna，仅在用户明确选择 Z-Library 时引导登录 / Continue
  with Anna without login and guide Z-Library login only when explicitly needed.

## 0.2.0 - 2026-08-06

### Added / 新增

- 自包含 `scripts/run.py`，首次使用创建版本化缓存运行环境 / A self-contained runner that
  prepares a versioned cache-local runtime on first use.
- 通用、固定版本并带 SHA-256 哈希的运行依赖锁 / A universal, pinned runtime dependency lock
  with SHA-256 hashes.
- 首次引导失败的脱敏 schema 2 JSON 与缓存复用测试 / Sanitized schema 2 setup failures and
  runtime-cache reuse tests.
- `ZLIB_ANNA_*` 运行、配置、安全和调试环境变量 / Skill-named runtime, config, safety, and
  debug environment variables.

### Changed / 调整

- 项目与 Skill 重命名为 `zlib-anna-skill` / Renamed the project and Skill.
- 执行代码迁移到 `scripts/zlib_anna/`，作为 Skill 私有深模块 / Moved execution code into a
  private bundled module.
- JSON schema 升至 2，`cli_version` 改为 `skill_version` / Raised the JSON schema to 2 and
  replaced `cli_version` with `skill_version`.
- 安装从 Skill + CLI 两步改为单次 Skill 安装 / Replaced two-surface Skill-plus-CLI setup
  with one Skill installation.
- Agent 元数据、双语文档、Issue/PR 模板与 CI 统一为 Skill-first / Updated metadata, docs,
  templates, and CI around the Skill-first product.

### Removed / 移除

- 移除全局 `zlib-cli` console script、`pipx` 要求、wheel/sdist 和 Python 包发布面 / Removed
  the global console command, pipx requirement, wheel/sdist, and standalone package surface.

### Security / 安全

- 运行依赖使用 `--require-hashes --only-binary=:all:` / Runtime dependencies require hashes
  and binary distributions.
- 内部引擎以 Python isolated mode 启动，避免当前目录与 `PYTHONPATH` 注入 / The engine
  starts in isolated mode to avoid current-directory and `PYTHONPATH` injection.

## 0.1.0 - 2026-08-06

### Added / 新增

- 首个公开 alpha：Z-Library 登录、动态域名、搜索与流式下载 / First public alpha with
  Z-Library auth, dynamic domains, search, and streaming downloads.
- Anna 无账号搜索、镜像解析、best-effort 下载和 MD5 校验 / Account-free Anna search,
  mirror resolution, best-effort downloads, and MD5 verification.
- Agent JSON 协议、稳定错误码、`doctor`、`resolve` 与 `batch` / Agent JSON contract,
  stable error codes, doctor, resolve, and batch operations.
- 下载大小、类型、重定向、私网与凭据安全边界 / Download size, type, redirect,
  private-network, and credential boundaries.
- Python 3.9-3.14 CI、依赖审计、Bandit 与 secret scan / Python 3.9-3.14 CI, dependency
  audit, Bandit, and secret scanning.
