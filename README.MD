# ETL Data Pipeline

A production-style ETL (Extract → Transform → Load) pipeline built in pure Python using Object-Oriented Programming principles. Designed as a hands-on learning project covering all four OOP pillars — encapsulation, inheritance, polymorphism, and abstraction — in a real data engineering context.

---

## Project structure

```
data_pipeline/
├── data/
│   ├── raw/
│   │   ├── students_raw.csv       # messy input data (CSV)
│   │   └── students_raw.json      # messy input data (JSON)
│   └── output/
│       ├── students_clean.csv     # cleaned output (CSV)
│       └── students_clean.json    # cleaned output (JSON)
├── logs/
│   └── Student_Data_Pipeline_YYYYMMDD_HHMMSS.log
├── pipeline/
│   ├── __init__.py
│   ├── extractor.py               # Stage 1 — reads raw data
│   ├── transformer.py             # Stage 2 — cleans and enriches data
│   ├── loader.py                  # Stage 3 — writes clean output
│   └── pipeline.py                # Stage 4 — orchestrates all three stages
├── utils/
│   ├── __init__.py
│   └── logger.py                  # Stage 5 — structured timestamped logging
├── tests/
│   └── test_pipeline.py           # pipeline integration test
└── main.py                        # Stage 6 — interactive entry point
```

---

## Quickstart

**1. Clone the project and navigate to the root:**

```bash
cd data_pipeline
```

**2. No external dependencies required — pure Python 3.8+**

**3. Run the interactive menu:**

```bash
python main.py
```

**4. Or run the pipeline directly from code:**

```bash
python -m tests.test_pipeline
```

> Always run from the project root (`data_pipeline/`) using `python -m` to avoid relative path issues.

---

## How it works

The pipeline follows the classic ETL pattern — three independent stages chained together by a single `Pipeline` orchestrator:

```
Raw file (CSV or JSON)
        ↓
  [ Extractor ]   — reads rows into a list of dicts
        ↓
[ Transformer ]   — cleans, validates, and enriches each row
        ↓
   [ Loader ]     — writes clean rows to CSV, JSON, or both
        ↓
  Clean output + timestamped log file
```

### Stage 1 — Extractor (`pipeline/extractor.py`)

`BaseExtractor` is an abstract base class that enforces a `.extract()` method on every subclass. Two implementations are provided:

- `CSVExtractor` — reads from a `.csv` file using `csv.DictReader`
- `JSONExtractor` — reads from a `.json` file, expects a top-level list

Both return the same format — a `list` of `dict` objects — so the rest of the pipeline is format-agnostic.

### Stage 2 — Transformer (`pipeline/transformer.py`)

`StudentTransformer` applies a series of ordered rule methods to each row:

| Rule | What it does |
|---|---|
| `_rule_strip_whitespace` | strips leading/trailing spaces from all string values |
| `_should_drop` | drops rows with missing name or all scores missing |
| `_rule_convert_scores` | converts score strings to floats, clamps values to 0–100 |
| `_rule_fill_missing_scores` | fills `None` scores with the row mean |
| `_rule_fix_type` | sets unknown student types to `"regular"` |
| `_rule_parse_projects` | converts comma-separated project string to a list |
| `_rule_add_average` | computes and adds `average` field |
| `_rule_add_grade` | computes and adds `grade` field (A/B/C/F) |

### Stage 3 — Loader (`pipeline/loader.py`)

`BaseLoader` is an abstract base class that enforces a `._write()` method. Three implementations:

- `CSVLoader` — writes clean rows to a `.csv` file
- `JSONLoader` — writes clean rows to a `.json` file
- `MultiLoader` — standalone coordinator that delegates to multiple loaders simultaneously

### Stage 4 — Pipeline (`pipeline/pipeline.py`)

`Pipeline` wires all three stages together. Calling `.run()` executes extract → transform → load in sequence, tracks timing for each stage, and returns run metadata.

```python
pipeline = Pipeline(
    extractor   = CSVExtractor("data/raw/students_raw.csv"),
    transformer = StudentTransformer(),
    loader      = MultiLoader([
        CSVLoader("data/output/students_clean.csv"),
        JSONLoader("data/output/students_clean.json"),
    ]),
    name = "Student Data Pipeline"
)

pipeline.run()
meta = pipeline.get_meta()
```

### Stage 5 — Logger (`utils/logger.py`)

`Logger` replaces scattered `print()` calls with structured, leveled log entries written simultaneously to the console and a timestamped `.log` file in `logs/`.

```
[2026-07-07 10:00:01] ℹ INFO     | Student_Data_Pipeline | Extracted 7 rows
[2026-07-07 10:00:01] ⚠ WARNING  | Student_Data_Pipeline | Invalid score 110.0 for 'Bopha' → clamped to 0
[2026-07-07 10:00:01] ✔ SUCCESS  | Student_Data_Pipeline | Wrote 6 rows to 'data/output/students_clean.csv'
```

Four log levels: `INFO`, `WARNING`, `ERROR`, `SUCCESS`.

### Stage 6 — Entry point (`main.py`)

Interactive menu that lets you:

- Pick the input source (CSV or JSON) and file path
- Pick the output format (CSV, JSON, or both)
- Confirm and run the pipeline
- Browse and read previous log files

---

## OOP concepts covered

| Concept | Where applied |
|---|---|
| Encapsulation | Each class owns its data and logic — no stage reaches into another |
| Inheritance | `CSVExtractor` → `BaseExtractor`, `CSVLoader` → `BaseLoader` |
| Abstraction | `@abstractmethod` forces `.extract()` and `._write()` on every subclass |
| Polymorphism | `pipeline.run()` works with any extractor or loader without modification |
| Liskov substitution | `MultiLoader` is a standalone coordinator — not forced into `BaseLoader` inheritance |
| Separation of concerns | Each file has exactly one responsibility |

---

## Extending the pipeline

### Add a new data source

Create a new extractor that inherits `BaseExtractor` and implement `.extract()`:

```python
class APIExtractor(BaseExtractor):
    def extract(self):
        import requests
        response = requests.get(self.filepath)   # filepath used as URL
        data = response.json()
        self.logger.info(f"Extracted {len(data)} rows from API")
        return data
```

Plug it into the pipeline — no other changes needed.

### Add a new transformation rule

Add a `_rule_*` method to `StudentTransformer` and call it inside `.transform()`:

```python
def _rule_normalize_name(self, row):
    row["name"] = row["name"].strip().title()
    return row
```

### Add a new output destination

Create a new loader that inherits `BaseLoader` and implement `._write()`:

```python
class DatabaseLoader(BaseLoader):
    def _write(self, rows):
        # insert rows into SQLite, PostgreSQL, etc.
        pass
```

---

## Sample data

The raw input file contains intentional data quality issues for the transformer to handle:

| Issue | Example |
|---|---|
| Missing name | `name` field is empty |
| Missing score | `score2` is blank for Dara |
| Invalid score | `score1 = 110` for Bopha (out of 0–100 range) |
| Unknown type | `type = "unknown"` for Chan |
| Missing project | `projects` is blank for regular students |

---

## Real-world connections

This pipeline mirrors how production data engineering tools work internally:

| This project | Production equivalent |
|---|---|
| `BaseExtractor` with `@abstractmethod` | Airflow `BaseOperator` with `.execute()` |
| Transformer rule methods | dbt model transformations |
| `MultiLoader` coordinator | Airflow fan-out tasks |
| `Logger` with file output | Python `logging` module with `FileHandler` |
| `Pipeline.run()` orchestration | Airflow DAG execution order |

---

## Author

Built as a hands-on OOP learning project working toward a career in data engineering and data science.