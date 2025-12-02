from typing import ClassVar
from models.model_validation import ModelValidationInstructions
from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.dataitem.float_value_matrix_data_item import \
  FloatValueMatrixDataItem
from models.task.datamodel.dataitem.map_data_item import \
  MapWithFloatValueDataItem
from models.task.datamodel.dataitem.string_data_item import StringDataItem


class TransportationDataModel(AbstractDataModel):
  """
  Data model handler for transportation optimization tasks.
  Manages data related to suppliers, consumers, transportation costs, and the objective function.
  1. SUPPLIER_AVAILABILITY: Map of suppliers and their available supply.
  2. CONSUMER_NEEDS: Map of consumers and their required needs.
  3. SUPPLIER_TO_CONSUMER: Matrix of transportation costs from suppliers to consumers.
  4. OBJECTIVE_FUNCTION: String indicating whether to minimize or maximize the objective function
  """

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

  SUPPLIER_AVAILABILITY: ClassVar[str] = "supplier_availability"
  CONSUMER_NEEDS: ClassVar[str] = "consumer_needs"
  SUPPLIER_TO_CONSUMER: ClassVar[str] = "supplier_to_consumer"
  OBJECTIVE_FUNCTION: ClassVar[str] = "objective_function"

  @classmethod
  def create(cls):
    data = [
      MapWithFloatValueDataItem(
          data_name=cls.SUPPLIER_AVAILABILITY,
          description=
          '''
          Use this if user talks about entity that suppose to supply/provide/can produce something in an abstract or specific way. You need to mention supplier name in key1 and the amount of items it can supply in value. If user just mention the supplier without specifying the amount, you can set the value to empty string.
          ''',
          action_examples=
          f"""
      
      Example:    
      User: The warehous Brothers company can supply up to 500 items.
      Result: [(action=UPDATE, resource={cls.SUPPLIER_AVAILABILITY}, key1=Brothers, value=500)]
      
      Example:    
      User: I have the warehous Brothers company.
      Result: [(action=UPDATE, resource={cls.SUPPLIER_AVAILABILITY}, key1=Brothers, value='')]
      
      Example:
      User: I have some warehouses.
      Result: []
      """,
      ),
      MapWithFloatValueDataItem(
          data_name=cls.CONSUMER_NEEDS,
          description=
          '''
          Use this If user talk something about entity that suppose to consume something ot act like a consumer.
          You need to mention consumer name in key1 and the amount of items it consume in value. If user just mention the consumer without specifying the amount, you can set the value to empty string.
          ''',
          action_examples=
          f'''
      Example:    
      User: The ice cream shop Magenta need 500 ice creams.
      Result: [(action=UPDATE, resource={cls.CONSUMER_NEEDS}, key1=Magenta, value=500)]
      
      Example:    
      User: need to be provided to Magenta.
      Result: [(action=UPDATE, resource={cls.CONSUMER_NEEDS}, key1=Magenta, value='')]
      
      Example:
      User: I have some consumers.
      Result: []
          '''
      ),
      FloatValueMatrixDataItem(
          data_name=cls.SUPPLIER_TO_CONSUMER,
          description=
          '''
          Use this if user specify value that explicitly related to one supplier and to one consumer. You need to mention supplier in key1 and consumer in key2, and the value that represent the cost/value in abstract sense from supplier to consumer in value.
          ''',
          action_examples=
          f"""
      Example:    
      User: From Brothers to Megenda costs 23.
      Result: [(action=UPDATE, resource={cls.SUPPLIER_TO_CONSUMER}, key1=Brothers, key2=Magenda, value=23)]
      
      Example:
      User: I have some suppliers to consumers relations.
      Result: []
      """
      ),
      StringDataItem(
          data_name=cls.OBJECTIVE_FUNCTION,
          description=
          """
          Use this when user talk about objective function that he want to achieve. You need to set the value to either "minimize" or "maximize" based on user statement.
          In this case only resource name and the value is needed.
          """,
          action_examples=
          f'''
      Example:    
      User: I want to minimize the cost.
      Result: [(action=UPDATE, resource={cls.OBJECTIVE_FUNCTION}, value='minimize')]
      
      Example:    
      User: I want to maximize the cost.
      Result: [(action=UPDATE, resource={cls.OBJECTIVE_FUNCTION}, value='maximize')]
      
      Example:    
      User: I still thinking about objective function.
      Result: []
      '''
      ),
    ]

    return cls(data_items=data)

  def validate_model_with_instruction(
      self) -> ModelValidationInstructions | None:
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

  def to_mcp_dict(self) -> dict:
    return {
      "task": {
        "supplier_to_supply": self._data_map[self.SUPPLIER_AVAILABILITY].data,
        "consumer_to_consume": self._data_map[self.CONSUMER_NEEDS].data,
        "supplier_to_consumer_cost": self._data_map[
          self.SUPPLIER_TO_CONSUMER].data,
        "objective_function": self._data_map[self.OBJECTIVE_FUNCTION].data
      }
    }



  def __validate_suppliers(self, suppliers) -> list[str]:
    if len(suppliers.data) == 0:
      return [
        "List of suppliers need to be provided first. At leas one suppler need to be provided"]

    return self._get_empty_validation_instructions(suppliers,
                                                   "User need to provide amount of items for supplier")

  def __validate_providers(self, providers) -> list[str]:
    if len(providers.data) == 0:
      return [
        "List of consumers need to be provided first. At leas one consumer need to be provided"]

    return self._get_empty_validation_instructions(providers,
                                                   "Amount of items need to be consumed for consumer")

  def __validate_supplier_to_providers_cost(self, supplier_to_providers,
      suppliers, providers) -> list[str]:
    if len(supplier_to_providers.data) == 0:
      return [
        "Now cost of relation from each supplier to provider need to be provided"]

    return self.__get_supplier_to_provider_cost_instructions(
        supplier_to_providers, suppliers, providers)

  @staticmethod
  def __validate_objective_function(objective_function) -> list[str]:
    if not objective_function:
      return [
        "Objective function need to be defined. User must select if he want to minimize or maximize."]

    if objective_function.lower() not in ['minimize', 'maximize']:
      return [
        f"Objective function value {objective_function} is not valid. It must be either minimize or maximize."]

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
