from typing import ClassVar

from models.model_validation import ConversationInstructions
from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.dataitem.float_value_matrix_data_item import \
  FloatValueMatrixDataItem
from models.task.datamodel.dataitem.map_data_item import \
  MapWithFloatValueDataItem
from models.task.datamodel.dataitem.string_data_item import StringDataItem
from models.task.datamodel.dataitem.string_list_data_item import \
  StringListDataItem
from utils import string_manager


class BlendDataModel(AbstractDataModel):
  """
  Data model handler for blending optimization tasks.
  Manages data related to materials, compositions, costs, and the objective function.
  1. MATERIAL_TO_COST: Map of materials and their procurement costs.
  2. COMPOSITIONS: List of available compositions.
  3. MATERIAL_TO_COMPOSITIONS_COST: Matrix of costs for using compositions in materials.
  4. PRODUCTS_COMPOSITIONS: Map of compositions and their demand percentages for new products.
  5. OBJECTIVE_FUNCTION: String indicating whether to minimize or maximize the objective function
  """

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
          description=string_manager.get("material_to_cost_description"),
          action_examples=string_manager.get("material_to_cost_examples", resource_name=cls.MATERIAL_TO_COST)),

      StringListDataItem(
          data_name=cls.COMPOSITIONS,
          description=string_manager.get("composition_list_description"),
          action_examples=string_manager.get("composition_list_examples", resource_name=cls.COMPOSITIONS)),

      FloatValueMatrixDataItem(
          data_name=cls.MATERIAL_TO_COMPOSITIONS_COST,
          description=string_manager.get("material_to_compositions_cost_description"),
          action_examples=string_manager.get("material_to_compositions_cost_examples", resource_name=cls.MATERIAL_TO_COMPOSITIONS_COST)),

      MapWithFloatValueDataItem(
          data_name=cls.PRODUCTS_COMPOSITIONS,
          description=string_manager.get("products_compositions_description"),
          action_examples=string_manager.get("products_compositions_examples", resource_name=cls.PRODUCTS_COMPOSITIONS)),

      StringDataItem(
          data_name=cls.OBJECTIVE_FUNCTION,
          description=string_manager.get('objective_function_description'),
          action_examples=string_manager.get('objective_function_example', resource_name=cls.OBJECTIVE_FUNCTION,)),
    ]
    return cls(data_items=data)

  def get_model_summary(self) -> str:
    text: str = "Here is the summary of the current data model state:\n"

    text += "Material to Cost:\n"
    material_to_cost = self._data_map.get(self.MATERIAL_TO_COST)
    for material, cost in material_to_cost.data.items():
      text += f"- Material: {material}, Cost per unit: {cost}\n"

    text += "Compositions:\n"
    compositions = self._data_map.get(self.COMPOSITIONS)
    for composition in compositions.data:
      text += f"- Composition: {composition}\n"

    text += "Material to Compositions Cost:\n"
    material_to_compositions_cost = self._data_map.get(
      self.MATERIAL_TO_COMPOSITIONS_COST)
    for material, compositions in material_to_compositions_cost.data.items():
      for composition, cost in compositions.items():
        text += f"- Material: {material}, Composition: {composition}, Cost: {cost}\n"

    text += "Composition to Demands:\n"
    composition_to_demands = self._data_map.get(self.PRODUCTS_COMPOSITIONS)
    for composition, demand in composition_to_demands.data.items():
      text += f"- Composition: {composition}, Demand Percentage: {demand}\n"

    return text


  def validate_model_with_instruction(self) -> ConversationInstructions:
    materials = self._data_map.get(self.MATERIAL_TO_COST)
    compositions = self._data_map.get(self.COMPOSITIONS)


    material_to_compositions = self._data_map.get(
      self.MATERIAL_TO_COMPOSITIONS_COST)
    composition_to_demands = self._data_map.get(self.PRODUCTS_COMPOSITIONS)

    objective_function = self._data_map.get(self.OBJECTIVE_FUNCTION).data

    instructions_model = ConversationInstructions.create_empty()

    instructions_model.add_prompt_missed_data_instructions(self.__validate_materials(materials))
    if not instructions_model.is_data_model_comlete:
      return instructions_model

    instructions_model.add_prompt_missed_data_instructions(self.__validate_compositions(compositions))
    if not instructions_model.is_data_model_comlete:
      return instructions_model

    instructions_model.add_prompt_missed_data_instructions(self.__validate_materials_to_compositions(material_to_compositions, materials, compositions))
    if not instructions_model.is_data_model_comlete:
      return instructions_model

    instructions_model.add_prompt_missed_data_instructions(self.__validate_compositions_to_demands(composition_to_demands))
    if not instructions_model.is_data_model_comlete:
      return instructions_model

    instructions_model.add_prompt_missed_data_instructions(self.__validate_objective_function(objective_function))

    return instructions_model

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

  def already_existed_entities(self) -> str:
    if len(self._data_map.get(self.MATERIAL_TO_COST).data.keys()) == 0:
      return "No entities exist yet."

    text = "Already existing materials:\n"
    material_to_cost = self._data_map.get(self.MATERIAL_TO_COST)
    for material in material_to_cost.data.keys():
      text += f"- {material}\n"
    text += "Already existing compositions:\n"
    compositions = self._data_map.get(self.COMPOSITIONS)
    for composition in compositions.data:
      text += f"- {composition}\n"

    return text




  def __validate_materials(self, materials) -> list[str]:
    if len(materials.data) == 0:
      return [string_manager.get("empty_materials")]

    return self._get_empty_validation_instructions(materials,
                                                              "User need to provide cost for material.")

  @staticmethod
  def __validate_compositions(compositions) -> list[str]:
    if len(compositions.data) == 0:
      return [string_manager.get("empty_compositions")]

    return []

  def __validate_materials_to_compositions(self, material_to_compositions,
      materials,
      compositions) -> list[str]:
    # if len(material_to_compositions.data) == 0:
    #   return ["Now user must specify all compositions for each material."]

    return self.__get_materials_to_composition_instructions(
        material_to_composition=material_to_compositions,
        materials=materials,
        compositions=compositions
    )

  def __validate_compositions_to_demands(self, composition_to_demands) -> list[str]:
    # if len(composition_to_demands.data) == 0:
    #   return ["Now user need to provide percentage of each composition in a new product."]

    return self._get_empty_validation_instructions(
        composition_to_demands,
        "User need to provide demand in a new product for composition .")

  def __validate_objective_function(self, objective_function) -> list[str]:
    if not objective_function:
      return ["Objective function need to be defined. User must select if he want to minimize or maximize."]

    if objective_function.lower() not in ['minimize', 'maximize']:
      return [f"Objective function value {objective_function} is not valid. It must be either minimize or maximize."]

    return []



  @staticmethod
  def __get_materials_to_composition_instructions(material_to_composition,
      materials,
      compositions
  ) -> list[str] | None:

    instructions = []

    materials_list = list(materials.data.keys())
    composition_list = compositions.data

    for material in materials_list:
      if material not in material_to_composition.data.keys():
        instructions.append(f"All compositions for {material} need to be given")
        continue

      compositon_to_values = material_to_composition.data[material]

      for composition in composition_list:
        if composition not in compositon_to_values.keys():
          instructions.append(
            f"Composition {composition} for {material} need to be provided")
          continue
        if not compositon_to_values[composition] or compositon_to_values[
          composition] <= 0:
          instructions.append(
            f"Composition {composition} for {material} need to be a valid value greater than zero")

    return instructions
