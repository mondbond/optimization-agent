from typing import ClassVar

from models.model_validation import ModelValidation
from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.dataitem.data_item import AbstractDataItem
from models.task.datamodel.dataitem.float_value_matrix_data_item import \
  FloatValueMatrixDataItem
# from models.task.datamodel.dataitem.float_value_matrix_data_item import \
#   FloatValueMatrixDataItem
from models.task.datamodel.dataitem.map_data_item import \
  MapWithFloatValueDataItem
from models.task.datamodel.dataitem.string_data_item import StringDataItem
from models.task.datamodel.dataitem.string_list_data_item import \
  StringListDataItem


# from models.task.datamodel.dataitem.string_data_item import StringDataItem


class BlendDataModel(AbstractDataModel):
  MATERIAL_TO_COST: ClassVar[str] = "material_to_cost"
  COMPOSITIONS: ClassVar[str] = "composition"
  MATERIAL_TO_COMPOSITIONS_COST: ClassVar[str] = "material_to_compositions_cost"
  PRODUCTS_COMPOSITIONS: ClassVar[str] = "product_composition_demand"

  OBJECTIVE_FUNCTION: ClassVar[str] = "objective_function"

  @classmethod
  def create(cls):
    data = [
      MapWithFloatValueDataItem(
          data_name=cls.MATERIAL_TO_COST,
          description='This is the map for material that need to be procured. The key value is a name of material always a string and the value is cost of procuring one unit of this material',
          action_examples=f'action=UPDATE. object={cls.MATERIAL_TO_COST}. key=name of the material. value=cost of procuring one unit of this material'
      ),
      StringListDataItem(
          data_name=cls.COMPOSITIONS,
          description='This is a list of compositions of that can be created. The key value is always empty and value is always string. No need keys here. ONly resource and value',
          action_examples=f'action=UPDATE. object={cls.COMPOSITIONS}.  value= name of the composition key is empty and key2 is always empty'
      ),
      FloatValueMatrixDataItem(
          data_name=cls.MATERIAL_TO_COMPOSITIONS_COST,
          description='This is a matrix that shows cost of using certain compositions in certain material. Use it when user gives a material and composition and value. The key1 value is a name of material always a string and the key2 is name of composition always a string. The value is cost of using one unit of material in one unit of composition',
          action_examples=f'action=UPDATE. object={cls.MATERIAL_TO_COMPOSITIONS_COST}. key=name of the material. key2= name of the composition. value= float value of the cost'
      ),
      MapWithFloatValueDataItem(
          data_name=cls.PRODUCTS_COMPOSITIONS,
          description="This is the map of the composition needed for product and it's percentage of demand that need to be fulfilled. The key is a name of composition always a string and the value. Key and value only needed here.",
          action_examples=f'action=UPDATE. object={cls.PRODUCTS_COMPOSITIONS}. key=specified composition. ket2= None. value=number specified by user'
      ),
      StringDataItem(
          data_name=cls.OBJECTIVE_FUNCTION,
          description=f"This is the value of  {cls.OBJECTIVE_FUNCTION} with value that represents the objective function of the blending task. The value is either minimize or maximize. It does not require keys.",
          action_examples=f'action=UPDATE. object={cls.OBJECTIVE_FUNCTION}. value=minimise ot maximize only'
      ),
    ]
    return cls(data_items=data)

  def get_model_summary(self) -> str:
    text: str = "Here is the summary of the current data model state:\n"

    text += f"Material to Cost:\n"
    material_to_cost = self._data_map.get(self.MATERIAL_TO_COST)
    for material, cost in material_to_cost.data.items():
      text += f"- Material: {material}, Cost per unit: {cost}\n"

    text += f"Compositions:\n"
    compositions = self._data_map.get(self.COMPOSITIONS)
    for composition in compositions.data:
      text += f"- Composition: {composition}\n"

    text += f"Material to Compositions Cost:\n"
    material_to_compositions_cost = self._data_map.get(
      self.MATERIAL_TO_COMPOSITIONS_COST)
    for material, compositions in material_to_compositions_cost.data.items():
      for composition, cost in compositions.items():
        text += f"- Material: {material}, Composition: {composition}, Cost: {cost}\n"

    text += f"Composition to Demands:\n"
    composition_to_demands = self._data_map.get(self.PRODUCTS_COMPOSITIONS)
    for composition, demand in composition_to_demands.data.items():
      text += f"- Composition: {composition}, Demand Percentage: {demand}\n"

    return text

  def get_objective_function(self) -> str | None:
    return "minimize"

  def validate_model_with_text_response(self) -> ModelValidation:
    materials = self._data_map.get(self.MATERIAL_TO_COST)
    compositions = self._data_map.get(self.COMPOSITIONS)

    material_to_compositions = self._data_map.get(
      self.MATERIAL_TO_COMPOSITIONS_COST)
    composition_to_demands = self._data_map.get(self.PRODUCTS_COMPOSITIONS)

    # material
    if len(materials.data) == 0:
      return ModelValidation(["At least one material must be provided."], None)

    materials_rules = self._get_empty_validation_rules(materials,
                                                       "User need to provide cost for material.")
    if len(materials_rules) > 0:
      return ModelValidation(materials_rules, None)

    # composition
    if len(compositions.data) == 0:
      return ModelValidation(["At least one composition must be provided."],
                             None)

    # material to composition matrix
    if len(material_to_compositions.data) == 0:
      return ModelValidation(
          ["Now user must specify all compositions for each material."], None)

    materials_to_composition_rules = self._get_materials_to_composition(
        material_to_composition=material_to_compositions,
        materials=materials,
        compositions=compositions
    )
    if len(materials_to_composition_rules) > 0:
      return ModelValidation(materials_to_composition_rules, None)

    if len(composition_to_demands.data) == 0:
      return ModelValidation(
          ["Now user need to provide percentage of each composition in a new product."],
          None)

    composition_to_demands_rules = self._get_empty_validation_rules(
      composition_to_demands,
      "User need to provide demand in a new product for composition .")
    if len(composition_to_demands_rules) > 0:
      return ModelValidation(composition_to_demands_rules, None)

    objective_function = self._data_map.get(self.OBJECTIVE_FUNCTION).data
    if not objective_function:
      return ModelValidation(
          ["Objective function need to be defined. User must select if he want to minimize or maximize."],
          None)

    if objective_function.lower() not in ['minimize', 'maximize']:
      return ModelValidation(None,
                             [f"Objective function value {objective_function} is not valid. It must be either minimize or maximize."])

    return ModelValidation(None, None)

  def to_mcp_dict(self) -> dict:
    return {
      "blending_task": {
        "material_to_cost": self._data_map[self.MATERIAL_TO_COST].data,
        "composition_constraint": self._data_map[
          self.PRODUCTS_COMPOSITIONS].data,
        "materials_to_composition": self._data_map[
          self.MATERIAL_TO_COMPOSITIONS_COST].data,
        "objective_function": self._data_map[self.OBJECTIVE_FUNCTION]
      }
    }

  @staticmethod
  def _get_materials_to_composition(material_to_composition: AbstractDataItem,
      materials: AbstractDataItem,
      compositions: AbstractDataItem
  ) -> list[str] | None:

    rules = []

    materials_list = list(materials.data.keys())
    composition_list = compositions.data

    for material in materials_list:
      if material not in material_to_composition.data.keys():
        rules.append(f"All compositions for {material} need to be given")
        continue

      compositon_to_values = material_to_composition.data[material]

      for composition in composition_list:
        if composition not in compositon_to_values.keys():
          rules.append(
            f"Composition {composition} for {material} need to be provided")
          continue
        if not compositon_to_values[composition] or compositon_to_values[
          composition] <= 0:
          rules.append(
            f"Composition {composition} for {material} need to be a valid value greater than zero")

    return rules
