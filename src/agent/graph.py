# ruff: noqa: D101

"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from __future__ import annotations

import json
import logging
from functools import reduce
from typing import Any, Dict, Literal, Optional, cast

from langchain.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

vector_store = FAISS.load_local(
    "faiss_index",
    OpenAIEmbeddings(model="text-embedding-3-small"),
    allow_dangerous_deserialization=True,
)

with open("data/ciselniky/vykon.jsonl") as f:
    vykony = [json.loads(line) for line in f if line.strip()]

with open("data/ciselniky/mkn.jsonl") as f:
    mkn = [json.loads(line) for line in f if line.strip()]


logger = logging.getLogger(__name__)

with open("data/stats/diag_code_proportion.json") as f:
    diag_code_proportion: dict[str, list[int]] = json.load(f)

DEFAULT_SYSTEM_PROMPT = """
You are an advanced medical AI assistant specialized in suggesting Czech billing codes based on clinical text. You will be given a medical report.

1.  **Analyze the Medical Report:** Carefully read the provided text describing a specific clinical encounter.
2.  **Identify Completed Actions & Materials Used:** Identify procedures **actually performed** and significant billable materials **actually used or administered** *during the clinical encounter documented in this report*.
3.  **Exclude Past Events, Future Plans & Recommendations:**
    *   Explicitly **ignore** any procedures, treatments, or materials mentioned *only* as part of the patient's past medical history or previous consultations occurring *before* this specific encounter.
    *   Explicitly **ignore** any procedures, treatments, or materials described as **recommendations, plans for the future, suggestions, possibilities, or decisions from meetings (like MDT)** that were *not* carried out during this specific documented encounter. Focus strictly on what was **verifiably done** during this visit.
4.  **Grounding:** Base your findings **solely and strictly** on explicit textual evidence describing actions **completed** or materials **used** during this specific encounter. Do not infer unmentioned items or guess codes if evidence is weak, ambiguous, or refers to plans/history.
5.  **You MUST Map the procedures/materials to the enumerated insurance billing codes available in the LLM tool you are operating within :** Map *only* to the completed actions and used materials identified from this encounter.

Do not include **any** introductory text, explanations, summaries, apologies, confidence scores, or concluding remarks in your response.

{corrections}

We know that the patient has the following diagnoses:
{diagnoses}
"""


PREPROCESS_PROMPT = """
You are an advanced medical AI assistant specialized in suggesting Czech billing codes based on clinical text.

There are the following diagnoses. Please pick at least one diagnosis that best describes the patient's condition in MKN-10 classification.
{diagnoses}
"""


VALIDATE_PROMPT = """
You are an advanced medical AI assistant specialized in suggesting Czech billing codes based on clinical text. Check if the provided billing codes are correct. 
Give an explanation for your reasoning for the worker. Return which codes are correct and which are not, those will be removed from the list. Explain why you are keeping or removing the codes. 
The life of humanity depends on it.

User has the following diagnoses:
{diagnoses}

Expected codes based off the diagnoses:
{expected_codes}
"""

VALIDATE_HUMAN_PROMPT = """Report:
{report}

=======

Billing codes provided by the doctor:
{vykony}
"""


class Configuration(BaseModel):
    system_prompt: str = Field(
        default=DEFAULT_SYSTEM_PROMPT,
        json_schema_extra={"langgraph_nodes": ["model"], "langgraph_type": "prompt"},
    )

    preprocess_prompt: str = Field(
        default=PREPROCESS_PROMPT,
        json_schema_extra={
            "langgraph_nodes": ["preprocess"],
            "langgraph_type": "prompt",
        },
    )

    validate_prompt: str = Field(
        default=VALIDATE_PROMPT,
        json_schema_extra={
            "langgraph_nodes": ["validate"],
            "langgraph_type": "prompt",
        },
    )

    validate_human_prompt: str = Field(
        default=VALIDATE_HUMAN_PROMPT,
        json_schema_extra={
            "langgraph_nodes": ["validate"],
            "langgraph_type": "prompt",
        },
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
    preprocess_diagnosis: dict[str, Any] | None = None

    embedded_vykony: list[dict[str, Any]] = []
    validity: dict[str, Any] | None = None
    explanation: str | None = None


async def preprocess(state: State, config: RunnableConfig) -> State:
    configuration = Configuration.from_runnable_config(config)

    diagnoses = "\n".join([f"- {v['DG']}: {v['NAZ']}" for v in mkn])

    class MKN10Code(BaseModel):
        """A diagnosis in MKN-10 classification."""

        code: str
        description: str

    class PreprocessOutput(BaseModel):
        """Please pick at least one diagnosis that best describes the patient's condition in MKN-10 classification."""

        codes: list[MKN10Code]

    result = await (
        ChatOpenAI(model="gpt-4o-mini", temperature=0)
        .with_structured_output(PreprocessOutput)
        .ainvoke(
            [
                SystemMessage(
                    content=configuration.preprocess_prompt.format(diagnoses=diagnoses)
                ),
                HumanMessage(content=state.report),
            ]
        )
    )

    result = cast(PreprocessOutput, result)
    return {"preprocess_diagnosis": result.model_dump()}


async def model(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Each node does work."""
    configuration = Configuration.from_runnable_config(config)

    suggested_vykony = []
    for v in state.preprocess_diagnosis.get("codes", []):
        code = str(v["code"])
        if code not in diag_code_proportion:
            logger.warning(f"Code {code} not found in diag_code_proportion")
            continue

        for code in diag_code_proportion[code]:
            found_vykon = next((v for v in vykony if v["code"] == code), None)
            if found_vykon:
                suggested_vykony.append(found_vykon)

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
            lambda acc, item: {
                **acc,
                **add_code(item["code"], item["description"] or item["name"]),
            },
            suggested_vykony,
            {},
        ),
        "properties": {
            "vykony": {"type": "array", "items": {"anyOf": code_refs}, "minItems": 1}
        },
    }

    diagnoses = "\n".join(
        [
            f"- {v['code']}: {v['description']}"
            for v in state.preprocess_diagnosis.get("codes", [])
        ]
    )

    diagnosis = (
        await ChatAnthropic(model="claude-3-7-sonnet-latest", temperature=0)
        .with_structured_output(schema)
        .ainvoke(
            [
                SystemMessage(
                    content=configuration.system_prompt.format(
                        diagnoses=diagnoses,
                        corrections=f"A more senior medical assistant has reviewed the report and provided the following corrections: {state.explanation}\n"
                        if state.explanation
                        else None,
                    )
                ),
                HumanMessage(content=state.report),
            ]
        )
    )

    return {"diagnosis": diagnosis}


EMBEDDED_VYKONY_PROMPT = """
You are an advanced medical AI assistant specialized in suggesting Czech billing codes based on clinical text.

You are given a list of expected vykony that are based off the frequency of the codes in the database. Please pick the most relevant vykony and return them in a list to be added to the medical report. 
The explanation should be based on the provided doctor's report.

Suggested vykony:
{suggested_vykony}
"""


async def add_embedded_vykony(state: State, config: RunnableConfig) -> State:
    configuration = Configuration.from_runnable_config(config)

    from collections import defaultdict

    top_10 = defaultdict(int)
    for items in diag_code_proportion.values():
        for item in items:
            top_10[item] += 1

    top_10 = sorted(top_10.items(), key=lambda x: x[1], reverse=True)[:10]

    suggested_vykony = []
    for code, _ in top_10:
        found_vykon = next((v for v in vykony if v["code"] == code), None)
        if found_vykon:
            suggested_vykony.append(found_vykon)

    suggested_vykony = "\n".join(
        [f"- {v['code']}: {v['description'] or v['name']}" for v in suggested_vykony]
    )

    class VykonAction(BaseModel):
        """Action to take on the vykon."""

        code: int = Field(description="Code of the 'vykon'")
        description: str = Field(description="Description of the 'vykon'")
        explanation: str = Field(description="Explanation for the action")

    class AddEmbeddedVykonyOutput(BaseModel):
        vykony: list[VykonAction]

    actions = await (
        ChatAnthropic(model="claude-3-7-sonnet-latest", temperature=0)
        .with_structured_output(AddEmbeddedVykonyOutput)
        .ainvoke(
            [
                SystemMessage(
                    content=EMBEDDED_VYKONY_PROMPT.format(
                        suggested_vykony=suggested_vykony
                    )
                ),
                HumanMessage(content=state.report),
            ]
        )
    )

    actions = cast(AddEmbeddedVykonyOutput, actions)
    new_vykony = state.diagnosis.get("vykony", [])

    # TODO: find the description of the vykon
    new_vykony.extend(
        [{"code": x.code, "description": x.description} for x in actions.vykony]
    )

    return {"diagnosis": {"vykony": new_vykony}}


async def validate(state: State, config: RunnableConfig) -> State:
    configuration = Configuration.from_runnable_config(config)

    vykony = state.diagnosis.get("vykony", [])
    vykony_str = "\n".join([f"- {v['code']}: {v['description']}" for v in vykony])

    class VykonAction(BaseModel):
        """Action to take on the vykon."""

        code: int
        explanation: str
        action: Literal["keep", "remove"]

    class ValidateOutput(BaseModel):
        vykony: list[VykonAction] = Field(
            description="List of vykony to keep or remove. Must include all of "
        )

    suggested_vykony = []
    for v in state.preprocess_diagnosis.get("codes", []):
        code = str(v["code"])
        if code not in diag_code_proportion:
            logger.warning(f"Code {code} not found in diag_code_proportion")
            continue

        for code in diag_code_proportion[code]:
            found_vykon = next((v for v in vykony if v["code"] == code), None)
            if found_vykon:
                suggested_vykony.append(found_vykon)

    validation = (
        await ChatAnthropic(model="claude-3-7-sonnet-latest", temperature=0)
        .with_structured_output(ValidateOutput)
        .ainvoke(
            [
                SystemMessage(
                    configuration.validate_prompt.format(
                        diagnoses="\n".join(
                            [
                                f"- {v['code']}: {v['description']}"
                                for v in state.preprocess_diagnosis.get("codes", [])
                            ]
                        ),
                        expected_codes="\n".join(
                            f"- {v['code']}: {v['description']}"
                            for v in suggested_vykony
                        ),
                    )
                ),
                HumanMessage(
                    content=configuration.validate_human_prompt.format(
                        report=state.report, vykony=vykony_str
                    )
                ),
            ]
        )
    )

    validation = cast(ValidateOutput, validation)

    def is_valid_code(code: int) -> bool:
        validity = next((v for v in validation.vykony if v.code == code), None)
        return not validity or validity.action != "remove"

    valid_codes = {
        "vykony": [
            vykon
            for vykon in state.diagnosis.get("vykony", [])
            if is_valid_code(vykon["code"])
        ],
    }

    return {"diagnosis": valid_codes, "validity": validation.model_dump()}


workflow = StateGraph(State, config_schema=Configuration)
workflow.add_node("preprocess", preprocess)
workflow.add_node("model", model)
workflow.add_node("add_embedded_vykony", add_embedded_vykony)
workflow.add_node("validate", validate)
workflow.add_edge("__start__", "preprocess")
workflow.add_edge("preprocess", "model")
workflow.add_edge("model", "add_embedded_vykony")
workflow.add_edge("add_embedded_vykony", "validate")

graph = workflow.compile()
graph.name = "New Graph"  # This defines the custom name in LangSmith
