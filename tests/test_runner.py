"""Black-box tests for the bundled Skill runner."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import run as runner

ROOT = Path(__file__).parent.parent
RUNNER = ROOT / "scripts" / "run.py"


def test_runner_reports_skill_version_without_creating_runtime(tmp_path):
    runtime_root = tmp_path / "runtime"
    env = os.environ.copy()
    env["ZLIB_SKILL_RUNTIME_DIR"] = str(runtime_root)

    result = subprocess.run(
        [sys.executable, str(RUNNER), "--version"],
        capture_output=True,
        check=False,
        env=env,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout == "zlib-skill 0.3.1\n"
    assert result.stderr == ""
    assert not runtime_root.exists()


def test_runtime_root_prefers_new_name_and_accepts_previous_alias(monkeypatch, tmp_path):
    canonical = tmp_path / "canonical"
    previous = tmp_path / "previous"
    monkeypatch.setenv("ZLIB_SKILL_RUNTIME_DIR", str(canonical))
    monkeypatch.setenv("ZLIB_ANNA_RUNTIME_DIR", str(previous))

    assert runner.runtime_root() == canonical

    monkeypatch.delenv("ZLIB_SKILL_RUNTIME_DIR")
    assert runner.runtime_root() == previous


def test_runner_reports_runtime_setup_failure_as_safe_json(monkeypatch, capsys):
    def fail_setup():
        raise runner.RuntimeSetupError("install_dependencies", RuntimeError("secret-index-token"))

    monkeypatch.setattr(runner, "ensure_runtime", fail_setup)

    exit_code = runner.main(["auth", "status", "--json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 1
    assert payload["ok"] is False
    assert payload["schema_version"] == "2"
    assert payload["skill_version"] == "0.3.1"
    assert payload["error"]["code"] == "RUNTIME_SETUP_FAILED"
    assert payload["error"]["details"] == {
        "step": "install_dependencies",
        "error_type": "RuntimeError",
    }
    assert "secret-index-token" not in captured.out
    assert "secret-index-token" not in captured.err


def test_runner_reuses_matching_runtime(monkeypatch, tmp_path):
    monkeypatch.setenv("ZLIB_SKILL_RUNTIME_DIR", str(tmp_path / "runtime-root"))
    runtime = runner.runtime_path()
    python = runner.runtime_python(runtime)
    python.parent.mkdir(parents=True)
    python.touch()
    (runtime / runner.READY_FILE).write_text(
        json.dumps({"fingerprint": runner.runtime_fingerprint()}),
        encoding="utf-8",
    )

    def unexpected_build(_runtime):
        pytest.fail("a matching runtime must be reused")

    monkeypatch.setattr(runner, "build_runtime", unexpected_build)

    assert runner.ensure_runtime() == python


def test_runtime_fingerprint_changes_when_dependency_lock_changes(monkeypatch, tmp_path):
    lock = tmp_path / "requirements.lock"
    monkeypatch.setattr(runner, "LOCK_FILE", lock)
    lock.write_text("requests==1 --hash=sha256:first\n", encoding="utf-8")
    first = runner.runtime_fingerprint()
    lock.write_text("requests==2 --hash=sha256:second\n", encoding="utf-8")

    assert runner.runtime_fingerprint() != first


def test_build_runtime_installs_only_hash_locked_binary_dependencies(monkeypatch, tmp_path):
    runtime = tmp_path / "runtime-root" / "runtime"
    calls = []

    class FakeBuilder:
        def create(self, destination):
            python = runner.runtime_python(Path(destination))
            python.parent.mkdir(parents=True)
            python.touch()

    monkeypatch.setattr(runner.venv, "EnvBuilder", lambda **_kwargs: FakeBuilder())
    monkeypatch.setattr(
        runner,
        "_run_setup_step",
        lambda command, step: calls.append((command, step)),
    )

    runner.build_runtime(runtime)

    install, install_step = calls[0]
    assert install[1:4] == ["-I", "-m", "pip"]
    assert "--require-hashes" in install
    assert "--only-binary=:all:" in install
    assert install_step == "install_dependencies"
    assert calls[1][1] == "verify_dependencies"
    assert runner.runtime_is_ready(runtime)


def test_runner_executes_engine_in_isolated_mode(monkeypatch):
    runtime_python = Path("/runtime/bin/python")
    monkeypatch.setattr(runner, "ensure_runtime", lambda: runtime_python)
    captured = {}

    def fake_exec(executable, arguments, environment):
        captured.update(
            executable=executable,
            arguments=arguments,
            environment=environment,
        )
        raise RuntimeError("exec intercepted")

    monkeypatch.setattr(runner.os, "execve", fake_exec)

    with pytest.raises(RuntimeError, match="exec intercepted"):
        runner.main(["search", "Python", "--source", "anna", "--json"])

    assert captured["executable"] == str(runtime_python)
    assert captured["arguments"][:4] == [
        str(runtime_python),
        "-I",
        "-c",
        runner.ENGINE_BOOTSTRAP,
    ]
    assert captured["arguments"][4] == str(ROOT / "scripts")
    assert captured["arguments"][5:] == ["search", "Python", "--source", "anna", "--json"]
    assert captured["environment"] == os.environ
