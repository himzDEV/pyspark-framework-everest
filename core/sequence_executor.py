from pyspark_framework.writer import WriterFactory

class SequenceExecutor:
    def __init__(self, spark_session, sequence_conf: dict, logger):
        self.spark = spark_session
        self.sequence_conf = sequence_conf
        self.query = sequence_conf.get("query")
        self.target_conf = sequence_conf.get("target")
        self.logger = logger

        if not self.query:
            raise ValueError("Sequence configuration must include a 'query'.")
        if not self.target_conf:
            raise ValueError("Sequence configuration must include a 'target'.")

    def run(self):
        seq_name = self.sequence_conf.get('name', 'unnamed')

        self.logger.info(f"Running sequence '{seq_name}'")

        # Execute query
        df = self.spark.sql(self.query)
        self.logger.info(f"Sequence '{seq_name}' produced schema: {df.schema.simpleString()}")

        # Write output
        writer = WriterFactory.create(self.target_conf)
        writer.write(df, self.target_conf)

        self.logger.info(f"Sequence '{seq_name}' completed successfully.")
