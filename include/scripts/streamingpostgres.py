from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
import requests
import json
import time

def fetch_data(api_url):
    """Fetch data from API."""
    response = requests.get(api_url)
    response.raise_for_status()
    return [json.loads(response.text)]

# Tạo SparkSession
spark = SparkSession.builder \
    .appName("Covid19 Streaming") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.2.5") \
    .getOrCreate()

# Cấu trúc schema
schema = "province_state STRING, country_region STRING, lat FLOAT, long FLOAT, date STRING, confirmed INT, deaths INT, recovered INT, active INT, who_region STRING"

api_url = "http://localhost:5000/stream"

while True:
    data = fetch_data(api_url)
    rdd = spark.sparkContext.parallelize(data)
    df = spark.read.json(rdd, schema=schema)
    
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://host.docker.internal:5436/postgres") \
        .option("dbtable", "public.covid19") \
        .option("user", "postgres") \
        .option("password", "postgres") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
    
    print(f"Streamed data: {data}")
    time.sleep(5)  # Đợi 5 giây cho lần tiếp theo
