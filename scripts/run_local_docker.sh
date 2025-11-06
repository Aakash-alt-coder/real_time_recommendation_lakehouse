#!/bin/bash
# Run the complete local stack via Docker Compose for Real-Time Recommendation Lakehouse.

# Exit on error
set -e

# Optional: Load environment variables from .env if exists
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | xargs)
fi

echo "Starting local Docker stack (Kafka, Zookeeper, Airflow, Redis, Postgres)..."
docker-compose up -d

echo "All containers started in background."
echo "Access Airflow at http://localhost:8080"
echo "Kafka listening on localhost:9092"
echo "Redis on localhost:6379"