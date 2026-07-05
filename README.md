# MyGlico Semantic

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21148858.svg?v=2)](https://doi.org/10.5281/zenodo.21148858)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

[Português](README.pt-br.md) | **English**

Coursework capstone for the **Semantic Web** discipline, covering the semantic slice of the MyGlico project.

This repository demonstrates:

- import of the raw dataset into MySQL;
- relational persistence of patients, raw records, and normalized measurements;
- the MYGV ontology;
- an R2RML/Juma mapping for RDF materialization;
- end-to-end validation across MySQL and GraphDB;
- academic presentation and report artifacts.

## Structure

```text
.
|-- alembic/                     # Migrations that instantiate the MySQL schema
|-- app/
|   |-- core/                    # Minimal configuration
|   |-- db/                      # SQLAlchemy engine and session
|   |-- models/                  # Relational entities used by the import
|   `-- services/uci_importer.py # UCI Diabetes importer
|-- artifacts/
|   |-- presentations/           # Presentations and the final Colab notebook
|   `-- reports/                 # Final report PDF when produced
|-- data/
|   `-- raw/                     # Raw artifacts included to ease evaluation
|-- mappings/
|   `-- myglico-core-r2rml-juma.ttl # R2RML mapping from MySQL to RDF
|-- ontology/
|   `-- mygv-dpo-extension.owl.ttl  # OWL ontology for the mygv: vocabulary
`-- scripts/
    `-- import_uci_dataset.py       # CLI to import the UCI Diabetes dataset
```

## Requirements

- Docker Desktop
- Python 3.12+
- MySQL via Docker Compose
- GraphDB to load the materialized RDF
- A Juma/R2RML distribution, if the RDF is regenerated outside this repository

## Instantiating MySQL and importing the dataset

Start MySQL only:

```powershell
docker compose up -d db
```

Install Python dependencies:

```powershell
pip install .
```

Apply migrations and import the UCI Diabetes dataset:

```powershell
python scripts/import_uci_dataset.py --skip-docker
```

Or run everything through the `importer` service:

```powershell
docker compose up importer
```

The import is idempotent by default: if dataset records already exist in `glucose_record_sources`, it reuses the last batch and avoids a full reload.

To force a new import:

```powershell
python scripts/import_uci_dataset.py --skip-docker --force-import
```

Use `--force-import` carefully, as it may duplicate records if the database was not cleared first.

## The `data/raw` folder

To ease evaluation, the repository ships a few prebuilt artifacts in `data/raw/`:

```text
data/raw/
|-- dump-database.sql
|-- myglico-rdf.ttl
`-- uci_diabetes.zip
```

- `myglico-rdf.ttl`: RDF base extracted by R2RML from the mapping authored in Juma and exported with the 2024 jar of [`chrdebru/r2rml-distributions`](https://github.com/chrdebru/r2rml-distributions).
- `dump-database.sql`: dump of the database populated by the Python UCI Diabetes import script, after migrations were applied.
- `uci_diabetes.zip`: the raw dataset downloaded and used as the load source.

These files were added to simplify inspection and grading. Even so, running the project through the pipeline described in this README reproduces the same artifacts and the same results.

## Ontology

The ontology lives in:

```text
ontology/mygv-dpo-extension.owl.ttl
```

It models the MYGV vocabulary used to represent patients, glucose measurements, raw records, and data sources.

## R2RML mapping

The main mapping lives in:

```text
mappings/myglico-core-r2rml-juma.ttl
```

As a project annex, the evolution of the Juma platform used in this work is available at [`cale-minds/juma.git`](https://github.com/cale-minds/juma.git).

It materializes the bridge:

```text
Patient -> GlucoseMeasurement -> RawRecord -> DataSource
```

## Presentation artifacts

The presentation artifacts live in:

```text
artifacts/presentations/
```

Current files:

| Order | File | Role |
| ---: | --- | --- |
| 01 | `01-myglico-semantic-overview.pptx` | Initial presentation of the semantic slice. |
| 02 | `02-myglico-semantic-pipeline.pptx` | Presentation of the technical pipeline, R2RML, and GraphDB. |
| 03 | `03-myglico-end-to-end-tracking-colab.ipynb` | Final Colab/notebook presentation with the end-to-end validation. |

The final notebook answers the question:

> Can a measurement queried via SPARQL prove, end to end, that value, timestamp, clinical class, and the pointer to the exact line of the raw UCI file match the relational record in MySQL?

It compares:

- patient and measurement counts in MySQL;
- patient and measurement counts in GraphDB;
- measurements of `Paciente UCI 01` on `1991-04-29`;
- UUIDs of `GlucoseMeasurement` and `RawRecord`;
- the exact UCI file line via `sourceRecordId`, such as `data-01:50`.

## Final report

Download the final PDF report: [MyGlico_WebSemantica_RelatorioFinal.pdf](artifacts/reports/MyGlico_WebSemantica_RelatorioFinal.pdf)

## Citation

If you use this repository, cite it using the [`CITATION.cff`](CITATION.cff) file — GitHub renders a **"Cite this repository"** button from it — or via the archived Zenodo record: **10.5281/zenodo.21148858** (concept DOI, always resolving to the latest release; version v0.1.0 is `10.5281/zenodo.21148859`). See the [Zenodo record](https://doi.org/10.5281/zenodo.21148858).

## License

Apache License 2.0 — see [`LICENSE`](LICENSE). The UCI Diabetes dataset used as a base has its own terms of use; confirm the official citation and license at `archive.ics.uci.edu`.
