from langgraph.constants import START, END
from langgraph.graph import StateGraph

from graph.data_collection.nodes.extract_data_node import extract_data
from graph.data_collection.nodes.data_model_population_node import \
  data_model_population
from graph.data_collection.nodes.data_model_validation_node import \
  data_model_validation
from graph.data_collection.state.data_collection_state import \
  DataPopulationState
from models.model_validation import ConversationInstructions


class DataCollectionAgent:
  """
  Agent that orchestrates the data collection process using a state graph.
  It manages the flow of data extraction, population, and validation through defined nodes.

  Subagent take data model and conversation history as input and process them through a series of nodes to extract.
  It returns the updated data model after going through the data collection process and validation instructions to translated to user after.
  """

  EXTRACTION_NODE = "EXTRACTION_NODE"
  POPULATION_NODE = "POPULATION_NODE"
  VALIDATION_NODE = "VALIDATION_NODE"


  def __init__(self):
    graph_builder = StateGraph(DataPopulationState)


    graph_builder.add_node(self.EXTRACTION_NODE, extract_data)
    graph_builder.add_node(self.POPULATION_NODE, data_model_population)
    graph_builder.add_node(self.VALIDATION_NODE, data_model_validation)

    graph_builder.add_edge(START, self.EXTRACTION_NODE)
    graph_builder.add_edge(self.VALIDATION_NODE, END)


    graph_builder.add_conditional_edges(
        self.EXTRACTION_NODE,
        lambda state: state["route"],
        {
          "answer": END,
          "validation": self.VALIDATION_NODE,
          "next": self.POPULATION_NODE,
        }
    )

    graph_builder.add_conditional_edges(
        self.POPULATION_NODE,
        lambda state: state["route"],
        {
          "answer": END,
          "next": self.VALIDATION_NODE,
        }
    )

    self._graph = graph_builder.compile()

  def run(self, history: list, optimization_data_model, model_validation : ConversationInstructions):
    data_collection_agent : DataPopulationState = {
      "history": history,
      "optimization_data_model": optimization_data_model,
      "model_validation": model_validation,
      "route": None,
    }

    return self._graph.invoke(data_collection_agent)

data_collection_agent = DataCollectionAgent()
