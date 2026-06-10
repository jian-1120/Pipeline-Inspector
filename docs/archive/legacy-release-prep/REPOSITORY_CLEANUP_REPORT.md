# Repository Cleanup Report

## Fixed Project Root

`C:\Users\简某\Desktop\AI\PL总\Pipeline-Inspector`

All cleanup actions were performed in this directory only.

## KEEP

Core long-term documentation:

- `README.md`
- `CLAUDE.md`
- `DEVELOPMENT_STATUS.md`
- `ROADMAP.md`
- `INSTALLATION.md`

Product, evidence, and specification documents:

- `MVP_CHECKLIST.md`
- `MVP_EVIDENCE_MAPPING.md`
- `MVP_REVIEW_REPORT.md`
- `TOP_FAILURES.md`
- `ARCHITECTURE_MVP_V1.md`
- `IMPLEMENTATION_SPEC_V1.md`
- `SCAFFOLD_PLAN_V1.md`

Project source, tests, and research directories:

- `pipeline_inspector/`
- `tests/`
- `research/`
- `evidence/`
- `prd/`
- `architecture/`
- `roadmap/`

Current valid runtime package:

- `PipelineInspector_Runtime_Check03_v0.1.1.zip`

Cleanup report:

- `REPOSITORY_CLEANUP_REPORT.md`

## ARCHIVE

Created:

- `docs/archive/`

Moved runtime reports into archive:

- `docs/archive/RUNTIME_VALIDATION.md`
- `docs/archive/RUNTIME_TEST_CHECK03.md`
- `docs/archive/RUNTIME_BUG_REPORT.md`
- `docs/archive/PACKAGE_NOTES_CHECK03.md`

## DELETE

Deleted temporary path repair reports:

- `PATH_MIGRATION_REPORT.md`
- `PATH_CLEAN_REPORT.md`

Deleted obsolete runtime package from the correct repository:

- `PipelineInspector_Scaffold_v0.1.zip`

## Deprecated ZIP Status

Deprecated:

- `PipelineInspector_Scaffold_v0.1.zip`

Current:

- `PipelineInspector_Runtime_Check03_v0.1.1.zip`

## Documents p Check

Checked:

- `C:\Users\简某\Documents\p`
- `C:\Users\简某\Documents\p\Pipeline-Inspector`

`Documents\p` was not deleted.

Reason:

- `C:\Users\简某\Documents\p\LOCAL_REPO_STATUS.md` exists only in `Documents\p`.
- `C:\Users\简某\Documents\p\MVP_CHECKLIST.md` differs from the correct repository's `MVP_CHECKLIST.md`.
- `C:\Users\简某\Documents\p\Pipeline-Inspector` still has same-path files with different content from the correct repository.

After cleanup, the wrong repository still has root-level runtime files because the correct repository moved those files into `docs/archive/`:

- `PACKAGE_NOTES_CHECK03.md`
- `PipelineInspector_Scaffold_v0.1.zip`
- `RUNTIME_BUG_REPORT.md`
- `RUNTIME_TEST_CHECK03.md`
- `RUNTIME_VALIDATION.md`

There are also 32 same-path files with different content between the wrong repository and the correct repository.

## Verification Summary

- `docs/archive/` exists.
- Four runtime report files are archived.
- `PipelineInspector_Scaffold_v0.1.zip` is removed from the correct repository.
- `PipelineInspector_Runtime_Check03_v0.1.1.zip` is retained in the correct repository.
- `PATH_MIGRATION_REPORT.md` is removed from the correct repository.
- `PATH_CLEAN_REPORT.md` is removed from the correct repository.
- `Documents\p` still exists and was not deleted.

## Commit

Commit message:

`Clean repository runtime artifacts`
