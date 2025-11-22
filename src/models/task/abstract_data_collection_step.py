from abc import ABC, abstractmethod


class AbstractDataCollectionStep(ABC):
    def __init__(self, step_name: str):
        self.step_name = step_name

    @abstractmethod
    def data_description(self) -> str:
      pass

    @abstractmethod
    def question(self) -> str:
      pass

    @abstractmethod
    def get_step_name(self) -> str:
      pass

    @abstractmethod
    def validate(self) -> bool:
      pass


