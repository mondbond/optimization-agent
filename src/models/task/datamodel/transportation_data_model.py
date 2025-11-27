from pydantic_settings.sources import providers

from models.model_validation import ModelValidation
from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.data_item import DataItem
from typing import ClassVar


class TransportationDataModel(AbstractDataModel):

  SUPPLIER_AVAILABILITY : ClassVar[str] = "supplier_availability"
  CONSUMER_NEEDS : ClassVar[str] = "consumer_needs"
  SUPPLIER_TO_CONSUMER : ClassVar[str] = "supplier_to_consumer"

  @classmethod
  def create(cls):

    data = [
      DataItem(
          data_name = cls.SUPPLIER_AVAILABILITY,
          data = {},
          data_type = 'map',
          description = 'if user talk something about entity that suppose to supply something',
          action_examples = f'''User: The warehous Brothers company can supply up to 500 items.
      Result: [(action=UPDATE, resource={cls.SUPPLIER_AVAILABILITY}, key1=Brothers company, value=500)]''',

      ),
      DataItem(
          data_name = cls.CONSUMER_NEEDS,
          data = {},
          data_type = 'map',
          description ='if user talk something about entity that suppose to consume something',
          action_examples = f'''
          User: The Grandma Icecream shop need 200 items
      Result: [(action=UPDATE, resource={cls.CONSUMER_NEEDS}, key1=Grandma Icecream, value=200)]
          '''
      ),
      DataItem(
          data_name = cls.SUPPLIER_TO_CONSUMER,
          data = {},
          data_type = 'matrix',
          description = 'if user specify value that explicitly related to one supplier to one consumer. You need to mention supplier in key1 and consumer in key2',
          action_examples=f'''
user: The cost of transportation from Brothers company to Grandma Icecream is 2312
      Result: [(action=UPDATE, resource={cls.SUPPLIER_TO_CONSUMER}, key1=Brothers company, key2=Grandma Icecream  value=500)]
''')]

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
      return ModelValidation(["List of providers need to be provided first. At leas one provider need to be provided"], None)

    providers_rules = self._get_empty_validation_rules(providers, "Amount of items need to be provided for provider")
    if len(providers_rules) > 0:
      return ModelValidation(providers_rules, None)


    if len(supplier_to_providers.data) == 0:
      return ModelValidation(["Now cost of relation from each supplier to provider need to be provided"], None)

    supplier_to_providers_rules = self._get_supplier_to_provider_cost_rules(supplier_to_providers, suppliers, providers)
    if len(supplier_to_providers_rules) > 0:
      return ModelValidation(None, supplier_to_providers_rules)

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
  def _get_supplier_to_provider_cost_rules(supplier_to_provider: DataItem,
      suppliers: DataItem,
      providers: DataItem
  ) -> list[str] | None:

    rules = []

    suppliers_list = suppliers.data.keys()
    providers_list = providers.data.keys()

    for supplier in suppliers_list:
      if supplier not in supplier_to_provider.data:
        rules.append(f"Connection cost between supplier {supplier} and providers need to be given")
        continue
      for provider in providers_list:
        rules.append(f"Cost from supplier {supplier} to provider {provider} need to be given")
        continue
        if not provider.data[supplier][provider]:
          rules.append(f"Connection cost between supplier {supplier} and provider {provider} has no value")

    return rules


if __name__ == "__main__":
  model = TransportationDataModel()

  model.update_data(TransportationDataModel.SUPPLIER_AVAILABILITY, "A", 100)
  model.update_data(TransportationDataModel.SUPPLIER_AVAILABILITY, "B", 200)

  model.update_data(TransportationDataModel.CONSUMER_NEEDS, "X", 150)
  model.update_data(TransportationDataModel.CONSUMER_NEEDS, "Y", None)

  model.update_data(TransportationDataModel.SUPPLIER_TO_CONSUMER, key="A", key2="X", value=4)

  validation = model.validate_model_with_text_response()

  print(validation.is_valid)
  print(validation.rules_for_prompt)
  print(validation.rules_for_injections)
