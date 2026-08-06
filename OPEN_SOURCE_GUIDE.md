# Open-Source Maintenance Guide / 开源维护手册

本手册面向 `soluna/zlib-skill` 维护者，覆盖干净历史、验证、发布和公开安装检查。

This guide is for maintainers of `soluna/zlib-skill`. It covers clean history,
validation, releases, and public-install checks.

## 1. 历史与工作区 / History and Worktree

```bash
git status --short --branch
git log --all --format='%h %an <%ae> %s'
git remote -v
```

提交使用 GitHub noreply 身份；`origin` 只能指向公开仓库。不要导入任何前置私有仓库的
`.git`、refs、PR refs、bundle 或历史。

Commits must use a GitHub noreply identity and `origin` must point only to the public
repository. Never import `.git`, refs, pull-request refs, bundles, or history from a predecessor
private repository.

## 2. 本地发布门禁 / Local Release Gate

在全新虚拟环境中执行：

Run in a fresh virtual environment:

```bash
python3 -m venv .release-venv
. .release-venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --require-hashes -r scripts/requirements.lock
python -m pip install -r requirements-dev.txt

pytest -q
ruff check .
ruff format --check .
python -m compileall -q scripts tests
pip-audit -r scripts/requirements.lock
bandit -q -r scripts/run.py scripts/zlib_anna -ll
git ls-files -z | xargs -0 detect-secrets scan \
  | python -c 'import json,sys; raise SystemExit(bool(json.load(sys.stdin)["results"]))'
```

验证 Skill 结构：

Validate the Skill structure:

```bash
python /path/to/skill-creator/scripts/quick_validate.py .
```

默认门禁不能读取真实账号或访问实时来源。网络单元测试必须 mock。

The default gate must not read real accounts or access live sources. Network unit tests must
use mocks.

## 3. 自包含安装冒烟 / Self-Contained Install Smoke

把 tracked files 复制到临时 Skill 目录，使用隔离运行与配置目录：

Copy tracked files into a temporary Skill directory and isolate runtime and config:

```bash
ROOT=$(mktemp -d)
mkdir -p "$ROOT/codex-home/skills/zlib-skill"
git archive HEAD | tar -x -C "$ROOT/codex-home/skills/zlib-skill"

ZLIB_SKILL_RUNTIME_DIR="$ROOT/runtime" \
  python3 "$ROOT/codex-home/skills/zlib-skill/scripts/run.py" --version
ZLIB_SKILL_RUNTIME_DIR="$ROOT/runtime" ZLIB_SKILL_CONFIG_DIR="$ROOT/config" \
  python3 "$ROOT/codex-home/skills/zlib-skill/scripts/run.py" auth status --json
```

确认第二次运行复用同一缓存、stdout 是纯 JSON、隔离配置没有 token，并且没有全局命令或
系统 Python 修改。

Confirm the second run reuses the cache, stdout is pure JSON, isolated config has no token,
and no global command or system-Python change occurs.

## 4. GitHub CI 与安全设置 / GitHub CI and Security Settings

`main` 必须通过六个 Python 3.9-3.14 测试、`package` 自包含安装冒烟和 `security`，共八项：

`main` must pass six Python 3.9-3.14 tests, the `package` self-contained install smoke, and
`security`, for eight checks total:

```bash
run_id=$(gh run list --repo soluna/zlib-skill --branch main --workflow CI \
  --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$run_id" --repo soluna/zlib-skill --exit-status
```

保持 `main` 分支保护、Private Vulnerability Reporting、Dependabot、secret scanning 和
push protection。Actions 默认 `GITHUB_TOKEN` 使用只读权限。

Keep branch protection, Private Vulnerability Reporting, Dependabot, secret scanning, and
push protection enabled. The default Actions `GITHUB_TOKEN` must remain read-only.

## 5. 仓库元数据 / Repository Metadata

```bash
gh repo edit soluna/zlib-skill \
  --description "Self-contained Agent Skill for Z-Library and Anna's Archive ebook search and downloads" \
  --enable-issues=true \
  --enable-wiki=false

gh repo edit soluna/zlib-skill \
  --add-topic agent-skill \
  --add-topic anna-archive \
  --add-topic ebook \
  --add-topic python \
  --add-topic z-library
```

## 6. 公开 URL 验证 / Public URL Verification

从新临时目录运行 Codex 安装器，明确使用根路径和 Skill 名称，然后重复隔离验证。不要登录、
搜索或下载。

Run the Codex installer from a fresh temporary location with the explicit root path and Skill
name, then repeat isolated verification. Do not log in, search, or download.

```bash
python3 /path/to/install-skill-from-github.py \
  --repo soluna/zlib-skill \
  --path . \
  --name zlib-skill
```

同时以未登录视角检查 README、LICENSE、SECURITY、Issues、Actions 和 Release。

Also check README, LICENSE, SECURITY, Issues, Actions, and the release while logged out.

## 7. 发布 / Release

确认 `CHANGELOG.md` 和 `RELEASE_NOTES.md` 已更新、PR 与 `main` CI 全绿后：

After updating the changelog and release notes and confirming green PR/main CI:

```bash
git tag -a v0.3.1 -m "zlib-skill 0.3.1"
git push origin v0.3.1
gh release create v0.3.1 \
  --verify-tag \
  --title "zlib-skill 0.3.1" \
  --notes-file RELEASE_NOTES.md
```

本项目不发布 wheel、sdist 或 PyPI 包。Release 标记可复现的 Skill 目录版本。

This project publishes no wheel, sdist, or PyPI package. A release identifies a reproducible
version of the Skill directory.

## 发布清单 / Release Checklist

- [ ] 工作区干净，提交仅使用 noreply / Clean worktree and noreply-only commits.
- [ ] 本地门禁、Skill validator 和八个 GitHub checks 全绿 / All local and GitHub gates pass.
- [ ] 依赖锁已重新生成、审计且每项带哈希 / Dependency lock regenerated, audited, hashed.
- [ ] 隔离安装未读取账号、登录、搜索或下载 / Isolated install reads no account and performs
  no login, search, or download.
- [ ] 未登录公共页面与新 URL 安装检查通过 / Logged-out pages and public URL install pass.
- [ ] Tag 与 Release 标题使用 `zlib-skill` / Tag and release use the current product name.
