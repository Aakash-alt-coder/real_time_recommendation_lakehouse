"""
Feature Store definition for Real-Time Recommendation Lakehouse.

Supports:
- Feast (recommended, uses Postgres or Redis backend)
- Delta Lake (if running on Spark/Databricks)

Defines entities, features, and sample registration. Provides functions to
write and read features.

Usage:
    python features/feature_store.py
    # to register and ingest features

Comments explain each step.
"""

import os
import pandas as pd

# Feast imports
try:
    from feast import FeatureStore, Entity, FeatureView, Field, FileSource
    from feast.types import String, Int64, Float32
    FEAST_ENABLED = True
except ImportError:
    FEAST_ENABLED = False

# Paths
FEATURE_REPO_PATH = os.getenv("FEAST_REPO_PATH", "./feature_repo")
FEATURE_DATA_PATH = os.getenv("FEATURE_DATA_PATH", "features/user_product_features.parquet")

def setup_feast_feature_store():
    """Define entities and feature views for user-product affinity."""
    user = Entity(name="user_id", join_keys=["user_id"])
    product = Entity(name="product_id", join_keys=["product_id"])

    source = FileSource(
        path=FEATURE_DATA_PATH,
        event_timestamp_column="event_time",
    )

    user_product_fv = FeatureView(
        name="user_product_features",
        entities=["user_id", "product_id"],
        ttl=None,
        schema=[
            Field(name="affinity_score", dtype=Float32),
            Field(name="rolling_engagement", dtype=Float32),
            Field(name="session_stats", dtype=Int64),
        ],
        online=True,
        source=source,
    )
    # You can use YAML/CLI for full repo, but here is code-based setup
    return user, product, user_product_fv

def ingest_features_to_feast():
    """Register and ingest features to Feast."""
    if not FEAST_ENABLED:
        print("Feast not installed. Skipping Feast feature store setup.")
        return

    user, product, user_product_fv = setup_feast_feature_store()
    fs = FeatureStore(repo_path=FEATURE_REPO_PATH)
    print("Registering entities and feature views...")
    fs.apply([user, product, user_product_fv])

    # Load feature data as DataFrame (example)
    if FEATURE_DATA_PATH.endswith(".parquet") and os.path.exists(FEATURE_DATA_PATH):
        feature_df = pd.read_parquet(FEATURE_DATA_PATH)
    else:
        feature_df = pd.DataFrame({
            "user_id": ["user_1", "user_2"],
            "product_id": ["product_1", "product_2"],
            "affinity_score": [1.45, 2.34],
            "rolling_engagement": [0.78, 1.02],
            "session_stats": [3, 7],
            "event_time": ["2025-11-06T09:00:00Z", "2025-11-06T09:01:00Z"],
        })
    print("Ingesting features to Feast...")
    fs.write_dataframe(feature_df)

def ingest_features_to_delta(delta_path="features/user_product_features.delta"):
    """(Alternative) Write features as Spark Delta table."""
    try:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.appName("FeatureStore").getOrCreate()
    except ImportError:
        print("Spark not installed. Skipping Delta feature store setup.")
        return

    feature_df = pd.read_parquet(FEATURE_DATA_PATH)
    sdf = spark.createDataFrame(feature_df)
    print(f"Writing features to Delta table at {delta_path}...")
    sdf.write.format("delta").mode("overwrite").save(delta_path)

if __name__ == "__main__":
    # Choose Feast or Delta based on environment
    use_feast = os.getenv("USE_FEAST", "True") == "True"
    if use_feast:
        ingest_features_to_feast()
    else:
        ingest_features_to_delta()