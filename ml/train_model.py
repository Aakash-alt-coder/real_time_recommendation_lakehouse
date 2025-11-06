"""
Train collaborative filtering model (ALS) using Spark MLlib
"""
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
import mlflow
import mlflow.spark

spark = SparkSession.builder.appName("ALSModelTraining").getOrCreate()
df = spark.read.format("delta").load("/delta/features/user_product_affinity")

als = ALS(userCol="user_id", itemCol="product_id", ratingCol="user_product_affinity", coldStartStrategy="drop")
model = als.fit(df)

mlflow.spark.log_model(model, "als_model")
print("ALS model trained and logged in MLflow.")
