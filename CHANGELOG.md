# 변경 기록 / Changelog

이 프로젝트는 [Keep a Changelog](https://keepachangelog.com/)의 구조와 [Semantic Versioning](https://semver.org/) 원칙을 따릅니다.

## [Unreleased]

### 한국어

- `README.en.md`보다 기본 `README.md`를 우선 평가해 저장소 첫 화면과 일치시켰습니다.
- Python 라이브러리가 애플리케이션 잠금 파일 대신 명시적 의존성 범위를 사용하는 정상적인 관행을 인정합니다.
- 보고서에서 머신 절대 경로를 제거하고 점수·출력 옵션을 검증합니다.
- 점수가 커뮤니티의 실제 환영 문화까지 판정하지 않는다는 한계를 분명히 했습니다.

### English

- Prefers the primary `README.md` over `README.en.md`, matching the repository landing experience.
- Recognizes explicit dependency ranges as normal reproducibility evidence for Python libraries rather than requiring an application lockfile.
- Removes machine-specific absolute paths and validates score and output options.
- Clarifies that a readiness score cannot measure the community's lived contributor experience.

### 검증 / Validation

- 4 regression tests, Ruff checks, clean wheel build and install, text/JSON/issue examples, invalid-score failure, and GitHub Actions.

[Unreleased]: https://github.com/Kwondh0321/repowelcome/compare/v0.1.0...HEAD
