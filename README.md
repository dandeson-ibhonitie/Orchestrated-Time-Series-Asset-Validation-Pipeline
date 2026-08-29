# Orchestrated-Time-Series-Asset-Validation-Pipeline
An automated, production-grade ETL data pipeline engineered in Python. It ingests high-velocity time-series event data from a live REST API, applies strict ISO-8601 datetime standardization using Pandas, and loads cleaned telemetry records into an idempotent SQLite warehouse managed via a centralized system orchestration controller.



A production-grade, modular ETL (Extract, Transform, Load) data engineering pipeline built to ingest, standardize, and warehouse high-velocity event tracking payloads. The architecture eliminates manual execution dependency by centralizing the data assembly line under a native synchronous Python orchestration controller.

##  System Architecture Overview

```text
           ┌───────────────────────────────────────┐
           │        orchestrator.py                │  <─── Master Controller Layer
           └───────────────────┬───────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
   [ 1_extract.py ] ──► [ 2_transform.py ] ──► [ 3_load.py ]
   Raw Lake Ingestion   ISO-8601 Standardization  Idempotent DB Append
```

##  The Engineering Challenge
In high-velocity trading or asset-tracking systems, multi-format timestamp data from global vendors creates analytical disparity, making delta-interval calculations unreliable. Additionally, executing individual multi-part code modules manually risks operational fragmentation. 

This engine solves these structural bottlenecks by forcing data payloads into an absolute international timeline format, implementing data type assertions, and running under a unified pipeline supervisor.

##  Module Structural Breakdowns

###  1. Ingestion Layer (`1_extract.py`)
* **Objective:** Connects to the endpoint `https://restful-api.dev` to pull live tracking data.
* **Defensive Patterns:** Includes explicit request timeouts (`timeout=15`) and full network exception traps (`requests.exceptions.RequestException`) to log infrastructure timeouts and prevent silent script freezes. Saves a raw local snapshot to `time_series_raw.json`.

###  2. Transformation Gate (`2_transform.py`)
* **Objective:** Normalizes structured multi-level JSON fields into clean tabular rows using `pd.json_normalize()`.
* **The Datetime Standardization Gate:** Generates a live processing timestamp column (`processed_at`) forced into a strict international ISO-8601 string sequence (`YYYY-MM-DD HH:MM:SS`) using Pandas `.dt.strftime()`.
* **Data Cleansing:** Standardizes headers to absolute lowercase formats *before* applying row filter assertions (`.dropna(subset=['id'])`) to eliminate broken records and catch shifting upstream field casing automatically. Saves output to `time_series_clean.csv`.

###  3. Storage Warehouse (`3_load.py`)
* **Objective:** Connects to a persistent local SQLite data warehouse (`time_series_warehouse.db`).
* **Defensive Schema Design:** Maps a primary key constraint to the core `id` field. Column names containing special characters or formatting spaces are escaped dynamically with double quotes (`"`) to ensure raw database compatibility.
* **Idempotency Rules:** Employs an append configuration paired with database mapping checks. Duplicate entry drops are handled gracefully without aborting execution batches or corrupting existing transaction histories.

###  4. Master Orchestration Layer (`orchestrator.py`)
* **Objective:** The central pipeline ops control center.
* **Subprocess Sychronization:** Uses Python's native `subprocess` layer to sequentially execute, monitor, and pass active execution states between dependency nodes using integer return codes. If any script crashes, the orchestrator instantly drops the conveyor belt to safeguard target schema environments.
* **Observability Logs:** Generates a detailed performance timing metric report to pinpoint bandwidth bottlenecks and database query speeds.

---

##  Execution Instructions

### 1. Requirements Installation
Verify that your local system command line shell environment has the primary data dependencies installed:
```bash
pip install requests pandas
```

### 2. Running the System Command
To trigger the automated pipeline execution loop, call the master control layer from your terminal:
```bash
python orchestrator.py
```

### 3. Production Environment Local Automation
To schedule this data pipeline to execute automatically every single night on Windows without manual developer intervention:
1. Create a file named `run_pipeline.bat` containing:
   ```batch
   python "C:\Your\Exact\Project\Path\orchestrator.py"
   ```
2. Open **Windows Task Scheduler** and choose **Create Basic Task**.
3. Set the **Trigger** window to **Daily** at your preferred midnight slot.
4. Set the **Action** to **Start a Program**, browse to link your `run_pipeline.bat` file, and paste your absolute folder path into the **Start in (optional)** field to enforce the local directory context.
