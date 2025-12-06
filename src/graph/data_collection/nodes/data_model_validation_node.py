from graph.data_collection.state.data_collection_state import \
  DataPopulationState

# todo: comments to all nodes
def data_model_validation(state: DataPopulationState):
  state['model_validation'].populate(state['optimization_data_model']
                                                         .validate_model_with_instruction())

  if state['model_validation'].is_valid:
    state['model_validation'].add_orders(["The data model has been successfully fulfilled and is ready for optimization."])

  return {
    'route': 'next',
    'model_validation': state['model_validation'],
  }

