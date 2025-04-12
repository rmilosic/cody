# ruff: noqa: D101

"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from __future__ import annotations

import json
from functools import reduce
from typing import Any, Dict, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

with open("data/ciselniky/vykon.jsonl") as f:
    vykony = [json.loads(line) for line in f if line.strip()]


class Configuration(BaseModel):
    system_prompt: str = Field(
        default="Extract the diagnosis from the text. Try to match as many codes as possible.",
        json_schema_extra={"langgraph_nodes": ["model"], "langgraph_type": "prompt"},
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""
        configurable = (config.get("configurable") or {}) if config else {}
        return cls.model_validate(configurable)


class State(BaseModel):
    report: str = "example"
    diagnosis: dict[str, Any] | None = None


code_refs = []


def add_code(code: int, description: str) -> dict[str, Any]:
    code_refs.append({"$ref": f"#/definitions/{str(code)}"})
    return {
        str(code): {
            "properties": {
                "code": {"const": code, "title": "Code", "type": "integer"},
                "description": {
                    "const": description,
                    "title": "Description",
                    "type": "string",
                },
            },
            "required": ["code", "description"],
            "title": str(code),
            "type": "object",
        },
    }


schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "MedicalReport",
    "description": "Medical report of the patient",
    "type": "object",
    "definitions": reduce(
        lambda acc, item: {**acc, **add_code(item["code"], item["description"])},
        vykony,
        {},
    ),
    "properties": {
        "vykony": {"type": "array", "items": {"anyOf": code_refs}, "minItems": 1}
    },
}


async def model(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Each node does work."""
    configuration = Configuration.from_runnable_config(config)

    diagnosis = (
        await ChatOpenAI(model="gpt-4o-mini", temperature=1)
        .with_structured_output(schema)
        .ainvoke(
            [
                SystemMessage(content=configuration.system_prompt),
                HumanMessage(content=state.report),
            ]
        )
    )

    return {"diagnosis": diagnosis}


workflow = StateGraph(State, config_schema=Configuration)
workflow.add_node("model", model)
workflow.add_edge("__start__", "model")

graph = workflow.compile()
graph.name = "New Graph"  # This defines the custom name in LangSmith
