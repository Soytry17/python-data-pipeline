# Student Data Pipeline

A simple but scalable **Python ETL (Extract, Transform, Load) pipeline** designed to process student data from raw CSV files, clean and transform the data, and export the final results into multiple formats.

The project demonstrates common **Data Engineering concepts**:

* ETL pipeline architecture
* Object-Oriented Programming (OOP)
* Abstract base classes
* Data validation and cleaning
* Logging system
* Pipeline metadata tracking
* Multiple output loaders

---

# Project Architecture

```
data-pipeline/
│
├── data/
│   ├── raw/
│   │   └── students_raw.csv
│   │
│   └── output/
│       ├── students_clean.csv
│       └── students_clean.json
│
├── logs/
│   └── StudentPipeline_YYYYMMDD_HHMMSS.log
│
├── pipeline/
│   ├── __init__.py
│   ├── extractor.py
│   ├── transform.py
│   ├── loader.py
│   ├── logger.py
│   └── pipeline.py
│
├── tests/
│   └── test_pipeline.py
│
└── README.md
```

---

# Pipeline Flow

```
Raw CSV File
      |
      v
+-------------+
|  Extractor  |
+-------------+
      |
      v
Raw Student Records
      |
      v
+--------------+
| Transformer  |
+--------------+
      |
      v
Clean Student Records
      |
      v
+----------------+
| Multi Loader   |
+----------------+
      |
      +-------------> CSV Output
      |
      +-------------> JSON Output
```

---

# Features

## 1. Extract Layer

The extractor reads raw data from CSV files.

Example:

```python
CSVExtractor(
    "data/raw/students_raw.csv"
)
```

Responsibilities:

* Read input files
* Convert CSV rows into Python dictionaries
* Provide data for transformation

---

## 2. Transform Layer

The transformation layer applies data cleaning and business rules.

Implemented rules:

### Remove whitespace

Example:

Before:

```
" Alice "
```

After:

```
"Alice"
```

---

### Validate student name

Rows without names are removed.

Example:

```python
{
    "name": "",
    "score1": 80
}
```

Result:

```
Dropped
```

---

### Convert scores

Input:

```
"95"
```

Output:

```python
95.0
```

Invalid scores are corrected.

Example:

```
score = 150
```

becomes:

```
score = 0
```

---

### Fill missing scores

Missing scores are replaced using the average score.

Example:

Before:

```json
{
 "score1": 80,
 "score2": null,
 "score3": 90
}
```

After:

```json
{
 "score1": 80,
 "score2": 85,
 "score3": 90
}
```

---

### Standardize student type

Allowed values:

```
regular
ds
```

Unknown values are changed to:

```
regular
```

---

### Calculate average score

Example:

```
score1 = 80
score2 = 90
score3 = 70
```

Result:

```
average = 80
```

---

### Assign grade

Rules:

| Average | Grade |
| ------- | ----- |
| >= 90   | A     |
| >= 75   | B     |
| >= 60   | C     |
| < 60    | F     |

---

# 3. Load Layer

The loader supports multiple output formats.

Implemented loaders:

## CSV Loader

Output:

```
students_clean.csv
```

## JSON Loader

Output:

```
students_clean.json
```

## Multi Loader

Allows writing the same transformed data to multiple destinations.

Example:

```python
loader = MultiLoader([
    CSVLoader("students_clean.csv"),
    JSONLoader("students_clean.json")
])
```

---

# Logging System

The project includes a custom logging system.

Example output:

```
[2026-07-07 10:30:20] ℹ INFO     | StudentPipeline | Extracting data
[2026-07-07 10:30:22] ⚠ WARNING  | StudentPipeline | Missing score fixed
[2026-07-07 10:30:25] ✔ SUCCESS  | StudentPipeline | Loading completed
```

The logger provides:

* Console output
* File logging
* Log history
* Log summary

Example:

```
LOG SUMMARY — StudentPipeline
--------------------------------------------------
total entries  : 25
warnings       : 5
errors         : 0
log file       : logs/StudentPipeline.log
--------------------------------------------------
```

---

# Pipeline Metadata

The pipeline tracks execution statistics:

Example:

```python
{
    "rows_extracted": 100,
    "rows_transformed": 95,
    "rows_loaded": 95,
    "rows_dropped": 5
}
```

This helps monitor ETL performance.

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project:

```bash
cd data-pipeline
```

(Optional) Create virtual environment:

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

---

# Running the Pipeline

From project root:

```bash
python -m tests.test_pipeline
```

Expected output:

```
Pipeline started

Extractor completed
Transformer completed
Loader completed

Pipeline finished successfully
```

---

# Example Input

`students_raw.csv`

```csv
name,type,score1,score2,score3,projects
Alice,regular,90,85,95,Python,SQL
Bob,ds,70,,80,ML
```

---

# Example Output

`students_clean.json`

```json
[
  {
    "name": "Alice",
    "type": "regular",
    "score1": 90,
    "score2": 85,
    "score3": 95,
    "average": 90,
    "grade": "A"
  }
]
```

---

# Design Principles

This project follows:

* Clean Code principles
* Separation of responsibilities
* Object-oriented design
* Reusable components
* Dependency injection for logging
* Extensible loader architecture

Future improvements:

* Database loader (PostgreSQL)
* Configuration file support
* Unit testing with PyTest
* Data quality reports
* Airflow orchestration
* Docker deployment

---

# Learning Goals

This project was built to practice:

* Python OOP
* ETL pipeline design
* Data transformation techniques
* Error handling
* Logging architecture
* Data Engineering workflow concepts

---

# Author

Data Engineering Student Project
