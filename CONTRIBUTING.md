# Contributing / 贡献指南

感谢你改进 `zlib-anna-skill`。当前优先级是可靠的单次 Skill 安装、稳定 JSON 协议、安全
凭据处理、来源降级、可诊断失败，以及不访问真实账号的离线测试。

Thanks for improving `zlib-anna-skill`. Priorities are reliable single-step Skill installation,
a stable JSON contract, safe credential handling, source fallback, diagnosable failures, and
offline tests that never access real accounts.

## 开发环境 / Development Setup

```bash
git clone https://github.com/soluna/zlib-anna-skill.git
cd zlib-anna-skill
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r scripts/requirements.lock -r requirements-dev.txt
```

Windows PowerShell 激活命令为 `.venv\Scripts\Activate.ps1`。

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## 提交前检查 / Before a Pull Request

```bash
pytest -q
ruff check .
ruff format --check .
pip-audit -r scripts/requirements.lock
bandit -q -r scripts/run.py scripts/zlib_anna -ll
git ls-files -z | xargs -0 detect-secrets scan
```

- 从可观察行为开始写测试，再实现最小修改 / Start with an observable behavior test, then
  implement the smallest change.
- 修改 JSON 时同步更新测试、README 和 schema 策略 / Update tests, README, and schema
  policy when changing JSON.
- 修改依赖时更新 `requirements.in` 并用 README 中的固定命令重新生成带哈希锁文件 / Update
  `requirements.in` and regenerate the hash lock with the documented command.
- 网络测试默认使用 mock；实时 smoke test 必须显式运行并使用隔离配置 / Mock network calls
  by default; live smoke tests must be explicit and use isolated config.
- 不提交下载文件、`.part`、真实 URL、账号、token、cookie、`.env` 或 `config.json` / Never
  commit downloads, partials, private URLs, accounts, tokens, cookies, `.env`, or config files.
- URL 跟随逻辑必须测试重定向、私网目标和大小限制 / URL-following changes must test
  redirects, private targets, and size limits.

## Pull Request 要求 / Pull Request Expectations

PR 应说明用户问题、行为变化、测试证据、Skill 安装影响和兼容性。不要把真实服务完整 HTML、
账号数据或私人下载链接放进 fixture。

Describe the user problem, behavior change, test evidence, Skill-install impact, and
compatibility. Do not place complete live-service HTML, account data, or private download URLs
in fixtures.

提交 PR 即表示你的贡献可按 MIT License 分发，并且你有权提交这些代码。

By submitting a pull request, you agree that your contribution may be distributed under the
MIT License and confirm that you have the right to contribute it.

普通问题使用 Issue 模板；安全问题遵循 [SECURITY.md](SECURITY.md) 私密报告。

Use the issue templates for normal problems. Follow [SECURITY.md](SECURITY.md) for private
security reports.
