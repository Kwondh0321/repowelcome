"""Open-source contributor readiness audits."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _exists(root: Path, *patterns: str) -> bool:
    return any(
        any(path.is_file() and not path.is_symlink() for path in root.glob(pattern))
        for pattern in patterns
    )


def _readme_sections(root: Path) -> set[str]:
    preferred = root / "README.md"
    candidates = (
        [preferred]
        if preferred.is_file() and not preferred.is_symlink()
        else sorted(
            path
            for path in root.glob("README*")
            if path.is_file() and not path.is_symlink()
        )
    )
    if not candidates:
        return set()
    text = candidates[0].read_text(encoding="utf-8", errors="ignore")
    return {
        match.group(1).strip().lower()
        for match in re.finditer(r"^#{1,6}\s+(.+)$", text, re.MULTILINE)
    }


def _manifest_commands(root: Path) -> dict[str, bool]:
    result = {"test_command": False, "lint_command": False}
    package = root / "package.json"
    if package.is_file():
        try:
            scripts = json.loads(package.read_text(encoding="utf-8")).get("scripts", {})
            result["test_command"] = isinstance(scripts, dict) and "test" in scripts
            result["lint_command"] = isinstance(scripts, dict) and any(
                name in scripts for name in ("lint", "check")
            )
        except json.JSONDecodeError:
            pass
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        result["test_command"] = result["test_command"] or _exists(
            root, "tests/test*.py", "test_*.py"
        )
        result["lint_command"] = result["lint_command"] or any(
            name in pyproject.read_text(encoding="utf-8", errors="ignore")
            for name in ("ruff", "mypy", "pytest")
        )
    return result


def _dependency_evidence(root: Path) -> bool:
    if _exists(
        root,
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "poetry.lock",
        "uv.lock",
        "Pipfile.lock",
    ):
        return True
    # Python libraries normally publish compatible dependency ranges instead of
    # an application lock file; pyproject.toml is their reproducibility record.
    if (root / "pyproject.toml").is_file():
        return True
    package = root / "package.json"
    if package.is_file():
        try:
            parsed = json.loads(package.read_text(encoding="utf-8"))
            return not parsed.get("dependencies") and not parsed.get("devDependencies")
        except json.JSONDecodeError:
            return False
    return not _exists(root, "requirements*.txt", "Cargo.toml", "go.mod")


def audit_repository(root: Path) -> dict[str, Any]:
    """Score contributor onboarding and maintenance hygiene."""
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"{root} is not a repository directory")
    sections = _readme_sections(root)
    commands = _manifest_commands(root)
    checks = [
        (
            "RW001",
            "README",
            _exists(root, "README*"),
            12,
            "목적·설치·사용·지원 방법이 포함된 간결한 README를 추가하세요.",
        ),
        (
            "RW002",
            "오픈소스 라이선스",
            _exists(root, "LICENSE*", "COPYING*"),
            12,
            "OSI 승인 라이선스 파일을 추가하고 README에도 표시하세요.",
        ),
        (
            "RW003",
            "기여 안내",
            _exists(root, "CONTRIBUTING*", ".github/CONTRIBUTING*"),
            10,
            "개발 환경, 테스트, 리뷰 기준과 예제 데이터 정책을 문서화하세요.",
        ),
        (
            "RW004",
            "행동 강령",
            _exists(root, "CODE_OF_CONDUCT*", ".github/CODE_OF_CONDUCT*"),
            6,
            "커뮤니티 행동 강령과 집행 절차를 추가하세요.",
        ),
        (
            "RW005",
            "보안 정책",
            _exists(root, "SECURITY*", ".github/SECURITY*"),
            8,
            "취약점을 비공개로 신고하는 방법을 설명하세요.",
        ),
        (
            "RW006",
            "이슈 템플릿",
            _exists(root, ".github/ISSUE_TEMPLATE/*"),
            7,
            "버그와 기능 제안을 위한 이슈 양식을 추가하세요.",
        ),
        (
            "RW007",
            "Pull Request 템플릿",
            _exists(
                root, ".github/PULL_REQUEST_TEMPLATE*", ".github/pull_request_template*"
            ),
            6,
            "테스트·범위·보안 영향을 확인하는 PR 체크리스트를 추가하세요.",
        ),
        (
            "RW008",
            "지속적 통합",
            _exists(root, ".github/workflows/*.yml", ".github/workflows/*.yaml"),
            12,
            "최소 권한으로 push와 PR에서 테스트를 실행하세요.",
        ),
        (
            "RW009",
            "자동 테스트",
            _exists(root, "tests/*", "test/*", "__tests__/*"),
            10,
            "합성 예제를 사용하는 빠른 테스트를 추가하세요.",
        ),
        (
            "RW010",
            "의존성 재현 정보",
            _dependency_evidence(root),
            5,
            "애플리케이션은 잠금 파일을, 라이브러리는 명시적인 의존성 범위를 커밋하세요.",
        ),
        (
            "RW011",
            "설치·사용 문서",
            (
                any(
                    "install" in section
                    or "getting started" in section
                    or "설치" in section
                    for section in sections
                )
                and any(
                    "usage" in section or "run" in section or "사용" in section
                    for section in sections
                )
            ),
            7,
            "README에 분명한 설치 및 사용 제목을 추가하세요.",
        ),
        (
            "RW012",
            "실행 가능한 테스트 명령",
            commands["test_command"],
            5,
            "전체 테스트를 실행하는 하나의 명령을 문서화하세요.",
        ),
    ]
    results = [
        {
            "id": identifier,
            "name": name,
            "passed": passed,
            "weight": weight,
            "recommendation": recommendation,
        }
        for identifier, name, passed, weight, recommendation in checks
    ]
    score = sum(item["weight"] for item in results if item["passed"])
    grade = (
        "A"
        if score >= 90
        else "B"
        if score >= 75
        else "C"
        if score >= 60
        else "D"
        if score >= 40
        else "F"
    )
    return {
        "schema_version": 1,
        "repository": ".",
        "score": score,
        "grade": grade,
        "checks": results,
        "summary": {
            "passed": sum(item["passed"] for item in results),
            "total": len(results),
        },
    }


def render_issue(report: dict[str, Any]) -> str:
    missing = [check for check in report["checks"] if not check["passed"]]
    lines = [
        "# 신규 기여자 준비 상태 개선",
        "",
        f"RepoWelcome 점수: **{report['score']}/100 ({report['grade']})**",
        "",
        "이 체크리스트는 규칙 기반으로 생성되었습니다. 적용 전에 각 권고를 검토하세요.",
        "",
    ]
    lines.extend(
        f"- [ ] **{check['name']}** — {check['recommendation']}" for check in missing
    )
    if not missing:
        lines.append("- [x] 현재 RepoWelcome 검사를 모두 통과했습니다.")
    lines.extend(["", "RepoWelcome이 생성했습니다.", ""])
    return "\n".join(lines)
