# Changelog / 变更记录

本项目遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 的结构；`0.x` 阶段
可能包含不兼容调整。

This project follows the structure of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Breaking changes may occur during `0.x`.

## Unreleased / 未发布

- 暂无 / None.

## 0.1.0 - 2026-08-06

### Added / 新增

- Agent-first JSON 协议：schema/CLI 版本、稳定错误码、结构化来源状态 / Agent-first
  JSON contract with schema/CLI versions, stable error codes, and source status.
- Z-Library 登录、搜索、动态域名、流式下载和无账号 Anna 降级 / Z-Library auth,
  search, dynamic domains, streaming downloads, and account-free Anna fallback.
- Anna HTML 搜索、镜像解析、best-effort 下载与 MD5 校验 / Anna HTML search, mirror
  resolution, best-effort downloads, and MD5 verification.
- `doctor`、`resolve`、`batch`、多格式过滤和可创建下载目录诊断 / Doctor, resolve,
  batch, multi-format filters, and creatable-directory diagnostics.
- 下载大小上限、已知电子书类型检查、私网/重定向安全边界 / Download size limits,
  ebook-type checks, and private-network/redirect protections.
- `ZLIB_CLI_CONFIG_DIR`、XDG、受信任域名与开发 opt-in 配置 / Config-directory/XDG,
  trusted-domain, and development opt-ins.
- Python 3.9-3.14 CI、构建冒烟、依赖审计、secret scan / Python 3.9-3.14 CI,
  package smoke tests, dependency audit, and secret scan.
- 中英双语 README、贡献、安全、行为准则、支持、发布手册和第三方声明 / Bilingual
  README, contribution, security, conduct, support, release, and third-party documents.

### Changed / 调整

- `--source all` 在单个来源失败时继续其他来源 / Multi-source search continues after
  one source fails.
- Anna 能力明确标记为 `can_attempt_download`，不再暗示保证下载 / Anna capability is
  marked best-effort instead of guaranteed.
- 删除不安全的 `--password` 参数，仅保留安全提示与 stdin / Removed the unsafe argv
  password option; secure prompt and stdin remain.
- `doctor` 缩写用户主目录，异常默认返回脱敏 JSON / Doctor abbreviates home paths and
  unexpected exceptions return sanitized JSON.

### Security / 安全

- 未验证 Z-Library 域名默认不会被访问或接收 token / Unverified Z-Library domains are
  not contacted or sent tokens by default.
- Anna 下载验证所有跳转并阻止内网目标 / Anna downloads validate redirects and block
  private-network targets.
- 严格验证 Anna MD5、Z-Library ID/hash 和下载文件名 / Strict result-id and filename
  validation.
