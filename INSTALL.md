# Skill Installation and Migration / Skill 安装与迁移

## 推荐指令 / Recommended Request

把下面完整指令发给具有 GitHub、文件写入和终端权限的 Agent：

Send this complete request to an agent with GitHub, filesystem, and terminal access:

> 请帮我安装这个 Agent Skill：https://github.com/soluna/zlib-anna-skill 。仓库根目录就是
> Skill 目录，不要使用 `pipx` 或安装全局 CLI。安装后请运行 Skill 自带的
> `scripts/run.py --version` 与 `scripts/run.py auth status --json` 验证，不要登录、搜索或
> 下载。
>
> Please install this Agent Skill: https://github.com/soluna/zlib-anna-skill . The repository
> root is the Skill directory. Do not use `pipx` or install a global CLI. Verify with the
> bundled `scripts/run.py --version` and `scripts/run.py auth status --json`. Do not log in,
> search, or download during installation.

## 为什么只需安装一次 / Why Installation Has One Surface

Skill 目录同时包含：

The Skill directory contains all required project-owned components:

- Agent 工作流：`SKILL.md` / Agent workflow.
- Agent 元数据：`agents/openai.yaml` / Agent metadata.
- 启动器：`scripts/run.py` / Bootstrap runner.
- 执行引擎：`scripts/zlib_anna/` / Deterministic execution engine.
- 带哈希依赖锁：`scripts/requirements.lock` / Hash-locked runtime dependencies.

首次真实命令会在用户缓存目录创建专用虚拟环境。这个内部准备步骤不安装全局命令、不修改系统
Python，也不需要用户单独管理第二个产品。

The first real command creates a dedicated virtual environment in the user cache. This
internal setup installs no global command, does not modify system Python, and does not require
the user to manage a second product.

## Codex 精确命令 / Exact Codex Command

Codex 的 GitHub Skill 安装器要求显式仓库路径，根目录使用 `--path .`：

The Codex GitHub Skill installer requires an explicit repository path; use `--path .` for the
root:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo soluna/zlib-anna-skill \
  --path . \
  --name zlib-anna-skill
```

验证安装时使用隔离配置，避免读取任何已有账号：

Use isolated config for verification so no existing account is read:

```bash
SKILL_DIR="$CODEX_HOME/skills/zlib-anna-skill"
python3 "$SKILL_DIR/scripts/run.py" --version
ZLIB_ANNA_CONFIG_DIR=/tmp/zlib-anna-install-check \
  python3 "$SKILL_DIR/scripts/run.py" auth status --json
```

第二条命令会准备运行依赖，需要 Python 3.9+ 和首次访问 Python 包索引的网络权限。安装成功
后重新开始一轮 Agent 对话，以便发现新 Skill。

The second command prepares runtime dependencies and requires Python 3.9+ plus first-use
package-index access. Start a new agent turn after installation so the new Skill is discovered.

## 手动安装 / Manual Installation

```bash
git clone https://github.com/soluna/zlib-anna-skill.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/zlib-anna-skill"
python3 "${CODEX_HOME:-$HOME/.codex}/skills/zlib-anna-skill/scripts/run.py" --version
```

不要覆盖含有用户修改的现有目录。账号配置和下载文件不应保存在 Skill 目录中。

Never overwrite an existing directory containing user changes. Account config and downloaded
files must not be stored inside the Skill directory.

## 更新 / Updating

手工 clone 的安装可在确认工作区干净后更新：

For a manually cloned installation, update only after confirming the worktree is clean:

```bash
git -C "${CODEX_HOME:-$HOME/.codex}/skills/zlib-anna-skill" status --short
git -C "${CODEX_HOME:-$HOME/.codex}/skills/zlib-anna-skill" pull --ff-only
```

安装器管理的副本应使用 Agent 的 Skill 更新流程重新安装。依赖锁或 Python 版本变化时，启动器
会创建新的版本化缓存；旧缓存不包含账号，但可在确认没有运行任务后删除。

Reinstall installer-managed copies through the agent runtime's Skill update flow. When the
dependency lock or Python version changes, the runner creates a new versioned cache. Old caches
contain no account data and may be removed after confirming no task is running.

## 从 zlib-cli 0.1.x 迁移 / Migrating from zlib-cli 0.1.x

1. 安装 `zlib-anna-skill`，不要覆盖旧 Skill / Install `zlib-anna-skill` separately.
2. 验证新 Skill 的 `auth status --json` / Verify the new Skill.
3. 从 Agent 配置中移除旧 `zlib-cli` Skill / Remove the old Skill registration.
4. 使用 `pipx uninstall zlib-cli` 删除旧全局命令 / Remove the old global command.

默认账号配置路径在 `0.x` 期间保持兼容。旧 `ZLIB_CLI_*` 环境变量仍可使用，但应迁移到
README 列出的 `ZLIB_ANNA_*` 名称。

The default account-config path remains compatible during `0.x`. Legacy `ZLIB_CLI_*`
environment variables still work, but should migrate to the `ZLIB_ANNA_*` names in the README.

## 其他 Agent / Other Agent Runtimes

完整安装要求 Agent 能读取 GitHub、写入 Skill 目录、运行 Python 3.9+，并能在首次使用时访问
Python 包索引。不支持 `SKILL.md` 的运行时不能称为完成 Skill 安装。

A complete installation requires GitHub read access, Skill-directory writes, Python 3.9+, and
first-use package-index access. A runtime without `SKILL.md` support cannot claim a complete
Skill installation.

没有终端或文件写入能力的 Agent 应返回手动命令，不能声称已经安装。安装请求只授权安装和
无账号验证，不授权登录、搜索或下载。

An agent without terminal or filesystem access must return manual commands and must not claim
success. An installation request authorizes installation and account-free verification only,
not login, search, or download.

## 验收标准 / Acceptance Criteria

- Skill 目录包含 `SKILL.md`、`agents/openai.yaml` 和 `scripts/run.py` / Required files exist.
- `--version` 输出 `zlib-anna-skill` 与当前版本 / Version reports the Skill name and version.
- `auth status --json` 返回 schema 2 JSON，且 `has_token` 为 false（隔离配置） / Isolated
  auth status returns schema 2 JSON with no token.
- 没有全局 `zlib-anna-skill` 命令或 `pipx` 要求 / No global command or pipx requirement.
- 安装期间没有登录、搜索、下载或凭据读取 / No login, search, download, or credential read.
