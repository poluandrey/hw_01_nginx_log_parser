import argparse
from pathlib import Path

PROJECT_DESCRIPTION = (
    "Анализатор логов nginx: сервис формирует статистический отчет "
    "о характеристиках запросов на основании парсинга логов."
)


def existing_file(file_path: str) -> Path:
    """Validate that config path points to an existing file."""
    path = Path(file_path)
    if not path.is_file():
        raise argparse.ArgumentTypeError(
            f"Config file does not exist: {file_path}",
        )
    return path


def build_parser() -> argparse.ArgumentParser:
    """Create CLI parser for the log analyzer."""
    parser = argparse.ArgumentParser(description=PROJECT_DESCRIPTION)
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        type=existing_file,
        help="Path to config file.",
    )
    return parser


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    return build_parser().parse_args(args)


def main(args: list[str] | None = None) -> int:
    """CLI entry point."""
    parse_args(args)
    return 0
