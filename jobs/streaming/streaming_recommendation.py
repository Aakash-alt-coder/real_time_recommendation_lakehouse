"""
Real-time Spark Structured Streaming job
Aggregates clickstream and updates Gold layer
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, struct
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

spark = SparkSession.builder.appName("StreamingRecommendation").getOrCreate()

# Define clickstream schema
schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("action", StringType(), True),
    StructField("timestamp", StringType(), True)
])

# Read from Kafka
df_raw = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "clickstream") \
    .option("startingOffsets", "latest") \
    .load()

df_parsed = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

# Aggregate user-product counts
agg = df_parsed.groupBy("user_id", "product_id").count()

# Write to Gold Delta
query = agg.writeStream \
    .format("delta") \
    .outputMode("complete") \
    .option("checkpointLocation", "/delta/checkpoints/streaming_recommendation") \
    .start("/delta/gold/recommendations")

query.awaitTermination()
