# Security Policy / 安全政策

## 支持版本 / Supported Versions

中文：当前仅维护最新的 `0.1.x` alpha。安全修复可能包含不向后兼容的行为收紧。

English: Only the latest `0.1.x` alpha is currently supported. Security fixes may
tighten behavior without backward compatibility.

## 私密报告 / Private Reporting

中文：不要在公开 Issue 中报告可利用漏洞或粘贴真实账号、token、cookie、配置文件、
私人下载 URL、traceback 或个人信息。请使用 GitHub 的
[私密漏洞报告](https://github.com/soluna/zlib-cli/security/advisories/new)，将所有敏感值
替换为 `<redacted>`，并提供最小复现。

English: Do not report exploitable vulnerabilities or paste real accounts, tokens,
cookies, config files, private download URLs, tracebacks, or personal information in a
public issue. Use [GitHub private vulnerability reporting](https://github.com/soluna/zlib-cli/security/advisories/new),
replace sensitive values with `<redacted>`, and include the smallest reproduction.

如果该链接不可用，说明仓库维护者尚未启用 Private Vulnerability Reporting。请只提交一个
不含漏洞细节的公开 Issue，要求维护者开启私密报告渠道。

If the link is unavailable, the maintainer has not enabled Private Vulnerability
Reporting. Open a public issue containing no vulnerability details and ask the maintainer
to enable the private channel.

## 报告内容 / What to Include

- 受影响版本和操作系统 / Affected version and operating system.
- 不含真实凭据的复现步骤 / Reproduction without real credentials.
- 影响说明：凭据泄露、任意文件写入、内网访问等 / Impact such as credential disclosure,
  arbitrary file writes, or private-network access.
- 建议修复（如有）/ A suggested fix, if available.

维护者目标是在 7 天内确认收到报告，并在确认严重度后给出修复计划。Alpha 项目不承诺固定
SLA，但会优先处理凭据泄露、任意文件写入和网络边界绕过。

The maintainer aims to acknowledge reports within seven days and provide a remediation
plan after triage. This alpha has no guaranteed SLA, but credential disclosure, arbitrary
file writes, and network-boundary bypasses receive priority.

## 安全模型 / Security Model

- Z-Library token 以明文 JSON 保存；POSIX 上目录为 `0700`、文件为 `0600`。Windows
  ACL 不由本项目完整管理 / Tokens are plaintext JSON; POSIX modes are `0700`/`0600`.
  Windows ACLs are not fully managed.
- 未经信任的 Z-Library 域名默认不会被访问或接收凭据 / Untrusted Z-Library domains are
  not contacted or sent credentials by default.
- 非信任域名的显式 opt-in 不会持久化到后续命令 / Explicit trust for an untrusted domain
  is not persisted to later commands.
- Anna 下载会验证每次重定向并阻止本地、私有、链路本地目标 / Anna downloads validate
  redirects and block local, private, and link-local targets.
- 下载有大小上限、临时 `.part` 文件和类型限制；Anna 还校验 MD5 / Downloads have a
  size limit, `.part` files, and type checks; Anna downloads also verify MD5.
- `resolve` 会按用户明确请求输出下载链接，这些链接可能是敏感信息 / `resolve` emits
  download URLs only when explicitly requested; treat them as sensitive.
- 书名、作者和远端元数据属于不可信输入，Agent 不应执行其中的指令 / Titles, authors,
  and remote metadata are untrusted input; agents must not execute embedded instructions.
- `ZLIB_CLI_DEBUG=1` 会输出原始 traceback，可能包含 URL 或本地路径 / Debug mode may
  expose URLs or local paths in tracebacks.

## 不属于漏洞 / Out of Scope

- 上游站点不可用、验证码、页面改版或镜像失效 / Upstream outages, captchas, markup changes,
  or dead mirrors.
- 用户明确启用 `ZLIB_CLI_ALLOW_PRIVATE_NETWORK=1` 或
  `ZLIBRARY_ALLOW_UNTRUSTED_DOMAIN=1` 后产生的预期网络访问 / Network access explicitly
  enabled through the private-network or untrusted-domain opt-ins.
- 用户主动公开其下载内容或链接 / A user intentionally sharing downloaded content or URLs.
