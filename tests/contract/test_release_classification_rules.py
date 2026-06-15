"""Contract tests: SemVer release classification rules.

Copyright © 2026 Archanaut Pty Ltd. All rights reserved.
Licensed under the Archanaut Proprietary License.

Validates that the compatibility classification matrix in research.md
covers the required change types and that version constants in
version.py follow SemVer format expectations.
"""

import os
import re

import pytest

from scanq_shared.version import (
    DUAL_SUPPORT_WINDOW,
    MIN_CONSUMER_VERSION,
    PHASE1_RELEASE,
    __version__,
    __version_info__,
)


RESEARCH_MD = os.path.join(
    os.path.dirname(__file__),
    "../../specs/001-phase1-shared-contracts/research.md",
)

SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")

REQUIRED_CHANGE_TYPES = [
    "MINOR",
    "MAJOR",
    "PATCH",
    "dual-support",
]


class TestVersionConstants:
    def test_version_is_semver(self):
        assert SEMVER_PATTERN.match(__version__), (
            f"__version__ '{__version__}' must be a valid SemVer string (X.Y.Z)"
        )

    def test_version_info_matches_version_string(self):
        major, minor, patch = __version_info__
        assert __version__ == f"{major}.{minor}.{patch}"

    def test_phase1_release_is_semver(self):
        assert SEMVER_PATTERN.match(PHASE1_RELEASE)

    def test_min_consumer_version_is_semver(self):
        assert SEMVER_PATTERN.match(MIN_CONSUMER_VERSION)

    def test_dual_support_window_is_positive_int(self):
        assert isinstance(DUAL_SUPPORT_WINDOW, int)
        assert DUAL_SUPPORT_WINDOW >= 1

    def test_dual_support_window_is_one_release(self):
        assert DUAL_SUPPORT_WINDOW == 1, (
            "Per research.md Decision 3, dual-support window must be exactly "
            "one release. Update version.py if this policy changes."
        )


class TestCompatibilityMatrixPresence:
    def test_research_md_exists(self):
        assert os.path.isfile(RESEARCH_MD)

    def test_compatibility_matrix_section_present(self):
        content = open(RESEARCH_MD).read()
        assert "Compatibility Classification Matrix" in content

    @pytest.mark.parametrize("change_type", REQUIRED_CHANGE_TYPES)
    def test_required_change_type_documented(self, change_type):
        content = open(RESEARCH_MD).read()
        assert change_type in content, (
            f"Compatibility matrix must document '{change_type}' changes"
        )

    def test_matrix_has_semver_bump_column(self):
        content = open(RESEARCH_MD).read()
        assert "SemVer Bump" in content

    def test_matrix_has_dual_support_column(self):
        content = open(RESEARCH_MD).read()
        assert "Dual-Support" in content
