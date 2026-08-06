# Open-Source Readiness Review / 开源就绪审查

Review date / 审查日期: 2026-08-06

## 结论 / Verdict

中文：当前代码、Skill、测试、打包与中英双语仓库材料达到 `0.1.0` alpha 开源标准。
本仓库由经过审查的 tracked-file snapshot 建立，不包含前置私有仓库的 Git 历史。仓库已经
公开，`main` CI、noreply 身份、分支保护、Private Vulnerability Reporting、secret scanning
和 push protection 均已验证。当前没有开源阻塞项。

English: The code, Skill, tests, packaging, and bilingual repository materials meet the
publication bar for a `0.1.0` alpha. This repository starts from an audited tracked-file
snapshot and contains no predecessor private Git history. It is now public, with green
`main` CI, noreply-only identity, branch protection, Private Vulnerability Reporting, secret
scanning, and push protection verified. No open-source blocker remains.

## 干净仓库边界 / Clean-Repository Boundary

- 只导入 tracked files，不导入 `.git`、refs、PR refs、bundle、缓存、构建产物或本地配置 /
  Only tracked files were imported; no `.git`, refs, PR refs, bundles, caches, build output,
  or local configuration were carried over.
- 新仓库必须使用 GitHub noreply 作者身份 / The new repository must use a GitHub noreply
  author identity.
- 不得把任何前置私有仓库添加为 remote 或合并其历史 / Never add a predecessor private
  repository as a remote or merge its history.
- 源码和审查过的历史中未发现真实 Z-Library token 或密码 / No real Z-Library token or
  password was found in the source or audited predecessor history.

## 发布前发现并修复 / Findings Resolved Before Publication

### OSR-001: 不可信域名可能接收 Z-Library token / Untrusted domain credential exposure

非内置/非入口发现域名默认不接触，必须由用户显式设置
`ZLIBRARY_ALLOW_UNTRUSTED_DOMAIN=1`；该授权不会持久化，Skill 禁止 Agent 猜测域名。

Domains outside the built-in/discovered trust set are blocked unless the user explicitly
opts in. That trust is not persisted, and the Skill forbids agents from guessing domains.

### OSR-002: 搜索和下载可被诱导访问内网 / Search and download could reach private networks

所有 Anna 搜索、详情、下载 URL 与每次重定向均经过校验，阻止 localhost、私有/链路本地
地址、内嵌凭据和解析到内网的域名。

Anna search, detail, download targets, and every redirect are validated, blocking local,
private, link-local, credential-bearing, and private-resolving destinations.

### OSR-003: 下载缺少大小、类型和完整性边界 / Missing download boundaries

下载使用流式写入和可配置大小上限；Anna 只接受已知电子书类型/扩展名并验证 MD5。空文件、
超限、类型异常和校验失败不会替换最终文件。

Downloads stream with a configurable size limit. Anna accepts known ebook types/extensions
and verifies MD5; empty, oversized, unexpected, or checksum-failing files never replace the
final output.

### OSR-004: Agent 协议与来源降级不稳定 / Unstable agent contract and source fallback

`--source all` 会隔离单来源错误并继续；所有响应包含 `schema_version`、`cli_version` 和稳定
错误码。默认异常不会回显上游正文、完整下载 URL 或 traceback。

`--source all` isolates source failures and continues. Every response carries schema/CLI
versions and stable error codes. Default errors do not echo remote page text, full download
URLs, or tracebacks.

### OSR-005: 开源仓库材料和维护门槛不完整 / Incomplete public materials and maintenance gates

仓库现包含中英双语 README、贡献指南、安全政策、行为准则、支持说明、第三方许可证、路线图、
变更记录、发布手册、Release Notes、PR/Issue 模板与 Agent 元数据。CI 覆盖 Python 3.9-3.14、
打包、依赖审计、Bandit 和秘密扫描。

The repository now contains bilingual README, contribution, security, conduct, support,
third-party, roadmap, changelog, release-guide, release-note, PR/issue, and agent metadata.
CI covers Python 3.9-3.14, packaging, dependency audit, Bandit, and secret scanning.

## 已知剩余风险 / Known Residual Risks

- Anna 依赖不稳定 HTML，页面改版仍会导致回归 / Anna relies on unstable HTML and can
  regress when markup changes.
- Z-Library 与 Anna 域名可能被封锁、吊销或接管，信任集合必须持续维护 / Domains can be
  blocked, revoked, or taken over; trust data requires maintenance.
- Z-Library token 仍为本地明文 JSON，不使用系统 keychain / The Z-Library token remains
  plaintext local JSON rather than an OS keychain secret.
- 默认 CI 不访问真实上游，不能提前发现所有页面变化 / Default CI avoids live services and
  cannot detect every upstream change.
- `zlib-cli` 容易与压缩库混淆，README 已标注但无法完全消除 / The name can be confused
  with the compression library; README reduces but does not eliminate that risk.
- CLI 主模块仍较大，后续应拆分命令、来源适配器和下载策略 / The main CLI module remains
  large and should later be split into commands, source adapters, and download policies.

以上是 alpha 维护风险，不是当前开源阻塞项。

These are alpha maintenance risks, not current publication blockers.

## 验证证据 / Validation Evidence

- Python 3.9 与 3.14：`93 passed`；3.9 仅有系统 LibreSSL/urllib3 环境警告 / `93 passed`
  on Python 3.9 and 3.14; 3.9 emitted only a system LibreSSL/urllib3 warning.
- Ruff、format check、compileall、Skill validator、YAML validation：passed.
- sdist 与 wheel 构建成功；wheel 安装后的 `--version`、`--help` 和 JSON error smoke 通过 /
  sdist/wheel build and installed-wheel version, help, and JSON-error smoke passed.
- `pip-audit`：无已知运行时依赖漏洞 / no known runtime dependency vulnerabilities.
- `bandit -ll`：无 medium/high findings / no medium/high findings.
- `detect-secrets`：最终文件快照 0 findings / zero findings in the final file snapshot.
- 无账号 Anna 隔离配置实时搜索成功，未下载文件 / An isolated, account-free Anna live
  search succeeded; no file was downloaded.
- 新公开仓库 `main` 的八个 GitHub CI jobs 全绿 / All eight GitHub CI jobs passed on the
  new public repository's `main`.
- 未登录视角可见 README、MIT License 与 Security Policy；匿名 HTTPS clone 和全新 venv
  安装后 `--version`、`--help` 通过 / README, MIT License, and Security Policy are visible
  while logged out; anonymous HTTPS clone and fresh-venv version/help checks passed.

## 最终发布门槛 / Final Release Gate

- [x] 新仓库历史仅含 noreply 提交 / New repository history contains only noreply commits.
- [x] 新仓库 `main` 的八个 GitHub CI checks 全绿 / All eight GitHub CI checks pass on `main`.
- [x] `origin` 只指向 `soluna/zlib-cli` / `origin` points only to `soluna/zlib-cli`.
- [x] Public 后已启用 branch protection 与 Private Vulnerability Reporting / Branch
  protection and Private Vulnerability Reporting are enabled after making the repository public.
- [x] 未登录浏览器和公开 URL 全新安装检查通过 / Logged-out and public clean-install checks pass.
- [x] `v0.1.0` tag 与 Release 已创建 / The `v0.1.0` tag and release exist.
