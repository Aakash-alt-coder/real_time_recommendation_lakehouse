# Real-Time Personalized Recommendation Lakehouse

## Overview

A cloud-ready, production Data Engineering project for real-time, personalized recommendations, leveraging streaming (Kafka/EventHub), batch, Delta Lake layers, Azure infrastructure, ML, CI/CD, and orchestration.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for full overview: streaming/batch dataflows, Lakehouse layers (Bronze, Silver, Gold), feature engineering, orchestration and ML model lifecycle.

## Quick Start: Local Development

1. **Clone and Setup**
   ```bash
   git clone https://github.com/your-org/rec-lakehouse.git
   cd rec-lakehouse
   cp .env.sample .env
   ```

2. **Launch Local Stack**
   ```bash
   docker-compose up
   ```

3. **Run Producer**
   ```bash
   python producer/clickstream_producer.py
   ```

4. **Run Spark Streaming**
   - (standalone or on Databricks)

5. **Trigger Airflow ETL DAG**
   - Access Airflow UI at [localhost:8080](http://localhost:8080) and trigger `lakehouse_etl`

6. **Feature Store**
   - See `features/feature_engineering.py` to generate and push features to Feast/Delta

7. **ML Model**
   - Use `ml/train_als.py` for collaborative filtering and MLflow logging

## Deploy to Azure

1. **Edit `.env` with your Azure credentials**
2. **Provision infrastructure**
   ```bash
   cd infra/terraform
   terraform init
   terraform apply
   ```
3. **Deploy Spark/Flink jobs on Databricks workspace**
4. **Connect your Airflow instance to Azure services as needed**

## Monitoring and Data Quality

- Integrate `Great Expectations` in ETL DAGs (`airflow/dags/`)
- Set up alerts with Azure Monitor or custom Python scripts

## CI/CD

- All pushes and PRs are checked via GitHub Actions (`.github/workflows/ci.yaml`)
- Linting, tests, and Terraform plan checks included

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.