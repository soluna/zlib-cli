# zlib-cli

## 直接让 Agent 安装 / Ask Your Agent to Install

不建议只说“安装这个仓库”，因为 Skill 注册和 `zlib-cli` 命令安装是两个步骤。请把下面
这句话直接发给具有 GitHub 与终端权限的 Agent：

Do not ask an agent to merely “install this repository”: skill registration and CLI
installation are separate steps. Send this exact request to an agent that has GitHub and
terminal access:

> 请帮我安装这个 Agent Skill 及其 CLI：https://github.com/soluna/zlib-cli 。仓库根目录
> 就是 Skill 目录；请同时安装 `zlib-cli` 命令，并运行 `zlib-cli --version` 和
> `zlib-cli doctor --json` 验证。安装阶段不要要求我的 Z-Library 账号。
>
> Please install both the Agent Skill and CLI from https://github.com/soluna/zlib-cli .
> The repository root is the skill directory. Also install the `zlib-cli` command, then
> verify it with `zlib-cli --version` and `zlib-cli doctor --json`. Do not request my
> Z-Library account during installation.

对于 Codex，Agent 应把仓库根目录作为 `--path .`、Skill 名称作为 `zlib-cli` 安装，然后用
`pipx` 安装同一仓库中的 Python CLI。只复制 `SKILL.md` 或只运行 `pipx install` 都不算完整
安装。完整命令、更新方法和其他 Agent 的边界见 [INSTALL.md](INSTALL.md)。

For Codex, the agent should install the repository root with `--path .` and the name
`zlib-cli`, then use `pipx` to install the Python CLI from the same repository. Copying only
`SKILL.md` or running only `pipx install` is incomplete. See [INSTALL.md](INSTALL.md) for
exact commands, updates, and limitations for other agents.

中文 | English

面向 Agent 的电子书搜索与下载 CLI / Skill，支持 Z-Library 与 Anna's Archive。

An agent-first ebook search and download CLI/Skill for Z-Library and Anna's Archive.

> 中文：项目名中的 `zlib` 指 Z-Library，不是 Python/C 的压缩库。当前版本是
> `0.1.0` alpha。它是非官方社区项目，与 Z-Library、Anna's Archive 均无隶属关系。
>
> English: `zlib` in this project means Z-Library, not the Python/C compression
> library. This is a `0.1.0` alpha and an unofficial community project unaffiliated
> with Z-Library or Anna's Archive.

## 60 秒开始 / Start in 60 Seconds

需要 Python 3.9+。推荐用 `pipx` 隔离安装：

Python 3.9+ is required. `pipx` is recommended for an isolated install:

```bash
pipx install git+https://github.com/soluna/zlib-cli.git

# 无账号搜索 / Search without an account
zlib-cli search "Python Programming" --source anna --json

# 从结果中选择 result_id 后下载 / Download a chosen result_id
zlib-cli download "anna:<32-character-md5>" --output ~/Books --json
```

没有 Z-Library 账号时不需要配置任何凭据。`--source all` 会跳过未登录的
Z-Library，继续使用 Anna's Archive。

No credentials are required when using Anna's Archive. With `--source all`, an
unauthenticated Z-Library source is skipped while Anna's Archive continues.

## 能力边界 / Capabilities

| 能力 / Capability | Z-Library | Anna's Archive |
| --- | --- | --- |
| 搜索 / Search | 需要账号 / Account required | 无需账号 / No account required |
| 自动下载 / Automatic download | 已登录时支持 / Supported after login | Best-effort |
| 格式过滤 / Format filter | 支持 / Supported | 支持 / Supported |
| 年份、语言过滤 / Year, language filters | 服务端 / Server-side | CLI 本地过滤 / CLI-side |
| 排序 / Ordering | 支持 / Supported | 暂不支持，会在状态中标记忽略 / Not supported; reported as ignored |
| 下载校验 / Download verification | 非空与大小限制 / Non-empty and size limit | 非空、大小限制、MD5 / Non-empty, size limit, and MD5 |

Anna 下载依赖 HTML 页面与第三方镜像，验证码、会员页、页面改版、失效镜像或网络封锁
都可能导致失败。搜索结果中的 `can_attempt_download: true` 表示“可以尝试”，不是保证。

Anna downloads depend on HTML pages and third-party mirrors. Captchas, member-only
pages, markup changes, dead mirrors, and network blocks can all cause failure.
`can_attempt_download: true` means “the CLI can try,” not “download is guaranteed.”

## 安装 / Installation

用户工具安装 / User-tool install:

```bash
pipx install git+https://github.com/soluna/zlib-cli.git
```

从源码安装 / Install from source:

```bash
git clone https://github.com/soluna/zlib-cli.git
cd zlib-cli
python3 -m pip install -e .
```

开发安装 / Development install:

```bash
python3 -m pip install -e ".[dev]"
pytest -q
ruff check .
ruff format --check .
python3 -m build
```

## Agent Skill 安装 / Agent Skill Installation

中文：推荐直接使用 README 开头的 Agent 安装指令。手动安装时，Skill 需要完整仓库目录，
同时还要安装 CLI。以 Codex 为例：

English: Prefer the agent-install request at the top of this README. For manual setup, keep
the complete repository as the skill directory and install the CLI as well. For Codex:

```bash
git clone https://github.com/soluna/zlib-cli.git ~/.codex/skills/zlib-cli
pipx install ~/.codex/skills/zlib-cli
zlib-cli --version
zlib-cli doctor --json
```

其他 Agent 框架请把仓库目录安装到其 Skill 搜索路径，并确保 `zlib-cli` 命令在 Agent
进程的 `PATH` 中。仓库包含 [SKILL.md](SKILL.md) 与 `agents/openai.yaml`。

For other agent frameworks, place the repository directory in the framework's skill
search path and make sure `zlib-cli` is available on the agent process `PATH`. The
repository includes [SKILL.md](SKILL.md) and `agents/openai.yaml`.

Agent 的正确流程是：先搜索并展示候选项；只有用户明确要求下载或确认某个结果后才下载。
不要因为用户只说“找一本书”就自动落盘。

The intended agent flow is: search and present candidates first; download only after
the user explicitly asks for a download or confirms a result.

## 快速使用 / Quick Start

```bash
# 环境诊断 / Diagnose environment and source access
zlib-cli doctor --json

# 无账号搜索 / Account-free search
zlib-cli search "Python Programming" --source anna --json

# 搜索所有可用来源 / Search every usable source
zlib-cli search "Clean Code" --source all --ext epub,pdf --lang en --json

# Z-Library 安全登录；密码通过终端提示读取
# Secure Z-Library login; password is read from the terminal prompt
zlib-cli auth login zlib --email you@example.com

# 自动化场景从 stdin 读取密码 / Read password from stdin for automation
printf '%s\n' "$ZLIB_PASSWORD" | zlib-cli auth login zlib \
  --email you@example.com --password-stdin --json

# 下载；默认单文件上限 2048 MiB / Download; default per-file limit is 2048 MiB
zlib-cli download "zlib:1234567:abcdef01" --output ~/Books --json
zlib-cli download "anna:<32-character-md5>" --output ~/Books --json

# 调低大小上限 / Lower the size limit
zlib-cli download "anna:<32-character-md5>" --max-size-mb 200 --json
```

## Agent JSON 协议 / Agent JSON Contract

- 始终把 `--json` 放在子命令参数中 / Always pass `--json` to the subcommand.
- stdout 只输出 JSON，stderr 用于人类提示 / stdout is JSON; stderr is for human logs.
- 每个响应包含 `schema_version` 与 `cli_version` / Every response includes both versions.
- 成功：`{"ok": true, ...}` / Success: `{"ok": true, ...}`.
- 失败：`{"ok": false, "error": {...}}` / Failure: structured `error`.
- 稳定结果 ID / Stable result IDs:
  - `zlib:<book_id>:<hash>`
  - `anna:<32-character-md5>`

错误示例 / Error example:

```json
{
  "ok": false,
  "schema_version": "1",
  "cli_version": "0.1.0",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "Z-Library search requires login.",
    "recoverable": true,
    "suggestions": [
      "Run: zlib-cli auth login zlib --email <you@example.com>"
    ]
  }
}
```

常见错误码包括 `AUTH_REQUIRED`、`AUTH_INVALID`、`SOURCE_UNAVAILABLE`、
`SEARCH_FAILED`、`INVALID_RESULT_ID`、`DOWNLOAD_FAILED`、`OUTPUT_NOT_WRITABLE`
和 `UNEXPECTED_ERROR`。

Common error codes include `AUTH_REQUIRED`, `AUTH_INVALID`, `SOURCE_UNAVAILABLE`,
`SEARCH_FAILED`, `INVALID_RESULT_ID`, `DOWNLOAD_FAILED`, `OUTPUT_NOT_WRITABLE`,
and `UNEXPECTED_ERROR`.

## 域名变化与不可访问 / Domain Changes and Unreachable Sources

Z-Library 域名确实经常变化。CLI 按以下顺序选择域名：已明确信任的环境变量或缓存域名、
固定 HTTPS 入口返回的当前域名、内置 fallback。每个候选都会先用不携带凭据的请求探测，
之后才可能用于认证请求。

Z-Library domains do change frequently. The CLI checks a trusted environment or cached
domain, domains returned by fixed HTTPS entry points, and built-in fallbacks. Every
candidate is probed without credentials before it can be used for authenticated calls.

手工域名覆盖 / Manual domain override:

```bash
ZLIBRARY_DOMAIN=verified.example zlib-cli doctor --json
```

如果手工域名不在内置或入口发现的信任集合中，CLI 默认不会访问它，更不会发送 token。
只有在你通过独立渠道确认域名后，才使用显式 opt-in：

If a manual domain is outside the built-in/discovered trust set, the CLI will not contact
it or send a token by default. Only after independently verifying it, opt in explicitly:

```bash
ZLIBRARY_DOMAIN=verified.example \
ZLIBRARY_ALLOW_UNTRUSTED_DOMAIN=1 \
zlib-cli doctor --json
```

这项 opt-in 会允许凭据发送到该主机，不能由 Agent 自行猜测或从任意搜索结果中获取。
对非信任集合域名的授权不会持久化；后续使用仍需同时提供域名和 opt-in。

This opt-in permits credentials to be sent to that host. An agent must not guess the host
or take it from arbitrary web search results. Trust for a domain outside the normal trust
set is not persisted; later use requires both variables again.

Anna's Archive 使用 `ANNAS_BASE_URL` 手工切换入口。项目不会从搜索引擎自动抓取新域名，
因为假镜像和过期域名可能返回恶意下载链接：

Use `ANNAS_BASE_URL` to switch Anna's Archive explicitly. The project does not scrape
search engines for new domains because fake or expired mirrors can return malicious links:

```bash
ANNAS_BASE_URL=https://verified.example zlib-cli search "query" --source anna --json
```

CLI 默认拒绝搜索与下载流程访问 localhost、私有 IP、链路本地地址以及解析到内网的域名，
并验证每一次重定向。仅本地开发镜像可在明确理解风险后设置
`ZLIB_CLI_ALLOW_PRIVATE_NETWORK=1`。HTTP 镜像还需要
`ZLIB_CLI_ALLOW_INSECURE_HTTP=1`。

The CLI rejects localhost, private IPs, link-local addresses, and hostnames resolving to
private networks during search and download flows, validating every redirect. Local
development mirrors require the explicit `ZLIB_CLI_ALLOW_PRIVATE_NETWORK=1` opt-in; plain
HTTP also requires `ZLIB_CLI_ALLOW_INSECURE_HTTP=1`.

## 认证与本地数据 / Authentication and Local Data

- Z-Library 密码不会保存 / Z-Library passwords are never stored.
- CLI 不提供 `--password` 参数，避免 shell history 和进程列表泄露 / There is no
  `--password` option; use the secure prompt or `--password-stdin`.
- 登录 token 以明文 JSON 保存在本机配置中 / Login tokens are stored as plaintext JSON
  in the local config.
- 默认路径：`~/.config/zlib_cli/config.json` / Default path.
- 支持 `ZLIB_CLI_CONFIG_DIR` 与 `XDG_CONFIG_HOME` / Both overrides are supported.
- POSIX 上目录为 `0700`、文件为 `0600`，旧权限会自动修复 / On POSIX, directory mode
  is `0700` and file mode is `0600`; legacy permissions are repaired.
- Windows 上 `chmod` 不能代替完整 ACL/凭据管理器保护 / On Windows, `chmod` is not a
  substitute for OS ACLs or a credential manager.
- `auth status --json` 不输出 token，只显示掩码邮箱 / Auth status never prints tokens.
- `doctor --json` 用 `~` 缩写用户主目录，降低 issue 日志泄露本地用户名的风险 /
  Doctor abbreviates the home directory to reduce local username exposure in issue logs.

不要提交或粘贴真实账号、token、cookie、配置文件、私人下载 URL 或电子书文件。

Never commit or paste real accounts, tokens, cookies, config files, private download URLs,
or downloaded ebooks.

## 命令 / Commands

```bash
zlib-cli --version
zlib-cli doctor --json
zlib-cli auth status --json
zlib-cli auth login zlib --email you@example.com
zlib-cli auth logout --json
zlib-cli search "query" --source all --json
zlib-cli resolve "anna:<32-character-md5>" --json
zlib-cli download "anna:<32-character-md5>" --output ~/Books --json
zlib-cli batch books.txt --source auto --output ~/Books --json
zlib-cli domains --json
zlib-cli info --json
zlib-cli popular --limit 10 --json
```

批量文件每行放一个 `result_id`，最多 1000 行、1 MiB。Anna 下载文件会与结果 MD5
核对；不匹配的临时文件会删除。下载使用 `.part` 临时文件，不覆盖同名已有文件。

Put one `result_id` on each batch-file line, up to 1,000 entries and 1 MiB. Anna
downloads are checked against the result MD5; mismatched partials are removed. Downloads
use `.part` files and do not overwrite an existing same-name file.

## 环境变量 / Environment Variables

| Name | 中文 | English |
| --- | --- | --- |
| `ANNAS_BASE_URL` | 指定已验证的 Anna 入口 | Use a verified Anna base URL |
| `ZLIBRARY_DOMAIN` / `ZLIB_DOMAIN` | 指定 Z-Library 域名 | Set a Z-Library domain |
| `ZLIBRARY_ALLOW_UNTRUSTED_DOMAIN` | 允许向非信任集合域名发送凭据 | Allow credentials to a domain outside the trust set |
| `ZLIB_CLI_CONFIG_DIR` | 覆盖配置目录 | Override the config directory |
| `XDG_CONFIG_HOME` | XDG 配置根目录 | XDG config root |
| `HTTPS_PROXY` / `ALL_PROXY` | 网络代理 | Network proxy |
| `ZLIB_CLI_ALLOW_PRIVATE_NETWORK` | 允许本地/私网目标，仅供受控开发 | Allow local/private targets for controlled development |
| `ZLIB_CLI_ALLOW_INSECURE_HTTP` | 允许 Anna 使用 HTTP，仅供受控开发 | Allow HTTP for Anna in controlled development |
| `ZLIB_CLI_DEBUG` | 输出未捕获异常 traceback，可能含敏感信息 | Re-raise unexpected errors; traceback may contain sensitive data |

## 开发与验证 / Development and Verification

```bash
python3 -m pip install -e ".[dev]"
pytest -q
ruff check .
ruff format --check .
python3 -m build
pip-audit -r requirements.txt
bandit -q -r zlib_cli.py Zlibrary.py annas_archive.py network_safety.py -ll
git ls-files -z | xargs -0 detect-secrets scan > /tmp/zlib-cli-secrets.json
python -c 'import json; data=json.load(open("/tmp/zlib-cli-secrets.json")); raise SystemExit(bool(data["results"]))'
```

所有自动化测试默认不访问真实 Z-Library/Anna 服务，也不读取维护者账号。

Automated tests do not access live Z-Library/Anna services or read maintainer credentials.

## 项目文档 / Project Documents

- [安装指南 / Installation Guide](INSTALL.md)
- [贡献指南 / Contributing](CONTRIBUTING.md)
- [行为准则 / Code of Conduct](CODE_OF_CONDUCT.md)
- [安全政策 / Security Policy](SECURITY.md)
- [支持 / Support](SUPPORT.md)
- [变更记录 / Changelog](CHANGELOG.md)
- [0.1.0 发布说明 / Release Notes](RELEASE_NOTES.md)
- [路线图 / Roadmap](ROADMAP.md)
- [开源发布手册 / Open-source Release Guide](OPEN_SOURCE_GUIDE.md)
- [第三方声明 / Third-party Notices](THIRD_PARTY_NOTICES.md)

## 归属与许可证 / Attribution and License

`Zlibrary.py` 改编自
[bipinkrish/Zlibrary-API](https://github.com/bipinkrish/Zlibrary-API)（MIT），本项目补充了
动态域名、timeout、流式下载、大小限制和网络目标校验。完整上游声明见
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

`Zlibrary.py` is adapted from
[bipinkrish/Zlibrary-API](https://github.com/bipinkrish/Zlibrary-API) (MIT). This copy
adds dynamic domains, timeouts, streaming downloads, size limits, and network-target
validation. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

本项目采用 MIT License，见 [LICENSE](LICENSE)。

This project is licensed under the MIT License. See [LICENSE](LICENSE).
