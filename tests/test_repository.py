"""Repository-level release and documentation checks."""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
REQUIRED_PUBLIC_FILES = {
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
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
