# Agent Installation Guide / Agent 安装指南

## 推荐说法 / Recommended Request

把下面完整指令发给具有 GitHub 与终端权限的 Agent：

Send this complete request to an agent with GitHub and terminal access:

> 请帮我安装这个 Agent Skill 及其 CLI：https://github.com/soluna/zlib-cli 。仓库根目录
> 就是 Skill 目录。请完成 Skill 注册、CLI 安装，并运行 `zlib-cli --version` 和
> `zlib-cli doctor --json` 验证。安装阶段不要登录账号、搜索或下载电子书。
>
> Please install both the Agent Skill and CLI from https://github.com/soluna/zlib-cli .
> The repository root is the skill directory. Register the skill, install the CLI, and run
> `zlib-cli --version` plus `zlib-cli doctor --json` to verify. Do not log in, search, or
> download anything during installation.

不建议只说“请帮我安装这个 URL”。不同 Agent 对“安装 GitHub 仓库”的理解不同，可能只
clone、只注册 Skill，或者只安装 Python 包。完整指令明确要求两个安装面和验证步骤。

Avoid saying only “install this URL.” Agent runtimes interpret GitHub installation
differently and may only clone, only register the skill, or only install the Python package.
The complete request names both installation surfaces and the verification steps.

## 为什么有两个步骤 / Why Installation Has Two Parts

1. **Skill 注册 / Skill registration**：让 Agent 发现并读取 `SKILL.md`。
2. **CLI 安装 / CLI installation**：让 Skill 能调用 PATH 中的 `zlib-cli` 命令。

The Skill contains behavior and safety instructions; the CLI contains the executable Python
implementation. Installing either one alone leaves the integration incomplete.

只安装 Skill 时，首次执行会找不到 `zlib-cli`。只安装 CLI 时，命令可用，但 Agent 不会自动
获得搜索、确认后下载、凭据保护和失败降级规则。

With only the Skill, execution fails because `zlib-cli` is missing. With only the CLI, the
command works but the agent does not automatically receive the search-first, confirmation,
credential, and fallback rules.

## Codex 精确安装命令 / Exact Codex Commands

Codex 当前的 GitHub Skill 安装器要求显式提供仓库内路径。仓库根 URL 本身没有 path，因此
必须使用 `--path . --name zlib-cli`：

The current Codex GitHub Skill installer requires an explicit path inside the repository.
Because a repository-root URL has no path, use `--path . --name zlib-cli`:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo soluna/zlib-cli \
  --path . \
  --name zlib-cli

pipx install git+https://github.com/soluna/zlib-cli.git
zlib-cli --version
zlib-cli doctor --json
```

Skill 会在 Agent 的下一轮可用。`doctor` 可以检查环境与来源可访问性，但安装过程不需要
Z-Library 账号，也不应要求密码、token 或 cookie。

The Skill becomes available to the agent on its next turn. `doctor` checks the environment
and source reachability, but installation requires no Z-Library account and must not request
a password, token, or cookie.

如果 `pipx` 不存在，Agent 应说明缺少的工具，并使用该操作系统的正常方式安装 `pipx`；不要
使用未经确认的 `sudo`、不要修改系统 Python，也不要退化为不受控的全局 `pip install`。

If `pipx` is unavailable, the agent should report the missing prerequisite and install it
through the operating system's normal mechanism. It must not use unapproved `sudo`, modify
the system Python, or silently fall back to an unmanaged global `pip install`.

## 手动安装 / Manual Installation

```bash
git clone https://github.com/soluna/zlib-cli.git ~/.codex/skills/zlib-cli
pipx install ~/.codex/skills/zlib-cli
zlib-cli --version
zlib-cli doctor --json
```

如果目标 Skill 目录已经存在，先确认它是否是本仓库的旧版本。不要直接覆盖包含用户修改的
目录。CLI 可使用 `pipx upgrade zlib-cli` 更新；从本地目录安装的环境可用
`pipx install --force ~/.codex/skills/zlib-cli` 重建。

If the destination skill directory already exists, first determine whether it is an older
copy of this repository. Never overwrite a directory containing user changes. Upgrade a
registry/Git-installed CLI with `pipx upgrade zlib-cli`; rebuild a local-directory install
with `pipx install --force ~/.codex/skills/zlib-cli`.

## 其他 Agent / Other Agent Runtimes

直接安装仅在 Agent 同时具备以下能力时成立：

Direct installation works only when the agent can:

- 读取公开 GitHub 仓库 / Read a public GitHub repository.
- 运行终端命令 / Run terminal commands.
- 把目录注册到自身的 Skill 搜索路径 / Register a directory in its skill search path.
- 安装隔离的 Python CLI 并访问其 PATH / Install an isolated Python CLI and expose it on PATH.

不支持 `SKILL.md` 的 Agent 仍可安装并调用 CLI，但不能称为完成 Skill 安装。没有终端或文件
写入权限的 Agent 应返回手动命令，不能声称已经安装。

An agent without `SKILL.md` support can still install and call the CLI, but that is not a
complete Skill installation. An agent without terminal or filesystem write access must
return manual commands and must not claim installation succeeded.

## 验收标准 / Acceptance Criteria

安装成功必须同时满足：

A successful installation must satisfy all of the following:

- Skill 目录中存在 `SKILL.md` 和 `agents/openai.yaml` / The skill directory contains both files.
- `zlib-cli --version` 输出当前已安装版本 / The version command reports the installed
  version.
- `zlib-cli doctor --json` 输出可解析 JSON，且不回显 token / Doctor returns parseable JSON
  without exposing a token.
- 安装期间没有登录、搜索或下载 / Installation performs no login, search, or download.

安装完成后，用户可以直接说“帮我找某本书”；Skill 会先搜索和展示候选，只有用户明确要求或
确认结果后才会下载。

After installation, the user can ask to find a book. The Skill searches and presents
candidates first, and downloads only after an explicit request or confirmation.
