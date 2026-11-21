"""Command line for Germany.

python -m open_policy_navigator.de fetch 20,21 out.jsonl   (needs DIP_API_KEY)
python -m open_policy_navigator.de report zaehlung/de/dip-gesetzentwuerfe.jsonl
"""

import argparse
from pathlib import Path

from open_policy_navigator.de.dip import DipClient, api_key_from_env, fetch_records
from open_policy_navigator.de.report import build_report, format_report
from open_policy_navigator.records import read_jsonl, write_jsonl


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m open_policy_navigator.de")
    commands = parser.add_subparsers(dest="command", required=True)
    fetch = commands.add_parser("fetch", help="fetch draft laws from DIP into a NEW jsonl file")
    fetch.add_argument("periods", help="comma separated electoral periods, e.g. 20,21")
    fetch.add_argument("out", type=Path)
    report = commands.add_parser("report", help="print the counts for a jsonl file")
    report.add_argument("data", type=Path)
    args = parser.parse_args(argv)

    if args.command == "fetch":
        client = DipClient(api_key_from_env())
        written = write_jsonl(args.out, fetch_records(client, args.periods.split(",")))
        print(f"wrote {written} records to {args.out}")
    else:
        print(format_report(build_report(read_jsonl(args.data))))


if __name__ == "__main__":
    main()
