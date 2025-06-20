class PipelineRunner:
    """
    Generic pipeline runner.
    Accepts a pipeline class and runs it using the provided config path.
    """

    def __init__(self, pipeline_cls, config_path: str):
        """
        :param pipeline_cls: Class that inherits from BasePipeline
        :param config_path: Path to the pipeline config (YAML or JSON)
        """
        self.pipeline_cls = pipeline_cls
        self.config_path = config_path

    def run(self):
        """
        Instantiates and runs the pipeline.
        """
        pipeline = self.pipeline_cls(self.config_path)
        pipeline.run()
