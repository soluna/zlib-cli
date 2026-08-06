# Troubleshooting

Read this file only after the normal search, login, source check, or download flow fails.

## Runtime Setup

When the runner returns `RUNTIME_SETUP_FAILED`, explain that the Skill could not prepare its
local runtime. Report the safe `details.step` and the provided suggestions. It needs Python 3.9+
and package-index access on first use.

Do not use `sudo`, global `pip`, or `pipx` as a fallback. Do not replace the bundled runner with
an improvised scraper.

## Check Source Availability

Run:

```bash
python3 {baseDir}/scripts/run.py doctor --json
```

Summarize which source is unavailable and what the user can do next. Do not dump the full JSON.

## Login Problems

- `AUTH_REQUIRED`: continue with Anna's Archive unless the user explicitly wants Z-Library.
- `AUTH_INVALID`: explain that the saved login expired or is invalid. Offer `auth logout`, then
  a fresh terminal login.
- Never request or echo the password in chat.

## Source Address Problems

Z-Library domains can change. Ask the user for a domain they independently verified. Use
`ZLIBRARY_DOMAIN` only with that value. Never take a domain from an arbitrary search result and
send credentials to it.

For Anna's Archive, suggest a user-verified `ANNAS_BASE_URL`, `HTTPS_PROXY`, or `ALL_PROXY` when
the normal address is blocked.

Unknown Z-Library domains require the user's explicit approval before
`ZLIBRARY_ALLOW_UNTRUSTED_DOMAIN=1`. Private-network and insecure-HTTP overrides also require
explicit approval and are only appropriate in a controlled environment.

## Failed Downloads

For a failed Anna download, explain that automatic download is best-effort. Report the stable
error code, the detail page when safe, available link kinds, and failed attempts. Captchas,
member-only pages, dead mirrors, and network blocking can prevent a download.

For every source, distinguish these outcomes clearly:

- Found: a matching edition exists.
- Download attempted: the Skill tried one or more links.
- Downloaded: a verified local file was saved.

Only the last outcome is a completed download.
