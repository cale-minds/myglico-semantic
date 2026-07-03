# MyGlico Semantic

[![DOI](https://img.shields.io/badge/DOI-pendente%20(Zenodo)-lightgrey.svg)](#citação)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

<!--
  Após criar o release no GitHub e o Zenodo cunhar o DOI, troque o badge acima por:
  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXXX)
-->

Repositório de conclusão da disciplina de **Web Semântica**, com o recorte semântico do projeto MyGlico.

O objetivo deste repositório é demonstrar:

- importação do dataset bruto para MySQL;
- persistência relacional dos pacientes, registros brutos e medições normalizadas;
- ontologia MYGV;
- mapping R2RML/Juma para materialização RDF;
- validação end-to-end em MySQL e GraphDB;
- artefatos acadêmicos de apresentação e relatório.

## Estrutura

```text
.
|-- alembic/                     # Migrations para instanciar o schema MySQL
|-- app/
|   |-- core/                    # Configuração mínima
|   |-- db/                      # Engine e sessão SQLAlchemy
|   |-- models/                  # Entidades relacionais usadas pelo import
|   `-- services/uci_importer.py # Importador UCI Diabetes
|-- artifacts/
|   |-- presentations/           # Apresentações e notebook final em formato Colab
|   `-- reports/                 # PDF do relatório final quando produzido
|-- data/
|   `-- raw/                     # Artefatos brutos incluídos para facilitar a avaliação
|-- mappings/
|   `-- myglico-core-r2rml-juma.ttl
|-- ontology/
|   |-- mygv-dpo-extension.owl.ttl
|   `-- mygv-dpo-extension.examples.ttl
`-- scripts/
    `-- import_uci_dataset.py
```

## Requisitos

- Docker Desktop
- Python 3.12+
- MySQL via Docker Compose
- GraphDB para carregar o RDF materializado
- Distribuição Juma/R2RML, caso o RDF seja regenerado fora deste repositório

## Como instanciar o MySQL e importar o dataset

Subir apenas o MySQL:

```powershell
docker compose up -d db
```

Instalar dependências Python:

```powershell
pip install .
```

Aplicar migrations e importar o dataset UCI Diabetes:

```powershell
python scripts/import_uci_dataset.py --skip-docker
```

Ou executar tudo pelo serviço `importer`:

```powershell
docker compose up importer
```

O import é idempotente por padrão: se registros de dataset já existirem em `glucose_record_sources`, ele reutiliza o último batch e evita uma nova carga completa.

Para forçar nova importação:

```powershell
python scripts/import_uci_dataset.py --skip-docker --force-import
```

Use `--force-import` com cuidado, pois ele pode duplicar registros caso o banco não tenha sido limpo antes.

## Pasta `data/raw`

Para facilitar a avaliação do projeto, o repositório inclui alguns artefatos já gerados em `data/raw/`:

```text
data/raw/
|-- dump-database.sql
|-- myglico-rdf.ttl
`-- uci_diabetes.zip
```

- `myglico-rdf.ttl`: base RDF extraída pelo R2RML a partir do mapping construído no Juma e exportado usando o jar da versão de 2024 do projeto [`chrdebru/r2rml-distributions`](https://github.com/chrdebru/r2rml-distributions).
- `dump-database.sql`: dump da base populada pelo script Python de importação do UCI Diabetes, após a aplicação das migrations.
- `uci_diabetes.zip`: dataset bruto baixado e usado como origem da carga.

Esses arquivos foram adicionados para simplificar a inspeção e a avaliação do trabalho. Ainda assim, executando o projeto com o pipeline descrito neste README, é possível reproduzir os mesmos artefatos e chegar aos mesmos resultados.

## Ontologia

A ontologia fica em:

```text
ontology/mygv-dpo-extension.owl.ttl
```

Ela modela o vocabulário MYGV usado para representar pacientes, medições glicêmicas, registros brutos e fontes de dados.

## Mapping R2RML

O mapping principal fica em:

```text
mappings/myglico-core-r2rml-juma.ttl
```

Como anexo ao projeto, a evolução da plataforma Juma usada no trabalho está disponibilizada em [`cale-minds/juma.git`](https://github.com/cale-minds/juma.git).

Ele materializa a ponte:

```text
Patient -> GlucoseMeasurement -> RawRecord -> DataSource
```

## Artefatos de apresentação

Os artefatos de apresentação ficam em:

```text
artifacts/presentations/
```

Arquivos atuais:

| Ordem | Arquivo | Papel |
| ---: | --- | --- |
| 01 | `01-myglico-semantic-overview.pptx` | Apresentação inicial do recorte semântico. |
| 02 | `02-myglico-semantic-pipeline.pptx` | Apresentação do pipeline técnico, R2RML e GraphDB. |
| 03 | `03-myglico-end-to-end-tracking-colab.ipynb` | Apresentação final em formato Colab/notebook com a validação end-to-end. |

O notebook final responde a pergunta:

> Uma medição consultada via SPARQL consegue comprovar, de ponta a ponta, que valor, horário, classe clínica e ponteiro para a linha exata do arquivo bruto UCI batem com o registro relacional no MySQL?

Ele compara:

- contagem de pacientes e medições no MySQL;
- contagem de pacientes e medições no GraphDB;
- medições do `Paciente UCI 01` em `1991-04-29`;
- UUIDs de `GlucoseMeasurement` e `RawRecord`;
- linha exata do arquivo UCI via `sourceRecordId`, como `data-01:50`.

## Relatório final

O relatório final em PDF será colocado em:

```text
artifacts/reports/
```

como:

```text
MyGlico_WebSemantica_RelatorioFinal.pdf
```

## Citação

Se você usar este repositório, cite-o usando o arquivo [`CITATION.cff`](CITATION.cff) — o GitHub renderiza um botão **"Cite this repository"** a partir dele. Após arquivar um release no Zenodo, adicione o DOI ao badge no topo e descomente o bloco `identifiers:` no `CITATION.cff`.

## Licença

Apache License 2.0 — veja [`LICENSE`](LICENSE). O dataset UCI Diabetes usado como base possui seus próprios termos de uso; confirme a citação e a licença oficiais em `archive.ics.uci.edu`.
