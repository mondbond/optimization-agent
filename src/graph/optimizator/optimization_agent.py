from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from graph.optimizator.nodes.task_intent_node import task_intent_node
from src.graph.optimizator.state.optimization_agent_state import \
  OptimizatorAgentState
from src.graph.optimizator.nodes.answer_node import answer_node
from src.graph.optimizator.nodes.data_collection_node import data_collection_node


class OptimizatorAgent:
  def __init__(self):
    graph_builder = StateGraph(OptimizatorAgentState)

    memory = InMemorySaver()

    graph_builder.add_node("TASK_INTENT_NODE", task_intent_node)
    graph_builder.add_node("DATA_COLLECTION_NODE", data_collection_node)
    graph_builder.add_node("ANSWER_NODE", answer_node)

    graph_builder.add_edge(START, "TASK_INTENT_NODE")
    graph_builder.add_edge("ANSWER_NODE", END)

    graph_builder.add_conditional_edges(
          "TASK_INTENT_NODE",
          lambda state: state["route"],
          {
            "answer": "ANSWER_NODE",
            "next": "DATA_COLLECTION_NODE",
          }
      )

    graph_builder.add_conditional_edges(
        "DATA_COLLECTION_NODE",
        lambda state: state["route"],
        {
          "answer": "ANSWER_NODE",
          "next": "ANSWER_NODE",
        }
    )


    self._graph = graph_builder.compile(checkpointer=memory)

  def run(self, inputs, config={'thread_id': 'default_thread'}):
    return self._graph.invoke({"history": [HumanMessage(inputs)]},
                              {'thread_id': config['thread_id']})

optimization_agent = OptimizatorAgent()
