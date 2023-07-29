from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
df = spark.read.text("hdfs://localhost:9000/test.txt")
df.show()

