from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

from models.model_validation import ModelValidation
from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.dataitem.data_item import AbstractDataItem
from typing import ClassVar

from models.task.datamodel.dataitem.float_value_matrix_data_item import \
  FloatValueMatrixDataItem
# from models.task.datamodel.dataitem.float_value_matrix_data_item import \
#   FloatValueMatrixDataItem
from models.task.datamodel.dataitem.map_data_item import \
  MapWithFloatValueDataItem
from models.task.datamodel.dataitem.string_data_item import StringDataItem


# from models.task.datamodel.dataitem.string_data_item import StringDataItem


class TransportationDataModel(AbstractDataModel):

  # todo why classVar
  SUPPLIER_AVAILABILITY : ClassVar[str] = "supplier_availability"
  CONSUMER_NEEDS : ClassVar[str] = "consumer_needs"
  SUPPLIER_TO_CONSUMER : ClassVar[str] = "supplier_to_consumer"
  OBJECTIVE_FUNCTION : ClassVar[str] = "objective_function"


  # why not use __init__
  @classmethod
  def create(cls):

    data = [
      MapWithFloatValueDataItem(
          data_name = cls.SUPPLIER_AVAILABILITY,
          description = 'if user talk something about entity that suppose to supply something',
          action_examples = f'''User: The warehous Brothers company can supply up to 500 items.
      Result: [(action=UPDATE, resource={cls.SUPPLIER_AVAILABILITY}, key1=Brothers company, value=500)]''',
      ),
      MapWithFloatValueDataItem(
          data_name = cls.CONSUMER_NEEDS,
          description ='if user talk something about entity that suppose to consume something ot act like a consumers',
          action_examples = f'''
          User: The Grandma Icecream shop need 200 items
      Result: [(action=UPDATE, resource={cls.CONSUMER_NEEDS}, key1=Grandma Icecream, value=200)]
          '''
      ),
      FloatValueMatrixDataItem(
          data_name = cls.SUPPLIER_TO_CONSUMER,
          description = 'if user specify value that explicitly related to one supplier to one consumer. You need to mention supplier in key1 and consumer in key2',
          action_examples=f'''
user: The cost of transportation from Brothers company to Grandma Icecream is 2312
      Result: [(action=UPDATE, resource={cls.SUPPLIER_TO_CONSUMER}, key1=Brothers company, key2=Grandma Icecream  value=500)]
'''),
      StringDataItem(
          data_name=cls.OBJECTIVE_FUNCTION,
          description=f"This is the value of  {cls.OBJECTIVE_FUNCTION} with value that represents the objective function of the blending task. The value is either minimize or maximize. It does not require keys.",
          action_examples=f'action=UPDATE. object={cls.OBJECTIVE_FUNCTION}. value=minimise ot maximize only'
      ),
    ]

    return cls(data_items=data)


  def validate_model_with_text_response(self) -> ModelValidation | None:
    # explain the order of validation is important in comment

    suppliers = self._data_map.get(self.SUPPLIER_AVAILABILITY)
    providers = self._data_map.get(self.CONSUMER_NEEDS)
    supplier_to_providers = self._data_map.get(self.SUPPLIER_TO_CONSUMER)

    if len(suppliers.data) == 0:
      return ModelValidation(["List of suppliers need to be provided first. At leas one suppler need to be provided"], None)

    suppliers_rules = self._get_empty_validation_rules(suppliers, "User need to provide amount of items for supplier")
    if len(suppliers_rules) > 0:
      return ModelValidation(suppliers_rules, None)


    if len(providers.data) == 0:
      return ModelValidation(["List of consumers need to be provided first. At leas one consumer need to be provided"], None)

    providers_rules = self._get_empty_validation_rules(providers, "Amount of items need to be consumed for consumer")
    if len(providers_rules) > 0:
      return ModelValidation(providers_rules, None)


    if len(supplier_to_providers.data) == 0:
      return ModelValidation(["Now cost of relation from each supplier to provider need to be provided"], None)

    supplier_to_providers_rules = self._get_supplier_to_provider_cost_rules(supplier_to_providers, suppliers, providers)
    if len(supplier_to_providers_rules) > 0:
      return ModelValidation(None, supplier_to_providers_rules)

    objective_function = self._data_map.get(self.OBJECTIVE_FUNCTION).data
    if not objective_function:
      return ModelValidation(["Objective function need to be defined. User must select if he want to minimize or maximize."], None)

    if objective_function.lower() not in ['minimize', 'maximize']:
      return ModelValidation([f"Objective function value {objective_function} is not valid. It must be either minimize or maximize."], None)


    return ModelValidation(None, None)


  def get_model_summary(self) -> str:
    text : str = "Here is the summary of transportation model:\n"

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

  @staticmethod
  def _get_supplier_to_provider_cost_rules(supplier_to_provider: AbstractDataItem,
      suppliers: AbstractDataItem,
      providers: AbstractDataItem
  ) -> list[str] | None:

    rules = []

    suppliers_list = suppliers.data.keys()
    providers_list = providers.data.keys()

    for supplier in suppliers_list:
      if supplier not in supplier_to_provider.data:
        rules.append(f"Connection cost between supplier {supplier} and providers need to be given")
        continue

      providers_of_supplier = supplier_to_provider.data[supplier]

      for provider in providers_list:
        if provider not in providers_of_supplier:
          rules.append(f"Cost from supplier {supplier} to provider {provider} need to be given")
          continue
        if not providers_of_supplier[provider] or providers_of_supplier[provider] <= 0:
          rules.append(f"Connection cost between supplier {supplier} and provider {provider} has no value")

    return rules

  def to_mcp_dict(self) -> dict:
    return {
      "linear_transportation_task": {
      "supplier_to_supply": self._data_map[self.SUPPLIER_AVAILABILITY].data,
      "consumer_to_consume": self._data_map[self.CONSUMER_NEEDS].data,
      "supplier_to_consumer_cost": self._data_map[self.SUPPLIER_TO_CONSUMER].data,
      "objective_function" : self._data_map[self.OBJECTIVE_FUNCTION].data
      }
    }

if __name__ == "__main__":
  model = TransportationDataModel.create()

  model.update_data(TransportationDataModel.SUPPLIER_AVAILABILITY, "A", 700)
  model.update_data(TransportationDataModel.SUPPLIER_AVAILABILITY, "B", 1100)

  model.update_data(TransportationDataModel.CONSUMER_NEEDS, "X", 150)
  model.update_data(TransportationDataModel.CONSUMER_NEEDS, "Y", 400)

  model.update_data(TransportationDataModel.SUPPLIER_TO_CONSUMER, key="A", key2="X", value=4)
  model.update_data(TransportationDataModel.SUPPLIER_TO_CONSUMER, key="A", key2="Y", value=3)
  model.update_data(TransportationDataModel.SUPPLIER_TO_CONSUMER, key="B", key2="X", value=12)
  model.update_data(TransportationDataModel.SUPPLIER_TO_CONSUMER, key="B", key2="Y", value=1)

  validation = model.validate_model_with_text_response()


  print(validation.is_valid)
  print(validation.rules_for_prompt)
  print(validation.rules_for_injections)

  tool_dict = model.to_mcp_dict()


  mcp_url = "http://0.0.0.0:8777/mcp"


  mcp_client = None

  # http://mond_mcp:8887/mcp
  if mcp_url is not None and mcp_url != "":
    mcp_client = MultiServerMCPClient(
        {
          "optimizator_mcp": {
            "transport": "streamable_http",
            "url": mcp_url,
          }
        }
    )

  async def main():
    tools = await mcp_client.get_tools()
    print(tools)

    result = await tools[0].coroutine(**tool_dict)
    print(result)

  asyncio.run(main())


