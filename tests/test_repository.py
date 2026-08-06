"""Repository-level release and documentation checks."""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
REQUIRED_PUBLIC_FILES = {
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "INSTALL.md",
    "LICENSE",
    "OPEN_SOURCE_GUIDE.md",
    "OPEN_SOURCE_READINESS.md",
    "README.md",
    "RELEASE_NOTES.md",
    "ROADMAP.md",
    "SECURITY.md",
    "SKILL.md",
    "SUPPORT.md",
    "THIRD_PARTY_NOTICES.md",
    "agents/openai.yaml",
}


def test_required_public_files_exist():
    missing = sorted(path for path in REQUIRED_PUBLIC_FILES if not (ROOT / path).is_file())

    assert missing == []


def test_manifest_includes_public_markdown_documents():
    manifest = (ROOT / "MANIFEST.in").read_text(encoding="utf-8")
    expected = REQUIRED_PUBLIC_FILES - {"agents/openai.yaml", "LICENSE"}

    for path in sorted(expected):
        assert f"include {path}" in manifest
    assert "recursive-include agents *.yaml" in manifest


def test_relative_markdown_links_resolve():
    markdown_files = list(ROOT.glob("*.md"))
    broken = []
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

    for markdown_file in markdown_files:
        text = markdown_file.read_text(encoding="utf-8")
        for target in pattern.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (markdown_file.parent / target).exists():
                broken.append(f"{markdown_file.name}: {target}")

    assert broken == []


def test_skill_frontmatter_uses_only_supported_keys():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]
    keys = {line.split(":", 1)[0].strip() for line in frontmatter.splitlines() if ":" in line}

    assert keys == {"name", "description"}


def test_readme_leads_with_complete_agent_install_request():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    first_screen = "\n".join(text.splitlines()[:50])

    assert "直接让 Agent 安装 / Ask Your Agent to Install" in first_screen
    assert "请帮我安装这个 Agent Skill 及其 CLI" in first_screen
    assert "https://github.com/soluna/zlib-cli" in first_screen
    assert "zlib-cli --version" in first_screen
    assert text.index("Ask Your Agent to Install") < text.index("60 秒开始")


def test_install_guide_covers_both_installation_surfaces():
    text = (ROOT / "INSTALL.md").read_text(encoding="utf-8")

    assert "--repo soluna/zlib-cli" in text
    assert "--path ." in text
    assert "--name zlib-cli" in text
    assert "pipx install git+https://github.com/soluna/zlib-cli.git" in text
    assert "zlib-cli doctor --json" in text
    assert "must not claim installation succeeded" in text
