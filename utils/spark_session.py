from pyspark.sql import SparkSession

class SparkSessionFactory:
    """
    Utility to create SparkSession with dynamic configuration.
    """

    @staticmethod
    def create(app_name: str = "PySparkApp", spark_conf: dict = None):
        builder = SparkSession.builder.appName(app_name)

        if spark_conf:
            for key, value in spark_conf.items():
                builder = builder.config(key, value)

        spark = builder.getOrCreate()
        return spark
