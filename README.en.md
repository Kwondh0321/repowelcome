# RepoWelcome

[한국어](README.md) | English | [Changelog / 변경 기록](CHANGELOG.md)

RepoWelcome audits whether an open-source repository is ready for a first-time contributor. It scores community documents, CI, tests, dependency reproducibility, README onboarding, and executable test commands, and can generate an improvement issue draft.

## Install and run

```bash
git clone https://github.com/Kwondh0321/repowelcome.git
cd repowelcome
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install .
repowelcome .
repowelcome ../another-project --format json --output reports/repowelcome.json
repowelcome . --format issue --output contributor-readiness.md
```

The default CI threshold is 75. `--minimum-score` accepts values from 0 to 100. Application lock files and explicit Python library dependency ranges are both recognized as valid reproducibility evidence.

RepoWelcome confirms that an onboarding path exists; it cannot determine whether a community is actually fair or welcoming. Review generated recommendations in project context.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
repowelcome . --minimum-score 0
```

Licensed under MIT.
