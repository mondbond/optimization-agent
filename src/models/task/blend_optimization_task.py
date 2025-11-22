from src.models.task.abstract_optimization_task import AbstractOptimizationTask
from src.models.enums.optimization_type import OptimizationType

class BlendOptimizationTask(AbstractOptimizationTask):


    @classmethod
    def description(cls):
        return "This optimization type need to be choosen when you can clearly detect entities like ingredients that togather can create some products."

    @classmethod
    def get_type(cls):
        return OptimizationType.BLENDING

    def get_steps(self):
        return None
