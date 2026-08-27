# RepoWelcome

RepoWelcome은 오픈소스 저장소가 첫 기여자를 맞을 준비가 되었는지 검사합니다. 커뮤니티 문서, CI, 테스트, 잠금 파일, README 안내와 실행 가능한 테스트 명령을 점수화하고 개선 이슈 초안을 만듭니다.

## 설치 및 사용

```bash
python -m pip install -e .
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

