"""
Test job for Real-Time Recommendation Lakehouse project.
Purpose:
- Sanity check: Reads from Bronze layer (or any input source) and prints sample records.
- Can be expanded for unit/integration testing of Spark jobs.

Usage:
    spark-submit jobs/test_job.py

Assumptions:
- Delta tables exist at input paths.
- SPARK_MASTER and other configs are in environment or .env.
"""

import os
from pyspark.sql import SparkSession

BRONZE_PATH = os.getenv("BRONZE_PATH", "data/bronze")  # Local path for bronze table/data

def main():
    spark = SparkSession.builder \
        .appName("LakehouseTestJob") \
        .getOrCreate()

    print("Reading Bronze layer from:", BRONZE_PATH)
    # For testing: read Parquet, Delta, or CSV
    try:
        if os.path.exists(os.path.join(BRONZE_PATH, "_delta_log")):
            df = spark.read.format("delta").load(BRONZE_PATH)
            print("Bronze Delta table found.")
        elif len(os.listdir(BRONZE_PATH)) > 0:
            df = spark.read.parquet(BRONZE_PATH)
            print("Bronze Parquet data found.")
        else:
            print("Bronze folder empty, falling back to CSV.")
            df = spark.read.csv(BRONZE_PATH, header=True, inferSchema=True)
    except Exception as e:
        print(f"Error reading Bronze layer: {e}")
        return

    print("Schema:")
    df.printSchema()
    print("Sample Records:")
    df.show(10, truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()