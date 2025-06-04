# cricbuzz-api-to-gcs

An Apache Airflow DAG that fetches player ranking data from the Cricbuzz API and uploads the processed data into Google Cloud Storage (GCS) as a CSV file. This pipeline is triggered and scheduled entirely via the Airflow web interface.

---

## 📖 Description

This DAG is part of a migration pipeline that performs the following tasks:

1. Makes an HTTP GET request to the Cricbuzz public API for ODI batsmen rankings.
2. Processes and extracts relevant fields (`rank`, `name`, `country`).
3. Writes the data to a temporary CSV file.
4. Uploads the CSV file directly to a specified GCS bucket (`ranking-data-1`).

The DAG uses the `DummyOperator` for initialization and a `PythonOperator` to execute the data extraction and upload.

---

## 🗂️ Project Structure

```text
dags/
└── pipeline.py       # The main Airflow DAG script
└── README.md         # Project documentation
```

---

## ⚙️ Requirements

### Python Packages (within your Airflow environment)

Ensure your Airflow environment has the following Python packages installed:

- `requests`
- `google-cloud-storage`

You can install them with:

```bash
pip install requests google-cloud-storage
```

### Google Cloud Setup

- Enable the **Cloud Storage API** in your GCP project.
- Create a bucket named **`ranking-data-1`** (or update the DAG with your bucket name).
- Ensure your Airflow environment has access to authenticate with GCP and upload to that bucket (via service account, workload identity, etc.).

---

## 🚀 Deployment Instructions

1. Place `pipeline.py` in your Airflow `dags/` directory.
2. Restart the Airflow scheduler (if needed).
3. Open the Airflow UI, locate the DAG named **`pipeline`**.
4. Trigger the DAG manually or let it run on its daily schedule (`@daily`).

---

## 🔐 Security Note

The script contains an API key in plain text. You should move this to a secure location such as:
- Airflow **Variables** or **Connections**
- Environment variables
- Secret managers

