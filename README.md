OPTIMIZATION AGENT

Key decisions:


The agent is built on two graphs:
1.	Main graph handles the full workflow from user-intent resolution to confirmation and final calculation (MCP call).
2.	Data-collection subgraph handles gathering inputs, extracting values, populating structured data, and validating completeness.

Functional scalability
The agent is designed in a way that new optimization tasks can be added without touching the existing graph or writing new prompt templates.
To add a new task, you only need to:
•	Implement and register a new optimization-task class (participates in intent resolution).
•	Define and register its data-model entity (owns the problem-specific data structure, validates completeness, and generates user instructions).

Decoupled architecture
The core components are independent.
Answer generation and data validation communicate through a middleware layer, allowing you to swap or evolve answer-generation logic without manually updating prompts or wiring components tightly.

The agent is also decoupled from the underlying model.
Different tasks can use different models.
Currently available roles: summarizer, general (default), and reasoning.
Model selection is configured through environment variables in the PoC, and can later be made fully dynamic.

Persistence
During the PoC phase, state is stored in memory using LangGraph’s built-in checkpointing.
All entities are Pydantic-serializable and retrieved by session ID (currently hardcoded).

Evaluation
Two critical point of workflow is covered by evaluation tasks:
1.	Intent resolution: checks if the agent correctly identifies the optimization task from user input.
2.	Data extraction: measure the accuracy of extracted values against expected to be extracted from conversation.
Method of evaluation is assertions since LLM as a Judge not needed in PoC phase.
