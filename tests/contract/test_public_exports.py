"""Contract tests: public export surface regression guard."""

import scanq_shared.enums as enums_module
import scanq_shared.schemas as schemas_module
from scanq_shared.clients import TrainingStudioClient
from scanq_shared.enums import MediaComposeStatus, MediaType
from scanq_shared.schemas import (
    ErrorEnvelope,
    MediaComposeRequest,
    MediaComposeResponse,
)


def test_new_media_compose_exports_are_public():
    assert "MediaType" in enums_module.__all__
    assert "MediaComposeStatus" in enums_module.__all__
    assert "MediaComposeRequest" in schemas_module.__all__
    assert "MediaComposeResponse" in schemas_module.__all__
    assert "ErrorEnvelope" in schemas_module.__all__


def test_public_symbols_import_and_client_method_exists():
    assert MediaType.FLOOR_PLAN.value == "floor_plan"
    assert MediaComposeStatus.COMPLETE.value == "complete"
    assert MediaComposeRequest.__name__ == "MediaComposeRequest"
    assert MediaComposeResponse.__name__ == "MediaComposeResponse"
    assert ErrorEnvelope.__name__ == "ErrorEnvelope"
    assert hasattr(TrainingStudioClient, "compose_media")
