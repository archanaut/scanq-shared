# Data Model: ScanQ Shared Phase 1

## Entity: SharedContractModel

- Purpose: Canonical cross-repository domain object representation.
- Fields:
  - `entity_name` (str, required): canonical model name.
  - `version` (str, required): contract version label tied to package release.
  - `required_fields` (list[str], required): fields that must be present.
  - `optional_fields` (list[str], optional): additive compatibility fields.
  - `deprecation_notes` (str, optional): guidance for retiring legacy fields.
- Validation rules:
  - `entity_name` must be stable and unique within the package.
  - `required_fields` cannot overlap with `optional_fields`.

## Entity: SharedSchema

- Purpose: Request/response payload shape definition for typed client and consumers.
- Fields:
  - `schema_name` (str, required)
  - `direction` (enum: request|response, required)
  - `fields` (list[SchemaField], required)
  - `error_mapping_profile` (str, optional)
- Validation rules:
  - Every schema field must define type and nullability.
  - Response schemas must map to a typed model or standardized error schema.

## Entity: SharedEnum

- Purpose: Controlled values used by contracts and typed client behavior.
- Fields:
  - `enum_name` (str, required)
  - `values` (list[str], required)
  - `default` (str, optional)
- Validation rules:
  - `values` must be unique and non-empty.
  - `default` must exist in `values` when defined.

## Entity: TrainingStudioOperation

- Purpose: Typed operation mapping for one fixed Phase 1 endpoint.
- Fields:
  - `operation_id` (str, required)
  - `endpoint_path` (str, required)
  - `http_method` (str, required)
  - `request_schema` (str, required)
  - `response_schema` (str, required)
  - `error_schema` (str, required)
  - `in_phase1_inventory` (bool, required)
- Validation rules:
  - `in_phase1_inventory` must be true for all Phase 1 operations.
  - Request/response schema references must exist in shared schemas.

## Entity: MigrationWorkItem

- Purpose: Actionable migration step for a consumer repository.
- Fields:
  - `repository` (enum: scanq-accreditation|scanq-training-studio, required)
  - `step_id` (str, required)
  - `description` (str, required)
  - `owner` (str, required)
  - `dual_support_release` (str, required)
  - `exit_criteria` (list[str], required)
  - `status` (enum: planned|in_progress|validated|completed, required)
- Validation rules:
  - `dual_support_release` must represent a single release window.
  - `status` can move only forward in the defined lifecycle.

## Relationships

- `TrainingStudioOperation` references one `SharedSchema` for request and one for response.
- `SharedSchema` may embed `SharedEnum` values for constrained fields.
- `MigrationWorkItem` references affected `SharedContractModel` and `TrainingStudioOperation` items.

## State Transitions

### MigrationWorkItem

- `planned` -> `in_progress` -> `validated` -> `completed`
- Invalid transitions are rejected (for example, `planned` -> `completed` directly).
