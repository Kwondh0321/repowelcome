"""Command-line interface for RepoWelcome."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import audit_repository, render_issue


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="오픈소스 저장소의 신규 기여자 준비 상태를 검사합니다.")
    parser.add_argument("repository", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--format", choices=("text", "json", "issue"), default="text")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--minimum-score", type=int, default=75)
    args = parser.parse_args(argv)
    try:
        report = audit_repository(args.repository)
    except (OSError, ValueError) as error:
        print(f"repowelcome: {error}", file=sys.stderr)
        return 2
    if args.format == "json":
        rendered = json.dumps(report, indent=2)
    elif args.format == "issue":
        rendered = render_issue(report)
    else:
        lines = [f"RepoWelcome: {report['score']}/100 ({report['grade']})"]
        lines.extend(f"[{'통과' if check['passed'] else '누락'}] {check['id']} {check['name']}" for check in report["checks"])
        rendered = "\n".join(lines)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 1 if report["score"] < args.minimum_score else 0


if __name__ == "__main__":
    raise SystemExit(main())
