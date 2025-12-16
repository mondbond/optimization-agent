# Optimization Agent

## Overview

The Optimization Agent is designed to handle complex workflows for user-intent resolution, data collection, and final calculations. It is built with scalability, modularity, and flexibility in mind.

---

## Architecture

### Graph-Based Design

The agent leverages two primary graphs:

1. **Main Graph**  
   Handles the full workflow from user-intent resolution to confirmation and final calculation (MCP call).

2. **Data-Collection Subgraph**  
   Manages input gathering, value extraction, structured data population, and completeness validation.

### Decoupled Architecture

- Core components are independent.
- Answer generation and data validation communicate through a middleware layer.
- Allows swapping or evolving the answer-generation logic without manual prompt updates.
- Agent is decoupled from the underlying model.
    - Different tasks can use different models.
    - Available roles: `summarizer`, `general` (default), `reasoning`.
    - Model selection is configured through environment variables and can be made dynamic later.

---

## Functional Scalability

Adding new optimization tasks requires minimal effort:

1. Implement and register a new **optimization-task class** (participates in intent resolution).
2. Define and register its **data-model entity**:
    - Owns the task-specific data structure.
    - Validates completeness.
    - Generates user instructions.

No changes to the existing graph or prompt templates are needed.

---

## Persistence

- During the PoC phase, state is stored in memory using **LangGraph’s built-in checkpointing**.
- All entities are **Pydantic-serializable** and retrieved by session ID (currently hardcoded).

---

## Evaluation

Two critical workflow points are evaluated:

1. **Intent Resolution**  
   Ensures the agent correctly identifies the optimization task from user input.

2. **Data Extraction**  
   Measures the accuracy of extracted values against expected outputs from conversations.

> Evaluation is done via assertions; an LLM as a judge is not required during the PoC phase.
