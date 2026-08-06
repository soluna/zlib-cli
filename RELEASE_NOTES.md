# zlib-skill 0.3.0

## 中文

`0.3.0` 将项目、GitHub 仓库和 Skill 标识统一缩短为 `zlib-skill`。

主要变化：

- 推荐安装请求缩短为一句：`请帮我安装这个 Agent Skill：https://github.com/soluna/zlib-skill`。
- 详细安装、隔离验证和故障排查命令移至 `INSTALL.md`，不再塞入首次请求。
- 默认运行缓存改为 `~/.cache/zlib-skill`；账号配置路径保持兼容，不要求重新登录。
- `ZLIB_SKILL_*` 成为规范环境变量；`ZLIB_ANNA_*` 与 `ZLIB_CLI_*` 在 `0.x` 保持兼容。
- 无 Z-Library 登录时默认继续使用 Anna，不会仅为了增加搜索覆盖要求登录。
- 只有用户明确选择 Z-Library 搜索或直接下载时，Agent 才引导用户在自己的终端安全登录。
- 运行器版本、Agent 元数据、CI、模板、安全链接和双语文档均更新为新名称。

从 `zlib-anna-skill` 更新时，应将 Skill 安装到新的 `zlib-skill` 目录，并移除旧 Skill
注册。旧仓库 URL 由 GitHub 重定向到新地址。

## English

`0.3.0` shortens and aligns the project, GitHub repository, and Skill identifier as
`zlib-skill`.

Highlights:

- The recommended install request is now one line: `Please install this Agent Skill:
  https://github.com/soluna/zlib-skill`.
- Detailed installation, isolated verification, and troubleshooting commands move to
  `INSTALL.md` instead of burdening the first request.
- The default runtime cache moves to `~/.cache/zlib-skill`; the account-config path remains
  compatible, so users do not need to log in again.
- `ZLIB_SKILL_*` becomes canonical; `ZLIB_ANNA_*` and `ZLIB_CLI_*` remain compatible during
  `0.x`.
- Without a Z-Library login, the Skill continues with Anna and does not request login merely
  to improve search coverage.
- The agent guides secure terminal login only when the user explicitly chooses Z-Library
  search or direct download.
- Runner output, agent metadata, CI, templates, security links, and bilingual documentation
  now use the new name.

When updating from `zlib-anna-skill`, install into the new `zlib-skill` directory and remove
the old Skill registration. GitHub redirects the previous repository URL to the new address.
