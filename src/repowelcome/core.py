"""Open-source contributor readiness audits."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _exists(root: Path, *patterns: str) -> bool:
    return any(any(path.is_file() for path in root.glob(pattern)) for pattern in patterns)


def _readme_sections(root: Path) -> set[str]:
    candidates = sorted(root.glob("README*"))
    if not candidates:
        return set()
    text = candidates[0].read_text(encoding="utf-8", errors="ignore")
    return {match.group(1).strip().lower() for match in re.finditer(r"^#{1,6}\s+(.+)$", text, re.MULTILINE)}


def _manifest_commands(root: Path) -> dict[str, bool]:
    result = {"test_command": False, "lint_command": False}
    package = root / "package.json"
    if package.is_file():
        try:
            scripts = json.loads(package.read_text(encoding="utf-8")).get("scripts", {})
            result["test_command"] = isinstance(scripts, dict) and "test" in scripts
            result["lint_command"] = isinstance(scripts, dict) and any(name in scripts for name in ("lint", "check"))
        except json.JSONDecodeError:
            pass
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        result["test_command"] = result["test_command"] or _exists(root, "tests/test*.py", "test_*.py")
        result["lint_command"] = result["lint_command"] or any(name in pyproject.read_text(encoding="utf-8", errors="ignore") for name in ("ruff", "mypy", "pytest"))
    return result


def audit_repository(root: Path) -> dict[str, Any]:
    """Score contributor onboarding and maintenance hygiene."""
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"{root} is not a repository directory")
    sections = _readme_sections(root)
    commands = _manifest_commands(root)
    checks = [
        ("RW001", "README", _exists(root, "README*"), 12, "Add a concise README with purpose, install, use, and support information."),
        ("RW002", "Open-source license", _exists(root, "LICENSE*", "COPYING*"), 12, "Add an OSI-approved license file and mention it in the README."),
        ("RW003", "Contribution guide", _exists(root, "CONTRIBUTING*", ".github/CONTRIBUTING*"), 10, "Document the development setup, tests, review expectations, and fixture policy."),
        ("RW004", "Code of conduct", _exists(root, "CODE_OF_CONDUCT*", ".github/CODE_OF_CONDUCT*"), 6, "Add a community code of conduct and enforcement path."),
        ("RW005", "Security policy", _exists(root, "SECURITY*", ".github/SECURITY*"), 8, "Explain how to report vulnerabilities privately."),
        ("RW006", "Issue templates", _exists(root, ".github/ISSUE_TEMPLATE/*"), 7, "Add focused bug and feature issue forms."),
        ("RW007", "Pull request template", _exists(root, ".github/PULL_REQUEST_TEMPLATE*", ".github/pull_request_template*"), 6, "Add a pull request checklist for tests, scope, and security impact."),
        ("RW008", "Continuous integration", _exists(root, ".github/workflows/*.yml", ".github/workflows/*.yaml"), 12, "Run tests on pushes and pull requests with least-privilege permissions."),
        ("RW009", "Automated tests", _exists(root, "tests/*", "test/*", "__tests__/*"), 10, "Add a fast test suite with synthetic fixtures."),
        ("RW010", "Reproducible dependency lock", _exists(root, "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock", "uv.lock", "Pipfile.lock"), 5, "Commit the ecosystem's dependency lock file when appropriate."),
        ("RW011", "Documented install/use sections", any("install" in section or "getting started" in section for section in sections) and any("usage" in section or "run" in section for section in sections), 7, "Add clear installation and usage headings to the README."),
        ("RW012", "Runnable test command", commands["test_command"], 5, "Expose one documented command that runs the test suite."),
    ]
    results = [
        {"id": identifier, "name": name, "passed": passed, "weight": weight, "recommendation": recommendation}
        for identifier, name, passed, weight, recommendation in checks
    ]
    score = sum(item["weight"] for item in results if item["passed"])
    grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F"
    return {
        "schema_version": 1,
        "repository": str(root),
        "score": score,
        "grade": grade,
        "checks": results,
        "summary": {"passed": sum(item["passed"] for item in results), "total": len(results)},
    }


def render_issue(report: dict[str, Any]) -> str:
    missing = [check for check in report["checks"] if not check["passed"]]
    lines = [
        "# Improve contributor readiness",
        "",
        f"RepoWelcome score: **{report['score']}/100 ({report['grade']})**",
        "",
        "This checklist was generated deterministically. Review each recommendation before implementation.",
        "",
    ]
    lines.extend(f"- [ ] **{check['name']}** — {check['recommendation']}" for check in missing)
    if not missing:
        lines.append("- [x] All current RepoWelcome checks pass.")
    lines.extend(["", "Generated by RepoWelcome.", ""])
    return "\n".join(lines)

