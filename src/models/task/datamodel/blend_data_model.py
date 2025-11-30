from models.model_validation import ModelValidation
from models.task.datamodel.abstract_data_model import AbstractDataModel
from models.task.datamodel.dataitem.data_item import DataItem
from typing import ClassVar

class BlendDataModel(AbstractDataModel):

  MATERIAL_TO_COST : ClassVar[str] = "consumer_to_costs"
  COMPOSITIONS : ClassVar[str] = "compositions"
  MATERIAL_TO_COMPOSITIONS_COST : ClassVar[str] = "material_to_compositions_cost"
  COMPOSITON_TO_DEMANDS : ClassVar[str] = "composition_to_demands"

  OBJECTIVE_FUNCTION : ClassVar[str] = "objective_function"

  @classmethod
  def create(cls):
    data = [
      DataItem(
          data_name=cls.MATERIAL_TO_COST,
          data={},
          data_type='map',
          value_type='float',
          description='This is the map for material that need to be procured. The key value is a name of material always a string and the value is cost of procuring one unit of this material',
          action_examples=f'action=UPDATE. object={cls.MATERIAL_TO_COST}. key=name of the material. value=cost of procuring one unit of this material'
      ),
      DataItem(
          data_name=cls.COMPOSITIONS,
          data={},
          data_type='map',
          value_type='float',
          description='This is a map of compositions of the materials that can be created. The key value is a name of composition always a string.',
          action_examples=f'action=UPDATE. object={cls.COMPOSITIONS}. key=name of the composition. value=not needed'
      ),
      DataItem(
          data_name=cls.MATERIAL_TO_COMPOSITIONS_COST,
          data={},
          data_type='matrix',
          value_type='float',
          description='This is a matrix that shows cost of using certain compositions in certain material. The key1 value is a name of material always a string and the key2 is name of composition always a string. The value is cost of using one unit of material in one unit of composition',
          action_examples=f'action=UPDATE. object={cls.MATERIAL_TO_COMPOSITIONS_COST}. key=name of the material. key2= name of the composition. value= float value of the cost'
      ),
      DataItem(
          data_name=cls.COMPOSITON_TO_DEMANDS,
          data={},
          data_type='map',
          value_type='float',
          description="This is the map of the composition and it's percentage of demand that need to be fulfilled. The key value is a name of composition always a string and the value is percentage of demand that need to be fulfilled for this composition represented as float between 0 and 100",
          action_examples=f'action=UPDATE. object={cls.COMPOSITON_TO_DEMANDSO}. key=name of the composition. value=percentage of demand that need to be fulfilled represented as float between 0 and 100'
      ),
      DataItem(
          data_name=cls.OBJECTIVE_FUNCTION,
          data="",
          data_type='string',
          value_type='string',
          description=f"This is the value of  {cls.OBJECTIVE_FUNCTION} with value that represents the objective function of the blending task. The value is either minimize or maximize. It does not require keys.",
          action_examples=f'action=UPDATE. object={cls.COMPOSITON_TO_DEMANDSO}. value=minimise ot maximize only'
      ),
    ]
    return cls(data_items=data)

  def get_model_summary(self) -> str:
    text: str = "Here is the summary of the current data model state:\n"

    text+=f"Material to Cost:\n"
    material_to_cost = self._data_map.get(self.MATERIAL_TO_COST)
    for material, cost in material_to_cost.data.items():
      text+=f"- Material: {material}, Cost per unit: {cost}\n"

    text+=f"Compositions:\n"
    compositions = self._data_map.get(self.COMPOSITIONS)
    for composition in compositions.data.keys():
      text+=f"- Composition: {composition}\n"

    text+=f"Material to Compositions Cost:\n"
    material_to_compositions_cost = self._data_map.get(self.MATERIAL_TO_COMPOSITIONS_COST)
    for material, compositions in material_to_compositions_cost.data.items():
      for composition, cost in compositions.items():
        text+=f"- Material: {material}, Composition: {composition}, Cost: {cost}\n"

    text+=f"Composition to Demands:\n"
    composition_to_demands = self._data_map.get(self.COMPOSITON_TO_DEMANDS)
    for composition, demand in composition_to_demands.data.items():
      text+=f"- Composition: {composition}, Demand Percentage: {demand}\n"

    return text

  def get_objective_function(self) -> str | None:
    return "minimize"

  def validate_model_with_text_response(self) -> ModelValidation:
    materials = self._data_map.get(self.MATERIAL_TO_COST)
    compositions = self._data_map.get(self.COMPOSITIONS)

    material_to_compositions = self._data_map.get(self.MATERIAL_TO_COMPOSITIONS_COST)
    composition_to_demands = self._data_map.get(self.COMPOSITON_TO_DEMANDS)

    # material
    if len(materials.data) == 0:
      return ModelValidation(["At least one material must be provided."], None)

    materials_rules = self._get_empty_validation_rules(materials, "User need to provide cost for material.")
    if len(materials_rules) > 0:
      return ModelValidation(materials_rules, None)

    # composition
    if len(compositions.data) == 0:
      return ModelValidation(["At least one composition must be provided."], None)


    # material to composition matrix
    if len(material_to_compositions.data) == 0:
      return ModelValidation(["Now user must specify all compositions for each material."], None)

    materials_to_composition_rules = self._get_materials_to_composition(
        material_to_composition=material_to_compositions,
        materials=materials,
        composition=compositions
    )
    if len(materials_to_composition_rules) > 0:
      return ModelValidation(materials_to_composition_rules, None)



    if len(composition_to_demands.data) == 0:
      return ModelValidation(["Now user need to provide percentage of each composition in a new product."], None)

    composition_to_demands_rules = self._get_empty_validation_rules(composition_to_demands, "User need to provide demand in a new product for composition .")
    if len(composition_to_demands_rules) > 0:
      return ModelValidation(composition_to_demands_rules, None)


    objective_function = self.get_objective_function()
    if not objective_function:
      return ModelValidation(None, ["Objective function must be defined (minimize or maximize)."])

    return ModelValidation(None, None)

  def to_mcp_dict(self) -> dict:
    return {
      "blending_task": {
        "material_to_cost": self._data_map[self.MATERIAL_TO_COST].data,
        "composition_constraint": self._data_map[self.COMPOSITON_TO_DEMANDS].data,
        "materials_to_composition": self._data_map[self.MATERIAL_TO_COMPOSITIONS_COST].data,
        "objective_function" : self._get_objective_function()
      }
    }

  @staticmethod
  def _get_materials_to_composition(material_to_composition: DataItem,
      materials: DataItem,
      composition: DataItem
  ) -> list[str] | None:

    rules = []

    materials_list = materials.data.keys()
    composition_list = composition.data.keys()

    for material in materials_list:
      if material not in material_to_composition.data:
        rules.append(f"All compositions for {material} need to be given")
        continue

      material_to_composition = material_to_composition.data[material]

      for composition in composition_list:
        if composition not in material_to_composition:
          rules.append(f"Composition {composition} for {material} need to be provided")
          continue
        if not material_to_composition[composition] or material_to_composition[composition] <= 0:
          rules.append(f"Composition {composition} for {material} need to be a valid value greater than zero")

    return rules

