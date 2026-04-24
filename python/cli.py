"""CLI tool for running analytics reports."""
import argparse
import sys
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analytics CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    report_parser = subparsers.add_parser("report", help="Generate a report")
    report_parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"))
    report_parser.add_argument("--output", type=Path, default=Path("reports"))
    report_parser.add_argument("--format", choices=["json", "csv"], default="json")

    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    stats_parser.add_argument("--metric", type=str, required=True)
    stats_parser.add_argument("--days", type=int, default=7)

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.command == "report":
        print(f"Generating {args.format} report for {args.date}...")
        print(f"Output: {args.output}")
        return 0
    elif args.command == "stats":
        print(f"Stats for '{args.metric}' over {args.days} days")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
