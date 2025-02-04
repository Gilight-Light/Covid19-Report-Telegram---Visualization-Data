# read.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr

def main():
    spark = SparkSession.builder \
    .appName("Covid19 Data Processing") \
    .getOrCreate()

    data_path = "./include/dataset/covid_19_clean_complete.csv"
    # Đọc file CSV
    df = spark.read.csv(data_path, header=True, inferSchema=True)

    # Đổi tên cột
    df = df.withColumnRenamed("Date", "date") \
        .withColumnRenamed("Province/State", "state") \
        .withColumnRenamed("Country/Region", "country") \
        .withColumnRenamed("Lat", "lat") \
        .withColumnRenamed("Long", "long") \
        .withColumnRenamed("Confirmed", "confirmed") \
        .withColumnRenamed("Deaths", "deaths") \
        .withColumnRenamed("Recovered", "recovered")

    # Thêm cột 'active' = confirmed - deaths - recovered
    df = df.withColumn("active", expr("confirmed - deaths - recovered"))

    # Hiển thị dữ liệu
    df.show()
    df.write.csv(data_path, header=True, mode="overwrite")
    
    # Write the DataFrame to PostgreSQL
    df.write \
        .format('jdbc') \
        .option('url', 'jdbc:postgresql://postgres:5436/dataeng') \
        .option('dbtable', 'public.covid') \
        .option('user', 'postgres') \
        .option('password', 'postgres') \
        .option('driver', 'org.postgresql.Driver') \
        .save()

    # Stop the Spark session
    spark.stop()
    
if __name__ == "__main__":
    main()