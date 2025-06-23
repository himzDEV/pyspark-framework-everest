from abc import ABC, abstractmethod

class BaseReader(ABC):
    """
    Abstract base class for all readers.
    """

    @abstractmethod
    def read(self, spark_session):
        """
        Read data and return as DataFrame.

        :param spark_session: SparkSession instance
        :return: DataFrame
        """
        pass
