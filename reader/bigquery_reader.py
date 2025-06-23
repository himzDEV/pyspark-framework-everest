from pyspark_framework.reader.base_reader import BaseReader

class BigQueryReader(BaseReader):
    """
    Reads data from BigQuery.
    """

    def __init__(self, source_conf: dict):
        self.source_conf = source_conf

    def read(self, spark_session):
        query = self.source_conf.get("query")
        table = self.source_conf.get("table")

        if query:
            df = spark_session.read.format("bigquery").option("query", query).load()
        elif table:
            df = spark_session.read.format("bigquery").option("table", table).load()
        else:
            raise ValueError("BigQuery source requires either 'query' or 'table' in config.")

        return df
