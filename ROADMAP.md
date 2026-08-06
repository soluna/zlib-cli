# Roadmap / 路线图

## 0.2.x

中文：

- 稳定 agent contract：冻结常用 JSON 字段，记录兼容性策略。
- 改进 Anna 下载解析：更多镜像页面模式、验证码/会员页识别、更清晰的失败分类。
- 改进 Z-Library 域名解析：缓存探测结果、记录最近成功域名、提供 `domains --refresh`。
- 设计可审计、可签名的域名注册表更新机制，降低过期/接管域名风险。
- 可选系统 keychain 存储 Z-Library token；保留无交互 CI 模式。
- 拆分 `zlib_cli.py` 为命令层、来源适配器与下载策略模块。
- 增加安装方式：PyPI 或 GitHub release artifact。
- 增加更完整的无网络单元测试和少量手动网络 smoke test 文档。

English:

- Stabilize the agent contract: freeze common JSON fields and document compatibility rules.
- Improve Anna download resolution: more mirror page patterns, captcha/member-page detection, clearer failure categories.
- Improve Z-Library domain resolution: cache probe results, remember the last successful domain, add `domains --refresh`.
- Design an auditable, signed domain-registry update path to reduce stale/taken-over domain risk.
- Add optional OS-keychain token storage while preserving non-interactive CI use.
- Split `zlib_cli.py` into command, source-adapter, and download-policy modules.
- Add install channels: PyPI or GitHub release artifacts.
- Add fuller offline unit tests and a small manual network smoke-test guide.

## Later / 后续

中文：

- 可选 MCP/server wrapper，方便 agent 直接调用。
- 更好的批量任务报告：可恢复、可重试、可导出。
- 更强的元数据清洗：作者、语言、年份、格式统一规范。

English:

- Optional MCP/server wrapper for direct agent use.
- Better batch reports: resumable, retryable, exportable.
- Stronger metadata cleanup for author, language, year, and format normalization.
