from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.blend_data_model import BlendDataModel
from src.models.task.abstract_optimization_task import AbstractOptimizationTask
from src.models.enums.optimization_type import OptimizationType

class BlendOptimizationTask(AbstractOptimizationTask):


    @classmethod
    def description(cls):
        return "This optimization type need to be choosen when you can clearly detect entities like ingredients that togather can create some products."

    @classmethod
    def get_type(cls):
        return OptimizationType.BLENDING

    @staticmethod
    def get_optimization_data_model() -> AbstractDataModel:
        return BlendDataModel()
