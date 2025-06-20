from pyspark_framework.reader.bigquery_reader import BigQueryReader
from pyspark_framework.reader.s3_reader import S3Reader
from pyspark_framework.reader.gcs_reader import GCSReader
from pyspark_framework.reader.jdbc_reader import JDBCReader

class ReaderFactory:
    """
    Factory to create reader instances based on config.
    """

    @staticmethod
    def create(source_conf: dict):
        source_type = source_conf.get("type")
        if source_type == "bigquery":
            return BigQueryReader(source_conf)
        elif source_type == "s3":
            return S3Reader(source_conf)
        elif source_type == "gcs":
            return GCSReader(source_conf)
        elif source_type == "jdbc":
            return JDBCReader(source_conf)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
