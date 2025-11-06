"""
Batch ingestion for product catalog
"""
from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.appName("ProductCatalogIngestion").getOrCreate()
    bronze_path = "adls://lakehouse/bronze/product_catalog/"

    df = spark.read.csv("data/product_catalog.csv", header=True, inferSchema=True)
    df.write.format("delta").mode("append").save(bronze_path)
    print("Product catalog ingested to Bronze layer")

if __name__ == "__main__":
    main()
