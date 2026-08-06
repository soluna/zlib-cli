# zlib-skill 0.3.1

## 中文

`0.3.1` 重新设计了用户第一次看到和实际使用这个 Skill 的方式。

- README 先说明怎么找书、怎么选版本、没有账号能否使用，再提供安装与使用示例。
- 推荐安装仍然只有一句，手工命令和环境配置留在 `INSTALL.md`。
- 新增可以直接对 Agent 说的自然语言示例，不要求用户理解来源网站或内部命令。
- Agent 会把搜索结果整理成简短书单，展示书名、作者、语言、格式和来源。
- 搜索与下载继续分开；多个版本合理时请用户选择，明确指定时不重复确认。
- 没有 Z-Library 登录时继续使用 Anna's Archive，不为增加搜索覆盖强迫登录。
- 运行失败、来源不可用和高级网络配置移到按需加载的故障参考。

本版本不改变账号存储位置，也不会读取维护者账号。安装验证不会登录、搜索或下载。

## English

`0.3.1` redesigns how users first encounter and use the Skill.

- The README begins with finding, choosing, account-free use, and natural request examples.
- The recommended install remains one line; manual commands and environment configuration stay
  in `INSTALL.md`.
- Users can speak naturally without understanding source websites or internal commands.
- Search results become a short readable book list with title, author, language, format, and
  source.
- Search and download remain separate. The agent asks when editions are ambiguous and avoids
  repeating confirmation when the choice is already explicit.
- Without Z-Library login, the Skill continues with Anna's Archive instead of forcing login.
- Runtime, source, and advanced network troubleshooting now loads only when a failure occurs.

This release does not change account storage or use the maintainer's account. Installation
verification performs no login, search, or download.
