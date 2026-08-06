# Open-Source Release Guide / 开源发布手册

本手册面向 `soluna/zlib-cli` 维护者，说明如何验证干净仓库、切换公开可见性并发布首个版本。

This guide is for the `soluna/zlib-cli` maintainer. It covers clean-history verification,
public visibility, and the first release.

## 先看结论 / Read This First

本仓库必须始终保持独立、干净的公开历史。它最初由经过审查的 tracked-file snapshot 创建，
不得导入或合并任何前置私有仓库的 Git 历史、refs、PR refs 或 bundle。

This repository must keep an independent, clean public history. It was created from an
audited tracked-file snapshot. Never import or merge Git history, refs, pull-request refs,
or bundles from any predecessor private repository.

## 1. 验证历史与工作区 / Verify History and Worktree

确认工作区干净，所有提交都使用公开身份：

Confirm that the worktree is clean and every commit uses a public identity:

```bash
git status --short --branch
git log --all --format='%h %an <%ae> %s'
git remote -v
```

提交邮箱应为 GitHub noreply 地址，不应出现私人邮箱。`origin` 必须指向
`https://github.com/soluna/zlib-cli.git`，不能指向任何内部仓库。

Commit emails must use a GitHub noreply address; no private email should appear. `origin`
must point to `https://github.com/soluna/zlib-cli.git`, never to an internal repository.

## 2. 运行发布验证 / Run Release Verification

在全新虚拟环境中执行：

Run the release gate in a fresh virtual environment:

```bash
python3 -m venv .release-venv
. .release-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

pytest -q
ruff check .
ruff format --check .
python -m compileall -q zlib_cli.py Zlibrary.py annas_archive.py network_safety.py tests
python -m build
pip-audit -r requirements.txt
bandit -q -r zlib_cli.py Zlibrary.py annas_archive.py network_safety.py -ll
git ls-files -z | xargs -0 detect-secrets scan > /tmp/zlib-cli-secrets.json
python -c 'import json; data=json.load(open("/tmp/zlib-cli-secrets.json")); raise SystemExit(bool(data["results"]))'
```

检查构建产物并从 wheel 安装：

Inspect the artifacts and install from the wheel:

```bash
python -m venv .wheel-venv
.wheel-venv/bin/python -m pip install dist/*.whl
.wheel-venv/bin/zlib-cli --version
.wheel-venv/bin/zlib-cli --help
```

不要读取真实 `~/.config/zlib_cli/config.json`。需要实时 smoke test 时使用隔离配置目录，
且只测试无账号 Anna 搜索，不执行下载：

Do not read the real `~/.config/zlib_cli/config.json`. If a live smoke test is needed, use
an isolated config directory and only test account-free Anna search; do not download:

```bash
ZLIB_CLI_CONFIG_DIR=/tmp/zlib-cli-release-config \
zlib-cli search "public domain book" --source anna --limit 1 --json
```

真实上游受地区、封锁和页面变化影响，不作为默认 CI 的硬门槛；但失败必须保持结构化且可诊断。

Live upstream behavior varies by region, blocking, and markup. It is not a default CI gate,
but failures must remain structured and actionable.

## 3. 验证 GitHub CI / Verify GitHub CI

公开前，`main` 最新提交必须通过以下 checks：

Before publication, the latest `main` commit must pass:

- Python 3.9-3.14 六个 test matrix jobs / six Python 3.9-3.14 test matrix jobs.
- `package`：sdist、wheel 和安装冒烟 / sdist, wheel, and install smoke tests.
- `security`：`pip-audit`、Bandit、`detect-secrets` / dependency, static, and secret scans.

```bash
gh run list --repo soluna/zlib-cli --branch main --limit 5
gh run watch --repo soluna/zlib-cli --exit-status
```

## 4. 配置仓库元数据 / Configure Repository Metadata

```bash
gh repo edit soluna/zlib-cli \
  --description "Agent-first CLI and skill for Z-Library and Anna's Archive ebook search and downloads" \
  --enable-issues=true \
  --enable-wiki=false

gh repo edit soluna/zlib-cli \
  --add-topic agent-skill \
  --add-topic anna-archive \
  --add-topic cli \
  --add-topic ebook \
  --add-topic python \
  --add-topic z-library
```

确认 Actions 默认 `GITHUB_TOKEN` 为 read-only，并启用 Dependabot alerts。Secret scanning
和 push protection 在当前仓库/套餐可用时也应启用。

Confirm that the default Actions `GITHUB_TOKEN` is read-only and enable Dependabot alerts.
Also enable secret scanning and push protection when available for the repository and plan.

## 5. 切换 Public 并立即加固 / Make Public and Harden Immediately

只有历史、验证和 CI 均通过后才执行：

Only after history, validation, and CI pass:

```bash
gh repo edit soluna/zlib-cli \
  --visibility public \
  --accept-visibility-change-consequences
```

随后立即完成以下操作，在完成前不要发布 Release 或对外公告：

Immediately complete the following before announcing the repository or publishing a release:

- 为 `main` 启用 branch protection，要求全部八个 CI checks，并阻止 force push / Protect
  `main`, require all eight CI checks, and block force pushes.
- 启用 Private Vulnerability Reporting / Enable Private Vulnerability Reporting.
- 在未登录浏览器中检查 README、LICENSE、SECURITY、Issues 和 Actions / Check README,
  license, security policy, issues, and Actions while logged out.
- 从公开 URL 在全新目录安装并运行 `--version`、`--help` / Install from the public URL in
  a clean directory and run version/help.

GitHub 的 Private Vulnerability Reporting 只对 Public 仓库开放，官方说明见
[Configuring private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configuring-private-vulnerability-reporting-for-a-repository)。

GitHub Private Vulnerability Reporting is available only for public repositories. See
[GitHub's configuration documentation](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configuring-private-vulnerability-reporting-for-a-repository).

## 6. 创建首个 Release / Create the First Release

```bash
git tag -a v0.1.0 -m "zlib-cli 0.1.0"
git push origin v0.1.0
gh release create v0.1.0 \
  --verify-tag \
  --title "zlib-cli 0.1.0" \
  --notes-file RELEASE_NOTES.md
```

首发暂不上传 PyPI，除非先确认包名、Trusted Publisher 和发布所有权。GitHub/pipx 安装足以
支持第一阶段用户。

Do not publish the first release to PyPI until package naming, Trusted Publisher, and
ownership are confirmed. GitHub/pipx installation is sufficient for phase 1.

## 发布门槛 / Release Checklist

- [ ] `origin` 只指向公开仓库 / `origin` points only to the public repository.
- [ ] 所有提交均为 noreply，无私人邮箱或凭据 / All commits use noreply and contain no secrets.
- [ ] 本地 release gate 和 GitHub 八个 checks 全绿 / Local release gate and all eight checks pass.
- [ ] 仓库已 Public，branch protection 与 Private Vulnerability Reporting 已启用 / The
  repository is public with branch protection and private vulnerability reporting enabled.
- [ ] 未登录浏览器和全新安装检查通过 / Logged-out and clean-install checks pass.
- [ ] `v0.1.0` tag 与 Release 已创建 / The `v0.1.0` tag and release exist.
