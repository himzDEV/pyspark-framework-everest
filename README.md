pyspark-framework-everest
=========================

Overview
--------
The PySpark Framework provides a robust, scalable, and modular foundation for building data pipelines using Apache Spark.

This framework is designed to:
- Enable easy onboarding of new pipelines through configuration-driven design.
- Provide reusable components for reading from and writing to common data sources/targets.
- Ensure clean separation of concerns (reading, writing, validation, orchestration).
- Support packaging as a Python library or Docker image for deployment on Spark clusters (e.g., Dataproc, EMR, Kubernetes).

Architecture
------------
Folder structure:
pyspark_framework/
├── core/            # Abstract base pipeline, runner, sequence executor
├── reader/          # Modular source readers (BigQuery, GCS, S3, JDBC, etc.)
├── writer/          # Modular target writers (Parquet, BigQuery, S3, JDBC, etc.)
├── validator/       # Config and data validation logic
├── utils/           # Config loader, Spark session creator, logger
├── extensions/      # Optional helpers (e.g., joiner, metrics)
└── tests/           # Unit tests organized by module

Key concepts:
- Sources: Any number of sources can be defined in config, and registered as Spark SQL temp views using their alias.
- Sequences: Each sequence specifies:
  - A SQL query or Spark SQL expression that references source aliases.
  - A target specification for output.
- Targets: Each sequence maps to exactly one target.

Configuration
-------------
Pipeline jobs are driven by YAML/JSON configs:
app_name: "example_pipeline"
spark_conf:
  spark.executor.memory: "4g"

sources:
  source1:
    type: "bigquery"
    alias: "bq_table"
    query: "SELECT * FROM `project.dataset.table`"

  source2:
    type: "s3"
    alias: "s3_data"
    path: "s3://bucket/path/"

sequences:
  - name: "summary_sequence"
    query: "SELECT user_id, COUNT(*) AS cnt FROM bq_table GROUP BY user_id"
    target:
      type: "parquet"
      path: "gs://output-bucket/summary/"
      mode: "overwrite"

  - name: "enriched_sequence"
    query: |
      SELECT bq_table.user_id, s3_data.extra_info
      FROM bq_table
      LEFT JOIN s3_data ON bq_table.user_id = s3_data.user_id
    target:
      type: "bigquery"
      table: "project.dataset.enriched_output"
      mode: "append"

How to Use
----------
1. Add this framework as a dependency in your pipeline repo:
- As a wheel:  
  pip install pyspark_framework-<version>.whl
- As a Docker base image:  
  FROM <your_artifact_registry>/pyspark-framework:<version>

2. In your pipeline repo:
- Write a config file (YAML/JSON).
- Write a lightweight Python entry point that uses the framework’s BasePipeline / PipelineRunner.

3. Run on cluster:
- python main.py --config configs/my_pipeline.yaml
- Or submit as Spark job:
  spark-submit --py-files pyspark_framework-<version>.whl main.py --config configs/my_pipeline.yaml

Packaging
---------
This repo produces:
- Python wheel for installing as a library.
- Docker image (optional) for running on Spark clusters that use containers.

Extending the Framework
-----------------------
To add a new source:
- Implement a new reader in reader/, subclassing BaseReader.

To add a new target:
- Implement a new writer in writer/, subclassing BaseWriter.

No need to modify core pipeline or runner logic — the framework dynamically dispatches readers/writers based on config.

Testing
-------
- Unit tests live in tests/ and cover all components.
- Run: pytest tests/

License
-------
Include your license details here (e.g., Apache 2.0, MIT, etc.)

Support / Contribution
----------------------
- Raise issues or feature requests via the repository issue tracker.
- Contributions welcome! Please submit pull requests against dev branch with clear descriptions and unit tests.
