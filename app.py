from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os

load_dotenv(override=True)

spark_local_ip = os.getenv("SPARK_LOCAL_IP")

if not spark_local_ip:
    raise ValueError(
        "A variável de ambiente 'SPARK_LOCAL_IP' não foi definida no arquivo .env"
    )

spark = (
    SparkSession.builder.appName("Teste")
    .config("spark.driver.host", spark_local_ip)
    .getOrCreate()
)

print(f"Configuração Spark - Driver Host definido como: {spark_local_ip}")
