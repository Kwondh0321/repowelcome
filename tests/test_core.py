import tempfile
import unittest
from pathlib import Path

from repowelcome.cli import main
from repowelcome.core import audit_repository, render_issue


class RepoWelcomeTests(unittest.TestCase):
    def test_scores_minimal_repository(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text(
                "# Project\n\n## Install\n\n## Usage\n", encoding="utf-8"
            )
            report = audit_repository(root)
            self.assertTrue(
                next(check for check in report["checks"] if check["id"] == "RW001")[
                    "passed"
                ]
            )
            self.assertFalse(
                next(check for check in report["checks"] if check["id"] == "RW002")[
                    "passed"
                ]
            )
            self.assertLess(report["score"], 75)

    def test_issue_contains_missing_actions(self):
        with tempfile.TemporaryDirectory() as temporary:
            report = audit_repository(Path(temporary))
            issue = render_issue(report)
            self.assertIn("- [ ] **README**", issue)
            self.assertIn("RepoWelcome 점수", issue)

    def test_cli_threshold(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.assertEqual(1, main([temporary, "--minimum-score", "100"]))

    def test_prefers_primary_readme_and_accepts_library_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.en.md").write_text("# English only\n", encoding="utf-8")
            (root / "README.md").write_text(
                "# 프로젝트\n\n## 설치\n\n## 사용\n", encoding="utf-8"
            )
            (root / "pyproject.toml").write_text(
                "[project]\nname='demo'\nversion='0.1.0'\n", encoding="utf-8"
            )
            report = audit_repository(root)
            checks = {check["id"]: check for check in report["checks"]}
            self.assertTrue(checks["RW010"]["passed"])
            self.assertTrue(checks["RW011"]["passed"])
            self.assertEqual(".", report["repository"])


if __name__ == "__main__":
    unittest.main()
