from models.task.blend_optimization_task import BlendOptimizationTask
from models.task.not_definded_task import NotDefinedOptimizationTask
from models.task.transportation_optimization_task import \
  TransportationOptimizationTask

REGISTERED_TASKS = [NotDefinedOptimizationTask, BlendOptimizationTask,
                    TransportationOptimizationTask]
