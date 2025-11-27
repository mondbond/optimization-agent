from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.data_item import DataItem


class BlendDataModel(AbstractDataModel):

  def __init__(self):
    data = [
      DataItem(
          'supplier_availability',
          {},
          'map'
          'This is a map for supplier that can produce something. The key value is a name of supplier always a string and the value is amount of items it can supply',
          'action=add. object=supplier_availability. key=name of the supplier. value=number of availability'
      ),
      DataItem(
          'consumer_needs',
          {},
          'map'
          'This is a map for consumer that need something. The key value is a name of consumer. The kay value is the amount (number) that is need something',
          'action=add. object=consumer_needs. key = name of consumer.  value=number of needs'
      ),
      DataItem(
          'supplier_to_consumer',
          {},
          'matrix'
          'This is a map of maps. It represent relation between supplier and providers. First value is supplier, second is consumer. Value of embedded map is an number.',
          'action=add. object=supplier_to_consumer. key1=name of the supplier. key2=name of the consumer.  value=some value'
      )
    ]

    super().__init__(data)

  def validate_model_with_text_response(self) -> str:
    raise NotImplementedError()
