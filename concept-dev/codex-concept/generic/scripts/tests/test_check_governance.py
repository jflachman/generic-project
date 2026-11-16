from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "check-governance.py"
FIXTURE = ROOT / "scripts" / "tests" / "fixtures" / "valid"


def copy_fixture(tmp_path: Path) -> tuple[Path, Path]:
    product = tmp_path / "generic"
    dev = tmp_path / "generic-dev"
    shutil.copytree(FIXTURE / "product", product)
    shutil.copytree(FIXTURE / "dev", dev)
    return product, dev


def run_check(product: Path, dev: Path, *checks: str) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        str(SCRIPT),
        "--product-root",
        str(product),
        "--dev-root",
        str(dev),
        "--today",
        "2026-08-20",
    ]
    for check in checks:
        command.extend(["--check", check])
    return subprocess.run(command, text=True, capture_output=True, check=False)


def assert_fails_with(product: Path, dev: Path, check: str) -> None:
    result = run_check(product, dev, check)
    assert result.returncode == 1
    assert check in result.stderr


class GovernanceCheckTests(unittest.TestCase):
    def with_fixture(self) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
        temp = tempfile.TemporaryDirectory()
        product, dev = copy_fixture(Path(temp.name))
        return temp, product, dev

    def test_valid_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            result = run_check(product, dev)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_line_byte_budget_failure_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            (product / "CLAUDE.md").write_text("# Product\n" + ("line\n" * 205), encoding="utf-8")
            assert_fails_with(product, dev, "line-byte-budgets")

    def test_relative_link_failure_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            (product / "CLAUDE.md").write_text("[missing](missing.md)\n", encoding="utf-8")
            assert_fails_with(product, dev, "relative-links")

    def test_section_length_failure_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            (dev / "PROTOCOL.md").write_text("# Protocol\n\n## Long\n" + ("body\n" * 151), encoding="utf-8")
            assert_fails_with(product, dev, "section-length")

    def test_schema_failure_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            (dev / "issues" / "bugs" / "BUG-001.yml").write_text("id: BUG-001\n", encoding="utf-8")
            assert_fails_with(product, dev, "schemas")

    def test_generated_file_failure_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            (dev / "QUEUE.md").write_text("# Hand Edited\n", encoding="utf-8")
            assert_fails_with(product, dev, "generated-files")

    def test_sync_pin_failure_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            (product / "governance" / "contracts" / "SYNC.yml").write_text(
                "last_checked: 2026-06-01\npaths: []\n",
                encoding="utf-8",
            )
            assert_fails_with(product, dev, "sync-pins")

    def test_dev_ignored_failure_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            (Path(tmp) / ".gitignore").write_text("generic-dev/\n", encoding="utf-8")
            assert_fails_with(product, dev, "dev-not-ignored")

    def test_closed_prompt_without_report_failure_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            (dev / "build-reports" / "20260820-seed.md").unlink()
            assert_fails_with(product, dev, "closed-prompts-have-reports")

    def test_mutable_constitution_failure_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            (product / "CLAUDE.md").write_text("# Product\n\n## Current phase\nSetup\n", encoding="utf-8")
            assert_fails_with(product, dev, "mutable-state-in-constitution")

    def test_amendment_drift_failure_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            unit = product / "governance" / "units" / "UNIT-001-core.md"
            unit.write_text(unit.read_text(encoding="utf-8") + "\n## Amendment\nThe opposite rule now applies.\n", encoding="utf-8")
            assert_fails_with(product, dev, "no-amendment-drift")

    def test_issue_type_prefix_folder_failure_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            product, dev = copy_fixture(Path(tmp))
            issue = dev / "issues" / "bugs" / "BUG-001.yml"
            issue.write_text(issue.read_text(encoding="utf-8").replace("type: bug", "type: gap"), encoding="utf-8")
            assert_fails_with(product, dev, "issue-type-prefix-folder")


if __name__ == "__main__":
    unittest.main()
