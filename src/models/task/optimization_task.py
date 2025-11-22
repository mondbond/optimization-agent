from src.models.task.abstract_data_collection_step import AbstractDataCollectionStep


class OptimizationTask:
    def __init__(self, data_collection_steps: list[AbstractDataCollectionStep]):
        self.steps = data_collection_steps

    def __repr__(self):
        return f"OptimizationTask(task_id={self.task_id}, description={self.description}, parameters={self.parameters})"
