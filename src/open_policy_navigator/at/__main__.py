"""Command line for Austria (needs `pdftotext` for fetch and refetch).

    python -m open_policy_navigator.at fetch XXVIII,XXVII out.jsonl
    python -m open_policy_navigator.at refetch in.jsonl out.jsonl
    python -m open_policy_navigator.at report zaehlung/at/at-vorblaetter.jsonl

fetch and refetch only write NEW files; an existing file is never overwritten.
"""

import argparse
from pathlib import Path

from open_policy_navigator.at.parlament import fetch_records, http_get, refetch
from open_policy_navigator.at.report import build_report, format_report
from open_policy_navigator.records import read_jsonl, write_jsonl


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m open_policy_navigator.at")
    commands = parser.add_subparsers(dest="command", required=True)
    fetch = commands.add_parser("fetch", help="fetch bills into a NEW jsonl file")
    fetch.add_argument("periods", help="comma separated periods, e.g. XXVIII,XXVII")
    fetch.add_argument("out", type=Path)
    again = commands.add_parser("refetch", help="re-read full WFAs without field text")
    again.add_argument("data", type=Path)
    again.add_argument("out", type=Path)
    report = commands.add_parser("report", help="print the counts for a jsonl file")
    report.add_argument("data", type=Path)
    args = parser.parse_args(argv)

    if args.command == "fetch":
        written = write_jsonl(args.out, fetch_records(http_get, args.periods.split(",")))
        print(f"wrote {written} records to {args.out}")
    elif args.command == "refetch":
        written = write_jsonl(args.out, refetch(http_get, read_jsonl(args.data)))
        print(f"wrote {written} records to {args.out}")
    else:
        print(format_report(build_report(read_jsonl(args.data))))


if __name__ == "__main__":
    main()
