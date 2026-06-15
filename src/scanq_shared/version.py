"""Version information for scanq-shared."""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

__author__ = "Archanaut Pty Ltd"
__license__ = "Proprietary"
__copyright__ = "Copyright © 2026 Archanaut Pty Ltd. All rights reserved."

# ---------------------------------------------------------------------------
# Compatibility constants (Phase 1)
# ---------------------------------------------------------------------------

# The release that introduced the shared Phase 1 contract surface.
# Consumers must depend on >= this version to use shared schemas/clients.
PHASE1_RELEASE = "1.0.0"

# Minimum compatible consumer package version.
# Contracts introduced in PHASE1_RELEASE are guaranteed stable for consumers
# on MIN_CONSUMER_VERSION or higher.
MIN_CONSUMER_VERSION = "1.0.0"

# Number of releases consumers are given to complete migration before legacy
# dual-support paths are removed.  Applies per consumer repository.
DUAL_SUPPORT_WINDOW = 1

# Human-readable compatibility note surfaced in release notes.
COMPATIBILITY_NOTE = (
    f"scanq-shared >= {PHASE1_RELEASE} introduces the Phase 1 shared contract "
    f"surface.  Consumers have {DUAL_SUPPORT_WINDOW} release window to migrate "
    "from local contract definitions to shared imports."
)
