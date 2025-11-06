"""
Feature engineering for recommendation system
Compute user-product affinity and session features
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("FeatureEngineering").getOrCreate()

clickstream_path = "/delta/silver/clickstream/"
df = spark.read.format("delta").load(clickstream_path)

features = df.groupBy("user_id", "product_id").count() \
             .withColumnRenamed("count", "user_product_affinity")

features.write.format("delta").mode("overwrite").save("/delta/features/user_product_affinity")
print("Features computed and stored.")
