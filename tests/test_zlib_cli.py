"""Unit tests for the agent-first CLI contract."""

import argparse
import hashlib
import json
import re
import stat
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

import zlib_cli

PDF_BODY = b"%PDF fake"
PDF_MD5 = hashlib.md5(PDF_BODY, usedforsecurity=False).hexdigest()
EPUB_BODY = b"epub bytes"
EPUB_MD5 = hashlib.md5(EPUB_BODY, usedforsecurity=False).hexdigest()


@pytest.fixture(autouse=True)
def allow_mock_network(monkeypatch):
    monkeypatch.setenv("ZLIB_CLI_ALLOW_PRIVATE_NETWORK", "1")


class FakeResponse:
    def __init__(
        self,
        url,
        *,
        headers=None,
        body=b"",
        text=None,
        status_code=200,
    ):
        self.url = url
        self.headers = headers or {}
        self.body = body
        self._text = text
        self.status_code = status_code

    @property
    def text(self):
        if self._text is not None:
            return self._text
        return self.body.decode("utf-8")

    def raise_for_status(self):
        if self.status_code >= 400:
            raise zlib_cli.requests.HTTPError(str(self.status_code), response=self)

    def iter_content(self, chunk_size=1024):
        yield self.body

    def close(self):
        pass


@pytest.fixture
def temp_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / "zlib_cli"
        config_file = config_dir / "config.json"
        with patch("zlib_cli.CONFIG_DIR", config_dir), patch("zlib_cli.CONFIG_FILE", config_file):
            yield config_dir, config_file


def test_load_config_empty(temp_config):
    assert zlib_cli.load_config() == {}


def test_safe_json_response_rejects_non_object_payload():
    response = MagicMock()
    response.json.return_value = ["unexpected", "payload"]

    assert zlib_cli.safe_json_response(response) is None


def test_load_config_rejects_non_object_json(temp_config):
    config_dir, config_file = temp_config
    config_dir.mkdir(parents=True)
    config_file.write_text("[]", encoding="utf-8")

    with pytest.raises(zlib_cli.CliError) as exc:
        zlib_cli.load_config()

    assert exc.value.code == "CONFIG_INVALID"
    assert zlib_cli.load_config(strict=False) == {}


def test_save_config_uses_private_permissions(temp_config):
    config_dir, config_file = temp_config
    cfg = {"remix_userid": "123", "remix_userkey": "token-value", "domain": "test.example"}

    zlib_cli.save_config(cfg)

    assert zlib_cli.load_config() == cfg
    assert stat.S_IMODE(config_dir.stat().st_mode) == 0o700
    assert stat.S_IMODE(config_file.stat().st_mode) == 0o600


def test_load_config_repairs_legacy_permissions(temp_config):
    config_dir, config_file = temp_config
    config_dir.mkdir(parents=True)
    config_file.write_text(
        json.dumps({"remix_userid": "123", "remix_userkey": "token-value"}),
        encoding="utf-8",
    )
    config_dir.chmod(0o755)
    config_file.chmod(0o644)

    cfg = zlib_cli.load_config()

    assert cfg["remix_userkey"] == "token-value"
    assert stat.S_IMODE(config_dir.stat().st_mode) == 0o700
    assert stat.S_IMODE(config_file.stat().st_mode) == 0o600


def test_config_status_reports_permission_repairs(temp_config):
    config_dir, config_file = temp_config
    config_dir.mkdir(parents=True)
    config_file.write_text(
        json.dumps({"remix_userid": "123", "remix_userkey": "token-value"}),
        encoding="utf-8",
    )
    config_dir.chmod(0o755)
    config_file.chmod(0o644)

    status = zlib_cli.config_status()

    assert status["config_dir_mode"] == "0o700"
    assert status["config_file_mode"] == "0o600"
    assert {item["kind"] for item in status["permission_repairs"]} == {
        "config_dir",
        "config_file",
    }


def test_config_status_redacts_sensitive_values(temp_config):
    _, config_file = temp_config
    zlib_cli.save_config(
        {
            "remix_userid": "42",
            "remix_userkey": "token-value",
            "domain": "z-library.example",
            "email": "secret@example.com",
            "name": "Test User",
        }
    )

    status = zlib_cli.config_status()
    encoded = json.dumps(status)

    assert status["zlib"]["has_token"] is True
    assert status["zlib"]["email"] == "s****t@example.com"
    assert "token-value" not in encoded
    assert str(config_file) in encoded


def test_config_status_reports_zlib_domain_override(temp_config):
    with patch.dict(zlib_cli.os.environ, {"ZLIBRARY_DOMAIN": "https://env.example/path"}):
        status = zlib_cli.config_status()

    assert status["zlib"]["domain_env"] == "env.example"


def test_mask_email_handles_empty_local_part():
    assert zlib_cli.mask_email("@example.com") == "*@example.com"


def test_fetch_domains_filters_unusable_domains():
    with patch("zlib_cli.requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "success": True,
            "domains": [
                {"domain": "z-library.example", "contentAvailable": True, "isRedirector": False},
                {"domain": "redirect.example", "contentAvailable": True, "isRedirector": True},
                {"domain": "offline.example", "contentAvailable": False, "isRedirector": False},
            ],
        }
        mock_get.return_value = mock_resp

        domains = zlib_cli.fetch_domains()

    assert domains == ["z-library.example"]


def test_test_domain_handles_request_errors():
    with patch(
        "zlib_cli.requests.get",
        side_effect=zlib_cli.requests.RequestException("network down"),
    ):
        assert zlib_cli.test_domain("bad.example") is False


def test_find_working_domain_prefers_env_override():
    with (
        patch.dict(
            zlib_cli.os.environ,
            {
                "ZLIBRARY_DOMAIN": "https://env.example/path",
                "ZLIBRARY_ALLOW_UNTRUSTED_DOMAIN": "1",
            },
        ),
        patch(
            "zlib_cli.test_domain",
            return_value=True,
        ) as mock_test_domain,
    ):
        domain, checks = zlib_cli.find_working_domain("config.example")

    assert domain == "env.example"
    assert checks == [
        {
            "domain": "env.example",
            "available": True,
            "source": "env",
            "trusted": True,
            "trust_basis": "explicit_opt_in",
        }
    ]
    mock_test_domain.assert_called_once_with("env.example")
    assert zlib_cli.domain_trust_is_persistent(domain, checks) is False


def test_find_working_domain_does_not_contact_untrusted_override(monkeypatch):
    monkeypatch.setenv("ZLIBRARY_DOMAIN", "untrusted.example")
    monkeypatch.delenv("ZLIBRARY_ALLOW_UNTRUSTED_DOMAIN", raising=False)

    with (
        patch("zlib_cli.fetch_domains", return_value=[]),
        patch(
            "zlib_cli.test_domain",
            return_value=True,
        ) as mock_test_domain,
    ):
        domain, checks = zlib_cli.find_working_domain()

    assert domain == "z-library.sk"
    assert checks[0]["domain"] == "untrusted.example"
    assert checks[0]["reason"] == "untrusted_domain"
    assert "untrusted.example" not in {call.args[0] for call in mock_test_domain.call_args_list}


def test_download_dir_status_reports_creatable_when_home_is_missing(tmp_path):
    missing_home = tmp_path / "missing-home"
    download_dir = missing_home / "Books"

    status = zlib_cli.download_dir_status(download_dir)

    assert status["exists"] is False
    assert status["parent_exists"] is False
    assert status["nearest_existing_parent"] == str(tmp_path)
    assert status["creatable"] is True


def test_parser_supports_json_and_source_choices():
    parser = zlib_cli.build_parser()

    args = parser.parse_args(["search", "clean code", "--source", "all", "--json"])

    assert args.command == "search"
    assert args.source == "all"
    assert args.json is True


def test_parser_help_includes_first_run_examples():
    help_text = zlib_cli.build_parser().format_help()

    assert "Examples:" in help_text
    assert "ZLIBRARY_DOMAIN" in help_text
    assert "==SUPPRESS==" not in help_text


def test_parser_rejects_non_positive_limits():
    parser = zlib_cli.build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["search", "python", "--limit", "0"])


def test_main_emits_json_for_argument_errors(capsys):
    exit_code = zlib_cli.main(["search", "python", "--limit", "0", "--json"])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert json.loads(captured.out)["error"]["code"] == "INVALID_ARGUMENT"
    assert "usage:" in captured.err


def test_app_version_matches_pyproject():
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    match = re.search(r'^version = "([^"]+)"', pyproject.read_text(encoding="utf-8"), re.M)

    assert match
    assert zlib_cli.APP_VERSION == match.group(1)


@pytest.mark.parametrize(
    ("value", "source", "hash_id", "expected"),
    [
        ("zlib:123:abc", "auto", None, ("zlib", "123", "abc")),
        (
            "anna:deadbeefdeadbeefdeadbeefdeadbeef",
            "auto",
            None,
            ("anna", "deadbeefdeadbeefdeadbeefdeadbeef", None),
        ),
        ("123", "zlib", "abc", ("zlib", "123", "abc")),
        (
            "deadbeefdeadbeefdeadbeefdeadbeef",
            "anna",
            None,
            ("anna", "deadbeefdeadbeefdeadbeefdeadbeef", None),
        ),
    ],
)
def test_parse_result_ref(value, source, hash_id, expected):
    assert zlib_cli.parse_result_ref(value, source, hash_id) == expected


@pytest.mark.parametrize(
    "value",
    [
        "anna:deadbeef",
        "anna:../../etc/passwd",
        "zlib:not-a-number:hash",
        "zlib:123:hash/with/slash",
    ],
)
def test_parse_result_ref_rejects_malformed_ids(value):
    with pytest.raises(zlib_cli.CliError) as exc:
        zlib_cli.parse_result_ref(value)

    assert exc.value.code == "INVALID_RESULT_ID"


def test_search_all_falls_back_to_anna_without_zlib_auth(temp_config):
    args = argparse.Namespace(
        query="python",
        source="all",
        limit=10,
        page=1,
        year_from=None,
        year_to=None,
        lang=None,
        ext=None,
        order=None,
        json=False,
    )
    anna_book = {
        "result_id": "anna:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "source": "anna",
        "md5": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "title": "Python Book",
        "author": "A. Author",
        "year": "2024",
        "extension": "PDF",
        "size": "1MB",
    }
    anna_status = zlib_cli.SourceStatus(
        source="anna",
        available=True,
        authenticated=False,
        can_search=True,
        can_download=True,
        status="ok",
    )

    with patch("zlib_cli.search_anna", return_value=([anna_book], anna_status)):
        payload = zlib_cli.cmd_search(args)

    assert payload["ok"] is True
    assert payload["results"] == [anna_book]
    assert payload["sources"][0]["source"] == "zlib"
    assert payload["sources"][0]["status"] == "auth_required"


def test_search_all_continues_when_zlib_source_errors(temp_config):
    args = argparse.Namespace(
        query="python",
        source="all",
        limit=10,
        page=1,
        year_from=None,
        year_to=None,
        lang=None,
        ext=None,
        order=None,
        json=False,
    )
    anna_book = {
        "result_id": "anna:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "source": "anna",
    }
    anna_status = zlib_cli.SourceStatus(
        source="anna",
        available=True,
        can_search=True,
        can_attempt_download=True,
        status="ok",
    )

    with (
        patch(
            "zlib_cli.search_zlib",
            side_effect=zlib_cli.CliError("SOURCE_UNAVAILABLE", "blocked"),
        ),
        patch("zlib_cli.search_anna", return_value=([anna_book], anna_status)),
    ):
        payload = zlib_cli.cmd_search(args)

    assert payload["ok"] is True
    assert payload["results"] == [anna_book]
    assert payload["sources"][0]["source"] == "zlib"
    assert payload["sources"][0]["status"] == "error"


def test_search_zlib_without_auth_is_error(temp_config):
    args = argparse.Namespace(source="zlib")

    with pytest.raises(zlib_cli.CliError) as exc:
        zlib_cli.search_zlib(args, {})

    assert exc.value.code == "AUTH_REQUIRED"


def test_normalize_anna_book_marks_download_as_best_effort():
    book = {
        "md5": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "title": "Example Book",
        "ext": "PDF",
        "detail_url": "https://annas.example/md5/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    }

    result = zlib_cli.normalize_anna_book(book)

    assert result["can_download"] is False
    assert result["can_attempt_download"] is True
    assert result["download_guaranteed"] is False
    assert result["download_strategy"] == "html_best_effort"
    assert result["best_effort"] is True


def test_anna_filters_year_and_language_locally():
    args = argparse.Namespace(
        query="python",
        source="anna",
        limit=10,
        page=1,
        year_from=2020,
        year_to=2025,
        lang="en",
        ext=None,
        order="popular",
    )
    client = MagicMock()
    client.search.return_value = [
        {
            "md5": "a" * 32,
            "title": "Keep",
            "language": "English [en]",
            "year": "2022",
        },
        {
            "md5": "b" * 32,
            "title": "Wrong language",
            "language": "Chinese [zh]",
            "year": "2022",
        },
        {
            "md5": "c" * 32,
            "title": "Too old",
            "language": "English [en]",
            "year": "2010",
        },
    ]

    with patch("zlib_cli.annas_archive.AnnasArchiveClient", return_value=client):
        books, status = zlib_cli.search_anna(args)

    assert [book["title"] for book in books] == ["Keep"]
    assert status.can_download is False
    assert status.can_attempt_download is True
    assert status.details["ignored_filters"] == ["order"]


def test_search_anna_sanitizes_upstream_failure(monkeypatch):
    args = argparse.Namespace(
        query="private query",
        source="all",
        limit=10,
        page=1,
        year_from=None,
        year_to=None,
        lang=None,
        ext=None,
        order=None,
    )
    client = MagicMock()
    client.search.side_effect = zlib_cli.requests.ConnectionError(
        "request failed for https://annas.example/private?token=secret"
    )
    monkeypatch.setenv("ANNAS_BASE_URL", "https://annas.example/private?token=secret")

    with patch("zlib_cli.annas_archive.AnnasArchiveClient", return_value=client):
        books, status = zlib_cli.search_anna(args)

    assert books == []
    assert status.message == "Anna's Archive request failed."
    assert status.details == {
        "base_origin": "https://annas.example",
        "error_type": "ConnectionError",
    }
    assert "token" not in json.dumps(status.to_dict())


def test_main_json_error_is_machine_readable(capsys):
    exit_code = zlib_cli.main(["download", "unknown-id", "--json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 1
    assert payload["ok"] is False
    assert payload["schema_version"] == "1"
    assert payload["cli_version"] == zlib_cli.APP_VERSION
    assert payload["error"]["code"] == "SOURCE_REQUIRED"
    assert captured.err == ""


def test_download_anna_direct_file_response(tmp_path):
    args = argparse.Namespace(output=str(tmp_path))
    fake_session = MagicMock()
    fake_session.get.return_value = FakeResponse(
        "https://files.example/book.pdf",
        headers={
            "content-type": "application/pdf",
            "content-disposition": 'attachment; filename="Book.pdf"',
        },
        body=PDF_BODY,
    )

    with (
        patch(
            "zlib_cli.anna_links",
            return_value={
                "detail_url": f"https://annas.example/md5/{PDF_MD5}",
                "libgen_li": "https://files.example/book.pdf",
                "libgen_is": None,
                "libgen_rs": None,
                "fast_downloads": [],
            },
        ),
        patch("zlib_cli.requests.Session", return_value=fake_session),
    ):
        payload = zlib_cli.download_anna(args, PDF_MD5)

    assert payload["ok"] is True
    assert payload["downloaded"] is True
    assert payload["source"] == "anna"
    assert payload["path"].endswith("Book.pdf")
    assert Path(payload["path"]).read_bytes() == PDF_BODY


def test_download_anna_follows_html_download_link(tmp_path):
    args = argparse.Namespace(output=str(tmp_path))
    fake_session = MagicMock()
    fake_session.get.side_effect = [
        FakeResponse(
            "https://libgen.example/book",
            headers={"content-type": "text/html; charset=utf-8"},
            text=f'<html><a href="/get.php?md5={EPUB_MD5}">GET</a></html>',
        ),
        FakeResponse(
            f"https://libgen.example/get.php?md5={EPUB_MD5}",
            headers={"content-type": "application/epub+zip"},
            body=EPUB_BODY,
        ),
    ]

    with (
        patch(
            "zlib_cli.anna_links",
            return_value={
                "detail_url": f"https://annas.example/md5/{EPUB_MD5}",
                "libgen_li": "https://libgen.example/book",
                "libgen_is": None,
                "libgen_rs": None,
                "fast_downloads": [],
            },
        ),
        patch("zlib_cli.requests.Session", return_value=fake_session),
    ):
        payload = zlib_cli.download_anna(args, EPUB_MD5)

    assert payload["downloaded"] is True
    assert payload["final_origin"] == "https://libgen.example"
    assert Path(payload["path"]).name == f"anna-{EPUB_MD5}.epub"
    assert Path(payload["path"]).read_bytes() == EPUB_BODY


def test_download_anna_reports_links_when_no_candidate_downloads(tmp_path):
    args = argparse.Namespace(output=str(tmp_path))
    fake_session = MagicMock()
    fake_session.get.return_value = FakeResponse(
        "https://libgen.example/book",
        headers={"content-type": "text/html"},
        text="<html><p>captcha required</p></html>",
    )
    links = {
        "detail_url": "https://annas.example/md5/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "libgen_li": "https://libgen.example/book",
        "libgen_is": None,
        "libgen_rs": None,
        "fast_downloads": [],
    }

    with (
        patch("zlib_cli.anna_links", return_value=links),
        patch(
            "zlib_cli.requests.Session",
            return_value=fake_session,
        ),
    ):
        with pytest.raises(zlib_cli.CliError) as exc:
            zlib_cli.download_anna(args, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    assert exc.value.code == "DOWNLOAD_FAILED"
    assert exc.value.details["attempts"][0]["kind"] == "libgen_li"
    assert exc.value.details["available_link_kinds"] == ["libgen_li"]


def test_download_anna_does_not_expose_resolved_link_map_when_empty(tmp_path):
    args = argparse.Namespace(output=str(tmp_path), max_size_mb=1)
    detail_url = "https://annas.example/md5/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    with patch(
        "zlib_cli.anna_links",
        return_value={
            "detail_url": detail_url,
            "libgen_li": None,
            "libgen_is": None,
            "libgen_rs": None,
            "fast_downloads": [],
        },
    ):
        with pytest.raises(zlib_cli.CliError) as exc:
            zlib_cli.download_anna(args, "a" * 32)

    assert exc.value.code == "DOWNLOAD_LINKS_NOT_FOUND"
    assert exc.value.details == {
        "detail_url": detail_url,
        "available_link_kinds": [],
    }


def test_download_anna_rejects_checksum_mismatch_and_removes_partial(tmp_path):
    args = argparse.Namespace(output=str(tmp_path), max_size_mb=1)
    fake_session = MagicMock()
    fake_session.get.return_value = FakeResponse(
        "https://files.example/book.pdf",
        headers={"content-type": "application/pdf"},
        body=PDF_BODY,
    )
    wrong_md5 = "0" * 32

    with (
        patch(
            "zlib_cli.anna_links",
            return_value={
                "detail_url": f"https://annas.example/md5/{wrong_md5}",
                "libgen_li": "https://files.example/book.pdf",
                "libgen_is": None,
                "libgen_rs": None,
                "fast_downloads": [],
            },
        ),
        patch("zlib_cli.requests.Session", return_value=fake_session),
    ):
        with pytest.raises(zlib_cli.CliError) as exc:
            zlib_cli.download_anna(args, wrong_md5)

    assert exc.value.code == "DOWNLOAD_FAILED"
    assert list(tmp_path.iterdir()) == []


def test_write_response_rejects_declared_file_over_size_limit(tmp_path):
    response = FakeResponse(
        "https://files.example/book.pdf",
        headers={"content-type": "application/pdf", "content-length": "100"},
        body=PDF_BODY,
    )

    with pytest.raises(ValueError, match="size limit"):
        zlib_cli.write_response_to_path(response, tmp_path / "book.part", max_bytes=10)


def test_filename_from_response_replaces_executable_extension():
    response = FakeResponse(
        "https://files.example/download",
        headers={
            "content-type": "application/pdf",
            "content-disposition": 'attachment; filename="book.exe"',
        },
    )

    assert zlib_cli.filename_from_response(response, "fallback") == "book.pdf"


def test_main_converts_unexpected_exception_to_safe_json(capsys):
    result_id = "anna:" + "a" * 32

    with patch("zlib_cli.cmd_download", side_effect=RuntimeError("secret-url-token")):
        exit_code = zlib_cli.main(["download", result_id, "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert payload["error"]["code"] == "UNEXPECTED_ERROR"
    assert payload["error"]["details"]["error_type"] == "RuntimeError"
    assert "secret-url-token" not in json.dumps(payload)


def test_imports_are_available():
    import annas_archive
    from Zlibrary import Zlibrary

    assert hasattr(zlib_cli, "main")
    assert hasattr(zlib_cli, "build_parser")
    assert hasattr(annas_archive, "AnnasArchiveClient")
    assert hasattr(Zlibrary(), "setDomain")
