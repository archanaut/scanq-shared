from scanq_shared.types import ArtifactManifest, ExecutionContext


def test_artifact_manifest_shape():
    artifact: ArtifactManifest = {
        "artifact_id": "a-1",
        "artifact_type": "report",
        "uri": "s3://bucket/key",
    }
    assert artifact["artifact_type"] == "report"


def test_execution_context_shape():
    context: ExecutionContext = {
        "run_id": "run-1",
        "project_id": "proj-1",
        "environment_id": "env-1",
        "initiated_by": "ci",
    }
    assert context["run_id"] == "run-1"

