"""
Batch ingestion for user profiles
Ingests CSV data into Bronze layer (Delta Lake)
"""
from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.appName("UserProfileIngestion").getOrCreate()
    bronze_path = "adls://lakehouse/bronze/user_profile/"

    # Read user profile CSV
    df = spark.read.csv("data/user_profiles.csv", header=True, inferSchema=True)
    df.write.format("delta").mode("append").save(bronze_path)
    print("User profiles ingested to Bronze layer")

if __name__ == "__main__":
    main()
