from typing import ClassVar
from models.model_validation import ModelValidationInstructions
from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.dataitem.float_value_matrix_data_item import \
  FloatValueMatrixDataItem
from models.task.datamodel.dataitem.map_data_item import \
  MapWithFloatValueDataItem
from models.task.datamodel.dataitem.string_data_item import StringDataItem
from utils import string_manager


class TransportationDataModel(AbstractDataModel):
  """
  Data model handler for transportation optimization tasks.
  Manages data related to suppliers, consumers, transportation costs, and the objective function.

  1. SUPPLIER_AVAILABILITY: Map of suppliers and their available supply.
  2. CONSUMER_NEEDS: Map of consumers and their required needs.
  3. SUPPLIER_TO_CONSUMER: Matrix of transportation costs from suppliers to consumers.
  4. OBJECTIVE_FUNCTION: String indicating whether to minimize or maximize the objective function
  """

  SUPPLIER_AVAILABILITY: ClassVar[str] = "supplier_availability"
  CONSUMER_NEEDS: ClassVar[str] = "consumer_needs"
  SUPPLIER_TO_CONSUMER: ClassVar[str] = "supplier_to_consumer"
  OBJECTIVE_FUNCTION: ClassVar[str] = "objective_function"

  @classmethod
  def create(cls):
    data = [
      MapWithFloatValueDataItem(
          data_name=cls.SUPPLIER_AVAILABILITY,
          description=string_manager.get('sup_availability_description'),
          action_examples=string_manager.get('sup_availability_example', resource_name=cls.SUPPLIER_AVAILABILITY)),
      MapWithFloatValueDataItem(
          data_name=cls.CONSUMER_NEEDS,
          description=string_manager.get('consumer_needs_description'),
          action_examples=string_manager.get('consumer_needs_example', resource_name=cls.CONSUMER_NEEDS)),
      FloatValueMatrixDataItem(
          data_name=cls.SUPPLIER_TO_CONSUMER,
          description=string_manager.get('supplier_to_consumer_description'),
          action_examples=string_manager.get('supplier_to_consumer_example', resource_name=cls.SUPPLIER_TO_CONSUMER)),
      StringDataItem(
          data_name=cls.OBJECTIVE_FUNCTION,
          description=string_manager.get('objective_function_description'),
          action_examples=string_manager.get('objective_function_example', resource_name=cls.OBJECTIVE_FUNCTION,)),
    ]

    return cls(data_items=data)

  def already_existed_entities(self) -> str:
    if len(self._data_map.get(self.SUPPLIER_AVAILABILITY).data.keys()) == 0:
      return "No entities exist yet."

    text = "Existing suppliers:\n"
    supplier_data = self._data_map.get(self.SUPPLIER_AVAILABILITY)
    for supplier in supplier_data.data.keys():
      text += f"- {supplier}\n"
    text += "Existing consumers:\n"
    consumer_data = self._data_map.get(self.CONSUMER_NEEDS)
    for consumer in consumer_data.data.keys():
      text += f"- {consumer}\n"

    return text


  def validate_model_with_instruction(
      self) -> ModelValidationInstructions | None:
    """
    Method validates the transportation data model and return validation instructions in specified order so
    missing data can be collected step by step.

    Current validation steps:
    1. Validate suppliers exists.
    2. Validate suppliers supply amount exist.
    3. Validate consumers exists.
    4. Validate consumers need amount exist.
    5. Validate cost from each supplier to each consumer exist and is valid.
    6. Validate objective function is defined and valid.

    :return: Method returns instruction objects with instructions for each validation step that need to be consumed during dynamic prompting.
    """

    suppliers = self._data_map.get(self.SUPPLIER_AVAILABILITY)
    providers = self._data_map.get(self.CONSUMER_NEEDS)
    supplier_to_providers = self._data_map.get(self.SUPPLIER_TO_CONSUMER)
    objective_function = self._data_map.get(self.OBJECTIVE_FUNCTION).data

    instruction_model = ModelValidationInstructions(None, None)

    instruction_model.append_instructions(self.__validate_suppliers(suppliers))
    if not instruction_model.is_valid:
      return instruction_model

    instruction_model.append_instructions(self.__validate_providers(providers))
    if not instruction_model.is_valid:
      return instruction_model

    instruction_model.append_instructions(
      self.__validate_supplier_to_providers_cost(supplier_to_providers,
                                                 suppliers, providers))
    if not instruction_model.is_valid:
      return instruction_model

    instruction_model.append_instructions(
      self.__validate_objective_function(objective_function))

    return instruction_model

  def get_model_summary(self) -> str:
    text: str = "Here is the summary of transportation model:\n"

    text += "Suppliers and their availability:\n"
    supplier_data = self._data_map.get(self.SUPPLIER_AVAILABILITY)
    for supplier, amount in supplier_data.data.items():
      text += f"- Supplier {supplier} can supply {amount} items.\n"

    text += "Providers and their needs:\n"
    provider_data = self._data_map.get(self.CONSUMER_NEEDS)
    for provider, need in provider_data.data.items():
      text += f"- Provider {provider} needs {need} items.\n"

    text += "Costs from suppliers to providers:\n"
    cost_data = self._data_map.get(self.SUPPLIER_TO_CONSUMER)
    for supplier, provider_costs in cost_data.data.items():
      for provider, cost in provider_costs.items():
        text += f"- Cost from supplier {supplier} to provider {provider} is {cost}.\n"

    return text



  def __validate_suppliers(self, suppliers) -> list[str]:
    if len(suppliers.data) == 0:
      return [string_manager.get('provide_suppliers')]

    return self._get_empty_validation_instructions(suppliers,
                                                   string_manager.get('provide_suppliers_amount'))

  def __validate_providers(self, providers) -> list[str]:
    if len(providers.data) == 0:
      return [string_manager.get('provide_consumers')]

    return self._get_empty_validation_instructions(providers,
                  string_manager.get('provide_consumer_needs'))

  def __validate_supplier_to_providers_cost(self, supplier_to_providers,
      suppliers, providers) -> list[str]:

    return self.__get_supplier_to_provider_cost_instructions(
        supplier_to_providers, suppliers, providers)

  @staticmethod
  def __validate_objective_function(objective_function) -> list[str]:
    if not objective_function:
      return [string_manager.get('objective_function_instruction')]

    if objective_function.lower() not in ['minimize', 'maximize']:
      return [string_manager.get('objective_function_instruction_wrong')]

    return []

  @staticmethod
  def __get_supplier_to_provider_cost_instructions(
      supplier_to_provider,
      suppliers,
      providers
  ) -> list[str] | None:

    instructions = []

    suppliers_list = suppliers.data.keys()
    providers_list = providers.data.keys()

    for supplier in suppliers_list:
      if supplier not in supplier_to_provider.data:
        instructions.append(
            f"Connection cost between supplier {supplier} and providers need to be given")
        continue

      providers_of_supplier = supplier_to_provider.data[supplier]

      for provider in providers_list:
        if provider not in providers_of_supplier:
          instructions.append(
              f"Cost from supplier {supplier} to provider {provider} need to be given")
          continue
        if not providers_of_supplier[provider] or providers_of_supplier[
          provider] <= 0:
          instructions.append(
              f"Connection cost between supplier {supplier} and provider {provider} has no value")

    return instructions
