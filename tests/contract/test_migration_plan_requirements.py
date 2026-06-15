"""Contract tests: Migration plan field validation.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

Validates that migration runbook documents contain all required
sections and fields as specified by the migration plan contract.
These tests act as a structural linter for human-authored runbooks.
"""

import os

import pytest


MIGRATIONS_DIR = os.path.join(
    os.path.dirname(__file__),
    "../../specs/001-phase1-shared-contracts/migrations",
)

REQUIRED_RUNBOOK_SECTIONS = [
    "Pre-migration state",
    "Import replacement",
    "Dry-run",
    "Dual-support",
    "Cutover",
]

EXPECTED_RUNBOOKS = [
    "scanq-training-studio.md",
    "scanq-accreditation.md",
]


class TestMigrationRunbookPresence:
    def test_migrations_directory_exists(self):
        assert os.path.isdir(MIGRATIONS_DIR), (
            f"Migrations directory not found at {MIGRATIONS_DIR}"
        )

    def test_readme_exists(self):
        readme = os.path.join(MIGRATIONS_DIR, "README.md")
        assert os.path.isfile(readme), "migrations/README.md must exist"

    def test_readme_lists_expected_runbooks(self):
        readme = os.path.join(MIGRATIONS_DIR, "README.md")
        content = open(readme).read()
        for runbook in EXPECTED_RUNBOOKS:
            assert runbook in content, (
                f"README.md must list expected runbook '{runbook}'"
            )

    @pytest.mark.parametrize("runbook", EXPECTED_RUNBOOKS)
    def test_runbook_exists(self, runbook):
        path = os.path.join(MIGRATIONS_DIR, runbook)
        assert os.path.isfile(path), (
            f"Expected migration runbook '{runbook}' not found in migrations/. "
            "Run T034/T035 to create it."
        )

    @pytest.mark.parametrize("runbook", EXPECTED_RUNBOOKS)
    def test_runbook_has_required_sections(self, runbook):
        path = os.path.join(MIGRATIONS_DIR, runbook)
        if not os.path.isfile(path):
            pytest.skip(f"{runbook} not yet created")
        content = open(path).read()
        for section in REQUIRED_RUNBOOK_SECTIONS:
            assert section.lower() in content.lower(), (
                f"Runbook '{runbook}' is missing required section: '{section}'"
            )
