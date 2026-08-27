# RepoWelcome

RepoWelcome audits how ready an open-source repository is for a first-time contributor. It checks community health files, CI, tests, lockfiles, README guidance, and a runnable test command, then produces a weighted score or a ready-to-file improvement issue.

## Run

```bash
python -m pip install -e .
repowelcome .
repowelcome ../another-project --format json --output repowelcome.json
repowelcome . --format issue --output contributor-readiness.md
```

The default CI threshold is 75/100 and can be changed with `--minimum-score`.

## Philosophy

RepoWelcome checks whether expected contributor paths exist, not whether a community is actually welcoming or governance is fair. Maintainers should review generated recommendations, adapt templates to their project, respond kindly to issues, and make contribution decisions transparently.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
repowelcome . --minimum-score 0
```

## License

MIT
