from pathlib import Path

import pytest

from app.cli import PROJECT_DESCRIPTION
from app.cli import main
from app.cli import parse_args


def test_parse_args_returns_existing_config_path(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 1\n", encoding="utf-8")

    parsed_args = parse_args(["--config", str(config_file)])

    assert parsed_args.config == config_file


def test_parse_args_exits_on_missing_config() -> None:
    with pytest.raises(SystemExit):
        parse_args(["--config", "missing.yml"])


def test_main_returns_zero_for_existing_config(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 1\n", encoding="utf-8")

    exit_code = main(["--config", str(config_file)])

    assert exit_code == 0


def test_parser_description_mentions_project_goal() -> None:
    assert "Анализатор логов nginx" in PROJECT_DESCRIPTION
