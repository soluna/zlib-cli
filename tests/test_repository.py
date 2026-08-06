"""Repository-level checks for the public self-contained Skill."""

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
REQUIRED_SKILL_FILES = {
    "scripts/run.py",
    "scripts/requirements.in",
    "scripts/requirements.lock",
    "scripts/zlib_anna/__init__.py",
    "scripts/zlib_anna/annas_archive.py",
    "scripts/zlib_anna/engine.py",
    "scripts/zlib_anna/network_safety.py",
    "scripts/zlib_anna/zlibrary.py",
}


def test_required_public_and_skill_files_exist():
    required = REQUIRED_PUBLIC_FILES | REQUIRED_SKILL_FILES
    missing = sorted(path for path in required if not (ROOT / path).is_file())

    assert missing == []


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


def test_skill_frontmatter_uses_new_name_and_supported_keys():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]
    keys = {line.split(":", 1)[0].strip() for line in frontmatter.splitlines() if ":" in line}

    assert keys == {"name", "description"}
    assert "name: zlib-anna-skill" in frontmatter


def test_readme_leads_with_single_skill_install_request():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    first_screen = "\n".join(text.splitlines()[:45])

    assert "直接让 Agent 安装 / Ask Your Agent to Install" in first_screen
    assert "请帮我安装这个 Agent Skill" in first_screen
    assert "https://github.com/soluna/zlib-anna-skill" in first_screen
    assert "python3 {baseDir}/scripts/run.py --version" in first_screen
    assert "不要另外安装全局 CLI" in first_screen


def test_install_guide_has_one_install_surface_and_isolated_verification():
    text = (ROOT / "INSTALL.md").read_text(encoding="utf-8")

    assert "--repo soluna/zlib-anna-skill" in text
    assert "--path ." in text
    assert "--name zlib-anna-skill" in text
    assert "scripts/run.py" in text
    assert "ZLIB_ANNA_CONFIG_DIR=" in text
    assert "/tmp/zlib-anna-install-check" in text
    assert "pipx install" not in text
    assert "must not claim" in text


def test_skill_invokes_only_the_bundled_runner():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "python3 {baseDir}/scripts/run.py" in text
    assert "pipx" in text  # Explicitly forbidden as a fallback.
    assert "pipx install" not in text
    assert "zlib-cli " not in text


def test_runtime_lock_pins_and_hashes_every_package():
    text = (ROOT / "scripts" / "requirements.lock").read_text(encoding="utf-8")
    package_starts = [
        match.start() for match in re.finditer(r"(?m)^[a-z0-9][a-z0-9-]*==[^\n]+", text)
    ]

    assert package_starts
    for index, start in enumerate(package_starts):
        end = package_starts[index + 1] if index + 1 < len(package_starts) else len(text)
        assert "--hash=sha256:" in text[start:end]


def test_repository_has_no_standalone_python_package_surface():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert not (ROOT / "MANIFEST.in").exists()
    assert not (ROOT / "requirements.txt").exists()
    assert list(ROOT.glob("*.py")) == []
    assert "[project]" not in pyproject
    assert "[project.scripts]" not in pyproject
    assert "[build-system]" not in pyproject


def test_active_install_docs_use_new_repository_url():
    for path in ("README.md", "INSTALL.md", "SKILL.md", "CONTRIBUTING.md", "SECURITY.md"):
        text = (ROOT / path).read_text(encoding="utf-8")
        assert "github.com/soluna/zlib-cli" not in text
