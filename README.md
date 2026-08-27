# RepoWelcome

한국어 | [English](README.en.md)

RepoWelcome은 오픈소스 저장소가 첫 기여자를 맞을 준비가 되었는지 검사합니다. 커뮤니티 문서, CI, 테스트, 의존성 재현 정보, README 안내와 실행 가능한 테스트 명령을 점수화하고 개선 이슈 초안을 만듭니다. 애플리케이션은 잠금 파일을, Python 라이브러리는 명시적인 `pyproject.toml` 의존성 범위를 인정합니다.

## 설치 및 사용

```bash
git clone https://github.com/Kwondh0321/repowelcome.git
cd repowelcome
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install .
repowelcome .
repowelcome ../another-project --format json --output repowelcome.json
repowelcome . --format issue --output contributor-readiness.md
```

기본 CI 기준은 75점이며 `--minimum-score`로 변경할 수 있습니다.

RepoWelcome은 기여 경로가 문서에 존재하는지를 확인할 뿐 커뮤니티가 실제로 공정하고 환영하는지 판정하지 않습니다. 생성된 권고를 프로젝트 상황에 맞게 검토하고 수정해야 합니다.

## 개발

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
repowelcome . --minimum-score 0
```

## 라이선스

MIT
