# Repository Guidelines

## Project Structure & Module Organization

MyGlico Semantic is a Python 3.12 Semantic Web coursework deliverable: it imports
the public UCI Diabetes dataset into MySQL and materializes an RDF layer via the
MYGV ontology and an R2RML mapping. `README.md` is the canonical overview; read it
before changing behavior.

- `app/` — backend: `app/core/` (config), `app/db/` (SQLAlchemy engine/session),
  `app/models/` (relational entities), `app/services/uci_importer.py` (importer).
- `alembic/` — migrations that instantiate the MySQL schema.
- `scripts/import_uci_dataset.py` — idempotent dataset import entry point.
- `ontology/` — MYGV ontology (`mygv-dpo-extension.owl.ttl`) and examples.
- `mappings/` — R2RML mapping (`myglico-core-r2rml-juma.ttl`).
- `data/raw/` — prebuilt artifacts for evaluation (dataset zip, SQL dump, RDF).
- `artifacts/presentations/` — slides and the final end-to-end Colab notebook;
  `artifacts/reports/` — the final PDF report.

## Build, Test, and Development Commands

```powershell
docker compose up -d db                                     # MySQL only
pip install .                                               # install from pyproject.toml
python scripts/import_uci_dataset.py --skip-docker          # migrate + import (idempotent)
python scripts/import_uci_dataset.py --skip-docker --force-import   # force a fresh import
docker compose up importer                                  # run the whole import via Docker
```

Load `data/raw/myglico-rdf.ttl` into GraphDB (named graph
`mygv-dpo-extension`) to reproduce the SPARQL validation.

## Coding Style & Naming Conventions

Follow the existing style: 4-space indentation, type hints where useful, and
concise docstrings. Use `snake_case` for functions/variables and `UPPER_CASE`
for constants. Keep IRIs, ontology terms, and R2RML templates explicit and stable
— they are part of the reproducible instrument and must not change silently.

## Testing & Validation Guidelines

The import is idempotent; re-running must not duplicate `glucose_record_sources`
batches. After changes to the importer, ontology, or mapping, regenerate the RDF
and re-run the end-to-end check (MySQL count == GraphDB count; a measurement
resolves by `sourceRecordId` to the same UUID, value, timestamp, and clinical
class). The final Colab notebook in `artifacts/presentations/` is the reference
validation.

## Commit & Pull Request Guidelines

Commits use conventional prefixes such as `feat:`, `fix:`, and `docs:` with a
scoped, imperative summary — for example `docs: add citation and license`.

Pull requests should summarize behavior changes, commands run, and artifacts
changed.

### AI-assisted contributions

When a change is co-authored with an AI assistant, attribute it in the commit
message with a trailer so the collaboration is transparent and appears in the
GitHub contributor list:

```
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Reproducibility Notes

Preserve the traceability chain `RawRecord -> GlucoseMeasurement -> Patient` and
the `sourceRecordId` anchor to the exact UCI source line. Do not commit secrets
such as `.env` or database credentials.
