# Architecture Overview

## Data Flow

- **Streaming**: User actions flow via Kafka/Event Hub to Bronze raw layer.
- **Batch**: Daily user profiles and product catalogs land in ADLS, loaded to Bronze.
- **Lakehouse Layers**:
    - **Bronze**: Raw data (no edits)
    - **Silver**: Cleaned, deduplicated, quality-checked
    - **Gold**: Aggregated, ML-featured, ready for serving (including recommendations)
- **Feature Store**: Central Delta/Feast tables, with session and affinity metrics.
- **ML**: ALS/LightFM training/validation, model logged to MLflow, scored recommendations back to Gold.
- **Orchestration**: Airflow DAGs (local/remote), optionally Azure Data Factory.
- **Serving**: Recommendations stored in Delta and Redis/Azure Cache for sub-ms latency.

## Infrastructure

- **Azure Terraform**: ADLS Gen2, Event Hub, Databricks workspace, Redis Cache.
- **Local stack**: Docker Compose for Kafka, Airflow, Redis, Postgres (Feast).

## Observability & Quality

- Great Expectations checks embedded in ETL
- Logging via Airflow, custom Python (logs & metrics)
- Alert samples (Azure Monitor/Slack/email; see scripts/)

## Scaling

- Designed for 10k+ events/sec, 100k users/products (simulate or scale infra accordingly)