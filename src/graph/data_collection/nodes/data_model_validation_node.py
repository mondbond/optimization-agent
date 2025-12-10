from graph.data_collection.state.data_collection_state import \
  DataPopulationState

def data_model_validation(state: DataPopulationState):
  """
  Third step of data collection subgraph process.
  Validate the optimization data model after population.
  If the data model is complete, add a success instruction.
  Otherwise, the validation instructions will guide the user to provide missing data.
  """

  state['model_validation'].merge_with(state['optimization_data_model']
                                       .validate_model_with_instruction())

  if state['model_validation'].is_data_model_comlete:
    state['model_validation'].add_prompt_instructions(["The data model has been successfully fulfilled and is ready for optimization."])

  return {
    'route': 'next',
    'model_validation': state['model_validation'],
  }

