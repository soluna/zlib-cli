# zlib-cli 0.1.0

## 中文

`0.1.0` 是首个公开 alpha，提供面向 Agent 的稳定 JSON 调用层，让用户在有或没有
Z-Library 账号时搜索并下载电子书。

主要内容：

- Z-Library 登录、动态域名、搜索、元数据和流式下载。
- Anna's Archive 无账号 HTML 搜索与 best-effort 自动下载。
- `--source all` 单来源失败时自动继续其他来源。
- 稳定 `result_id`、错误码、`schema_version` 和 `cli_version`。
- Anna MD5、下载大小、文件类型、重定向和私网目标安全检查。
- `doctor`、`resolve`、`batch` 以及中英双语开源文档。

安装：

```bash
pipx install git+https://github.com/soluna/zlib-cli.git@v0.1.0
```

已知限制：Anna 依赖不稳定 HTML 与第三方镜像；域名、验证码、网络封锁或页面改版可能导致
失败。Z-Library token 保存在本机明文 JSON 中，并使用 POSIX 文件权限保护。

## English

`0.1.0` is the first public alpha. It provides an agent-friendly JSON layer for searching
and downloading ebooks with or without a Z-Library account.

Highlights:

- Z-Library login, dynamic domains, search, metadata, and streaming downloads.
- Account-free Anna's Archive HTML search and best-effort automatic downloads.
- Source isolation: `--source all` continues when one source fails.
- Stable result IDs, error codes, `schema_version`, and `cli_version`.
- Anna MD5, file-size/type, redirect, and private-network safety checks.
- Doctor, resolve, batch commands, and complete bilingual open-source documentation.

Install:

```bash
pipx install git+https://github.com/soluna/zlib-cli.git@v0.1.0
```

Known limitations: Anna depends on unstable HTML and third-party mirrors; domain changes,
captchas, network blocking, and markup changes can cause failures. Z-Library tokens are
stored as local plaintext JSON protected with POSIX file permissions.
