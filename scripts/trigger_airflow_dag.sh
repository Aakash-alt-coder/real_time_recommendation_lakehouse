#!/bin/bash
# Script to trigger the Airflow ETL DAG from CLI
# Usage: bash scripts/trigger_airflow_dag.sh [DAG_ID]
# Defaults to lakehouse_etl

DAG_ID=${1:-lakehouse_etl}
AIRFLOW_HOST=${AIRFLOW_HOST:-"http://localhost:8080"}
AIRFLOW_USER=${AIRFLOW_USER:-"airflow"}
AIRFLOW_PW=${AIRFLOW_PW:-"airflow"}

echo "Triggering Airflow DAG '${DAG_ID}' using Airflow REST API..."

# Option 1: Using Airflow REST API (Airflow 2.x with API enabled).
curl -X POST \
  --user "$AIRFLOW_USER:$AIRFLOW_PW" \
  "${AIRFLOW_HOST}/api/v1/dags/${DAG_ID}/dagRuns" \
  -H 'Content-Type: application/json' \
  --data '{"conf":{}}'

echo "DAG ${DAG_ID} triggered (check Airflow UI for status)."

# Alternate: For Airflow CLI in Docker container
# Uncomment below if you prefer using Docker exec:
# docker exec -it <airflow-container-name> airflow dags trigger ${DAG_ID}