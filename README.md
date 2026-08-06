# zlib-skill

## 直接让 Agent 安装 / Ask Your Agent to Install

直接把这一句发给支持安装 GitHub Skill 的 Agent：

Send this one line to an agent that can install GitHub Skills:

> 请帮我安装这个 Agent Skill：https://github.com/soluna/zlib-skill
>
> Please install this Agent Skill: https://github.com/soluna/zlib-skill

这是一个单次安装、自包含的 Agent Skill。执行代码和带哈希的依赖锁都在 Skill 目录内；首次
实际命令会在用户缓存目录创建专用虚拟环境，不修改系统 Python，也不安装全局命令。

This is a single-install, self-contained Agent Skill. Its execution code and hash-locked
dependency set live inside the Skill. The first real command creates a dedicated virtual
environment in the user cache without modifying system Python or installing a global command.

## 功能 / What It Does

面向 Agent 搜索、比较、诊断和下载 Z-Library 与 Anna's Archive 电子书：

Search, compare, diagnose, and download ebooks from Z-Library and Anna's Archive through an
agent-oriented workflow:

- Z-Library 登录、动态域名、搜索、元数据与流式下载 / Z-Library authentication,
  dynamic domains, search, metadata, and streaming downloads.
- Anna's Archive 无账号搜索与 best-effort 下载 / Account-free Anna's Archive search and
  best-effort downloads.
- 稳定 `result_id`、schema 2 JSON、错误码与来源状态 / Stable result IDs, schema 2 JSON,
  error codes, and source status.
- 私网阻止、重定向校验、大小限制、文件类型与 Anna MD5 校验 / Private-network blocking,
  redirect validation, size limits, file-type checks, and Anna MD5 verification.
- 搜索与下载分离；Agent 必须等待明确下载请求或确认 / Search and download remain separate;
  the agent waits for an explicit request or confirmation.

| 能力 / Capability | Z-Library | Anna's Archive |
| --- | --- | --- |
| 无账号搜索 / Search without account | No | Yes |
| 登录后直接下载 / Authenticated direct download | Yes | N/A |
| 自动下载 / Automatic download | Yes | Best-effort |
| 主要不稳定因素 / Main instability | 域名与账号 / Domains and auth | HTML、镜像、验证码 / HTML, mirrors, captchas |

## 安装 / Installation

推荐使用 README 开头的 Agent 指令。Codex 的精确命令如下：

Prefer the agent request at the top of this README. For Codex, the exact command is:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo soluna/zlib-skill \
  --path . \
  --name zlib-skill
```

然后重新开始一轮 Agent 对话，或手工验证已安装目录：

Then start a new agent turn, or manually verify the installed directory:

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/zlib-skill"
python3 "$SKILL_DIR/scripts/run.py" --version
ZLIB_SKILL_CONFIG_DIR=/tmp/zlib-skill-install-check \
  python3 "$SKILL_DIR/scripts/run.py" auth status --json
```

第二条命令会在首次执行时准备运行环境，但不会登录、搜索或下载。需要 Python 3.9+，并且首次
准备依赖时需要访问 Python 包索引。完整安装、更新和迁移说明见 [INSTALL.md](INSTALL.md)。

The second command prepares the runtime on first use but does not log in, search, or download.
Python 3.9+ is required, plus package-index access for the first setup. See
[INSTALL.md](INSTALL.md) for complete installation, update, and migration guidance.

## Agent 工作流 / Agent Workflow

Skill 使用 `{baseDir}` 指代包含 `SKILL.md` 的目录：

The Skill uses `{baseDir}` for the directory containing `SKILL.md`:

```bash
python3 {baseDir}/scripts/run.py search "Python Programming" --source all --json
python3 {baseDir}/scripts/run.py doctor --json
python3 {baseDir}/scripts/run.py download "anna:<32-character-md5>" --output ~/Books --json
```

搜索不会自动触发下载。Anna 的 `can_attempt_download: true` 只表示执行器可以尝试，不保证
镜像、验证码或会员页允许自动获取文件。

Search never triggers a download automatically. Anna's `can_attempt_download: true` means
the runner can try; it does not guarantee that mirrors, captchas, or member pages permit an
automatic file download.

## 无账号与登录 / Account-Free Use and Login

没有 Z-Library 账号或尚未登录时，Agent 默认继续使用 Anna，不会仅为了增加搜索结果而要求
登录：

Without a Z-Library account or login, the agent continues with Anna by default and does not
request a login merely to improve search coverage:

```bash
python3 {baseDir}/scripts/run.py search "query" --source anna --json
```

只有当用户明确选择 Z-Library 搜索或直接下载时，Agent 才会引导用户在自己的终端运行：

Only when the user explicitly chooses Z-Library search or direct download does the agent guide
them to run this in their own terminal:

```bash
python3 {baseDir}/scripts/run.py auth login zlib --email you@example.com
```

密码通过安全提示读取，不提供 argv `--password`。token 以本机明文 JSON 保存；POSIX 上目录
权限为 `0700`、文件为 `0600`。不要把账号、token、cookie、配置、私人下载 URL 或电子书
提交到仓库或 Issue。

The password is read through a secure prompt; there is no argv `--password`. Tokens are stored
as local plaintext JSON with POSIX directory/file modes `0700`/`0600`. Never commit or post
accounts, tokens, cookies, config data, private download URLs, or ebooks.

## 域名变化与网络边界 / Changing Domains and Network Boundaries

Z-Library 地址会变化。执行器按受信任环境变量或缓存、官方入口发现、内置 fallback 的顺序
探测；未知域名默认不会被访问或接收凭据。不要从任意搜索结果猜测登录域名。

Z-Library addresses change. The runner checks trusted environment/cached values, official
entry-point discovery, then built-in fallbacks. Unknown domains are not contacted or sent
credentials by default. Never guess a login domain from arbitrary search results.

```bash
ZLIBRARY_DOMAIN=verified.example \
  python3 {baseDir}/scripts/run.py doctor --json
```

Anna 无法访问时可使用用户独立验证的 `ANNAS_BASE_URL`，或配置 `HTTPS_PROXY` / `ALL_PROXY`。
默认拒绝 localhost、私有 IP、链路本地地址和解析到内网的主机。开发环境 opt-in 见下表。

When Anna is unreachable, use a user-verified `ANNAS_BASE_URL` or configure `HTTPS_PROXY` /
`ALL_PROXY`. Localhost, private/link-local IPs, and private-resolving hosts are blocked by
default. Development opt-ins are listed below.

## 运行环境 / Runtime

- 默认缓存：`~/.cache/zlib-skill/`，Windows 使用 `%LOCALAPPDATA%` / Default cache.
- 缓存键包含 Skill 版本、Python 版本和依赖锁哈希 / Cache keys include Skill version,
  Python version, and dependency-lock hash.
- 依赖以 `--require-hashes --only-binary=:all:` 安装 / Dependencies install with required
  hashes and binary distributions.
- 更新锁文件或 Python 后自动建立新环境 / Lock-file or Python changes create a new runtime.
- stdout 保持 JSON；首次准备日志只写 stderr / Stdout remains JSON; setup logs use stderr.

## 环境变量 / Environment Variables

| Name | 中文 | English |
| --- | --- | --- |
| `ZLIB_SKILL_RUNTIME_DIR` | 覆盖运行缓存根目录 | Override runtime cache root |
| `ZLIB_SKILL_CONFIG_DIR` | 覆盖账号配置目录 | Override account config directory |
| `ANNAS_BASE_URL` | 指定用户验证的 Anna 入口 | Use a user-verified Anna base URL |
| `ZLIBRARY_DOMAIN` / `ZLIB_DOMAIN` | 指定用户验证的 Z-Library 域名 | Set a user-verified Z-Library domain |
| `ZLIBRARY_ALLOW_UNTRUSTED_DOMAIN` | 明确允许未知域名接收凭据 | Allow an unknown domain to receive credentials |
| `HTTPS_PROXY` / `ALL_PROXY` | 网络代理 | Network proxy |
| `ZLIB_SKILL_ALLOW_PRIVATE_NETWORK` | 允许本地/私网目标，仅限受控开发 | Allow local/private targets for controlled development |
| `ZLIB_SKILL_ALLOW_INSECURE_HTTP` | 允许 Anna 使用 HTTP，仅限受控开发 | Allow Anna HTTP for controlled development |
| `ZLIB_SKILL_DEBUG` | 输出 traceback，可能包含敏感数据 | Enable tracebacks that may contain sensitive data |

旧版 `ZLIB_ANNA_*` 与 `ZLIB_CLI_*` 在 `0.x` 期间作为兼容别名保留。

Previous `ZLIB_ANNA_*` and `ZLIB_CLI_*` names remain compatibility aliases during `0.x`.

## 开发与验证 / Development and Verification

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes -r scripts/requirements.lock
python -m pip install -r requirements-dev.txt
pytest -q
ruff check .
ruff format --check .
pip-audit -r scripts/requirements.lock
bandit -q -r scripts/run.py scripts/zlib_anna -ll
```

修改运行依赖后，用固定命令重新生成通用哈希锁：

After changing runtime dependencies, regenerate the universal hash lock with:

```bash
uv pip compile scripts/requirements.in --universal --python-version 3.9 \
  --generate-hashes --output-file scripts/requirements.lock
```

默认测试不访问真实服务，也不读取维护者账号。网络行为使用 mock；公开 URL 安装和实时来源
测试必须显式运行并使用隔离配置。

Default tests do not access live services or maintainer accounts. Network behavior is mocked;
public-URL installation and live-source checks must be explicit and use isolated config.

## 项目文档 / Project Documents

- [安装与迁移 / Installation and Migration](INSTALL.md)
- [贡献指南 / Contributing](CONTRIBUTING.md)
- [安全政策 / Security Policy](SECURITY.md)
- [支持 / Support](SUPPORT.md)
- [变更记录 / Changelog](CHANGELOG.md)
- [发布说明 / Release Notes](RELEASE_NOTES.md)
- [路线图 / Roadmap](ROADMAP.md)
- [开源维护手册 / Open-source Maintenance Guide](OPEN_SOURCE_GUIDE.md)
- [第三方声明 / Third-party Notices](THIRD_PARTY_NOTICES.md)

## 归属与许可证 / Attribution and License

`scripts/zlib_anna/zlibrary.py` 改编自
[bipinkrish/Zlibrary-API](https://github.com/bipinkrish/Zlibrary-API)（MIT）。完整声明见
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。本项目采用 [MIT License](LICENSE)。

`scripts/zlib_anna/zlibrary.py` is adapted from
[bipinkrish/Zlibrary-API](https://github.com/bipinkrish/Zlibrary-API) (MIT). See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). This project uses the [MIT License](LICENSE).
