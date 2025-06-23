from abc import ABC, abstractmethod
from pyspark.sql import SparkSession
from pyspark_framework.utils.config_loader import ConfigLoader
from pyspark_framework.utils.spark_session import SparkSessionFactory
from pyspark_framework.utils.logger import LoggerFactory
from pyspark_framework.reader import ReaderFactory
from pyspark_framework.core.sequence_executor import SequenceExecutor
from pyspark_framework.validator.config_validator import ConfigValidator

class BasePipeline(ABC):
    """
    Abstract base class for all pipelines.
    """

    def __init__(self, config_path: str):
        self.logger = LoggerFactory.create_logger(self.__class__.__name__)
        self.config_path = config_path
        self.config = ConfigLoader.load(config_path)

        self.logger.info(f"Loaded config from {config_path}")

        # Validate config structure
        ConfigValidator.validate(self.config)
        self.logger.info("Config validation passed.")

        # Create Spark session
        self.spark = SparkSessionFactory.create(
            self.config.get("app_name"),
            self.config.get("spark_conf")
        )
        self.logger.info("Spark session created.")

        self.sources = self.config.get("sources", {})
        self.sequences = self.config.get("sequences", [])

    def register_sources(self):
        for source_name, source_conf in self.sources.items():
            reader = ReaderFactory.create(source_conf)
            df = reader.read(self.spark)
            alias = source_conf.get("alias", source_name)
            df.createOrReplaceTempView(alias)
            self.logger.info(f"Registered source '{source_name}' as view '{alias}'.")

    def run_sequences(self):
        for sequence_conf in self.sequences:
            executor = SequenceExecutor(self.spark, sequence_conf, self.logger)
            executor.run()

    def run(self):
        try:
            self.logger.info("Pipeline started.")
            self.register_sources()
            self.run_sequences()
            self.logger.info("Pipeline completed successfully.")
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            raise
        finally:
            self.spark.stop()
            self.logger.info("Spark session stopped.")
