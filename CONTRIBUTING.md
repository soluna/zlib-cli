# Contributing / 贡献指南

感谢你改进 `zlib-cli`。当前优先级是稳定的 Agent JSON 协议、可靠的来源降级、安全的凭据
处理、可诊断的失败，以及不访问真实账号的离线测试。

Thanks for improving `zlib-cli`. Current priorities are a stable agent JSON contract,
reliable source fallback, safe credential handling, diagnosable failures, and offline tests
that never access real accounts.

## 开发环境 / Development Setup

```bash
git clone https://github.com/soluna/zlib-cli.git
cd zlib-cli
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

Windows PowerShell 激活命令为 `.venv\Scripts\Activate.ps1`。

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## 提交前检查 / Before a Pull Request

```bash
pytest -q
ruff check .
ruff format --check .
python -m build
pip-audit
detect-secrets scan $(git ls-files)
```

- 新增错误路径时使用稳定错误码和可执行 `suggestions` / Use stable error codes and
  actionable suggestions for new failure paths.
- 修改 JSON 时同时更新测试、README 与 `schema_version` 策略 / Update tests, README,
  and schema-version policy when changing JSON.
- 网络测试默认使用 mock；真实网络 smoke test 必须显式标记且不能进入默认 CI / Mock
  network calls by default; live smoke tests must be explicit and excluded from normal CI.
- 不提交下载文件、`.part`、真实 URL、账号、token、cookie、`.env` 或 `config.json` /
  Never commit downloads, partials, private URLs, accounts, tokens, cookies, `.env`, or
  `config.json`.
- 新增 URL 跟随逻辑时必须覆盖重定向、私网地址和大小限制测试 / URL-following changes
  must test redirects, private targets, and size limits.

## Pull Request 要求 / Pull Request Expectations

PR 应说明用户问题、行为变化、测试证据和兼容性影响。保持改动聚焦；不要把真实服务返回的
完整 HTML、账号数据或下载链接放进 fixture。

Describe the user problem, behavior change, test evidence, and compatibility impact. Keep
changes focused. Do not place complete live-service HTML, account data, or private download
URLs in fixtures.

提交 PR 即表示你的贡献可按本仓库 MIT License 分发，并且你有权提交这些代码。

By submitting a pull request, you agree that your contribution may be distributed under
this repository's MIT License and confirm that you have the right to contribute it.

## 报告问题 / Reporting Issues

普通问题使用 Issue 模板。安全问题遵循 [SECURITY.md](SECURITY.md)，不要公开漏洞细节。

Use the issue templates for normal bugs and features. Follow [SECURITY.md](SECURITY.md) for
security reports and do not disclose vulnerability details publicly.
