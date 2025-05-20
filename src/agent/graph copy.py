# ruff: noqa: D101

"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from __future__ import annotations

import json
import logging
from functools import reduce
from typing import Any, Dict, List, Literal, Optional, Union

import numpy as np
import pandas as pd
from langchain.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import StateGraph, START
from pydantic import BaseModel, Field

from typing import Annotated

from typing_extensions import TypedDict


from agent import abbrev_node, utils
from agent.state import AgentState

logger = logging.getLogger(__name__)


chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# router_model = (model="gpt-4o-mini", temperature=0)

# Pydantic
class ProcessedData(BaseModel):
    """Processed Data."""

    vykony: Union[List[str], None] = Field(description="provedeni vykony")
    materialy: Union[List[str], None] = Field(description="pouzite materialy a zdravotnicke pomucky") 


class ProcessOutput(BaseModel):
    """Output from text processing."""
    data: dict

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    # messages: Annotated[list, add_messages]
    text: str
    processed_data: Optional[ProcessedData] = None
    matched_codes: Optional[list] = None



# build a langgraph graph that intakes a text and 
# 1. runs a prompt to process the text and return structured data in JSON format
# 2. take JSON data and match each property (list) against a list of codes
# 3. return the list of codes






# def chatbot(state: State):
#     return {"messages": [chat_model.invoke(state["messages"])]}


# # The first argument is the unique node name
# # The second argument is the function or object that will be called whenever
# # the node is used.
# graph_builder.add_node("chatbot", chatbot)

# graph_builder.add_edge(START, "chatbot")

# graph = graph_builder.compile()

# vector_store = FAISS.load_local(
#     "faiss_index",
#     OpenAIEmbeddings(model="text-embedding-3-small"),
#     allow_dangerous_deserialization=True,
# )

# with open("data/ciselniky/vykon.jsonl") as f:
#     vykony_cis = [json.loads(line) for line in f if line.strip()]

# with open("data/ciselniky/mkn.jsonl") as f:
#     mkn_cis = [json.loads(line) for line in f if line.strip()]


# vykony = pd.read_csv(
#     "data/vykazy/vyk_23_vykony_new.csv", encoding="windows-1252", sep=";"
# )
# vykony_pivot = pd.get_dummies(vykony.set_index("CDOKL")["KOD"]).groupby("CDOKL").sum()
# co_occurrence_matrix = np.dot(vykony_pivot.T, vykony_pivot)
# np.fill_diagonal(co_occurrence_matrix, 0)
# co_occurrence_df = pd.DataFrame(
#     co_occurrence_matrix, index=vykony_pivot.columns, columns=vykony_pivot.columns
# )

# co_occurrence_df_normalized = (co_occurrence_df - co_occurrence_df.min()) / (
#     co_occurrence_df.max() - co_occurrence_df.min()
# )
# co_occurrence_df_normalized.fillna(0, inplace=True)
# co_occurrence_df_normalized.reset_index(inplace=True)
# co_occurrence_df_normalized.rename(columns={"index": "kod"}, inplace=True)


# PREPROCESS_PROMPT = """
# You are an advanced medical AI assistant specialized in suggesting Czech billing codes based on clinical text.

# There are the following diagnoses. Please pick at least one diagnosis that best describes the patient's condition in MKN-10 classification.
# {diagnoses}
# """


# DEFAULT_SYSTEM_PROMPT = """
# You are an advanced medical AI assistant specialized in suggesting Czech billing codes based on clinical text. You will be given a medical report.

# 1.  **Analyze the Medical Report:** Carefully read the provided text describing a specific clinical encounter.
# 2.  **Identify Completed Actions & Materials Used:** Identify procedures **actually performed** and significant billable materials **actually used or administered** *during the clinical encounter documented in this report*.
# 3.  **Exclude Past Events, Future Plans & Recommendations:**
#     *   Explicitly **ignore** any procedures, treatments, or materials mentioned *only* as part of the patient's past medical history or previous consultations occurring *before* this specific encounter.
#     *   Explicitly **ignore** any procedures, treatments, or materials described as **recommendations, plans for the future, suggestions, possibilities, or decisions from meetings (like MDT)** that were *not* carried out during this specific documented encounter. Focus strictly on what was **verifiably done** during this visit.
# 4.  **Grounding:** Base your findings **solely and strictly** on explicit textual evidence describing actions **completed** or materials **used** during this specific encounter. Do not infer unmentioned items or guess codes if evidence is weak, ambiguous, or refers to plans/history.
# 5.  **You MUST Map the procedures/materials to the enumerated insurance billing codes available in the LLM tool you are operating within :** Map *only* to the completed actions and used materials identified from this encounter.

# Do not include **any** introductory text, explanations, summaries, apologies, confidence scores, or concluding remarks in your response. 

# We know that the patient has the following diagnoses:
# {diagnoses}
# """


# VALIDATE_PROMPT = """
# You are an advanced medical AI assistant specialized in suggesting Czech billing codes based on clinical text. Check if the provided billing codes are correct. 
# Give an explanation for your reasoning for the worker. Return which codes are correct and which are not, those will be removed from the list. Explain why you are keeping or removing the codes. 
# Quote the parts of the report that support your reasoning. 

# Do not throw out generic codes that may apply for the initial appointment. Do not throw out codes that may be duplicated as multiple codes may apply for a single visit. The life of humanity depends on it.

# User has the following diagnoses:
# {diagnoses}

# Expected codes based off the diagnoses:
# {expected_codes}
# """

# VALIDATE_HUMAN_PROMPT = """Report:
# {report}

# =======

# Billing codes provided by the doctor:
# {vykony}
# """


# class Configuration(BaseModel):
#     system_prompt: str = Field(
#         default=DEFAULT_SYSTEM_PROMPT,
#         json_schema_extra={"langgraph_nodes": ["model"], "langgraph_type": "prompt"},
#     )

#     preprocess_prompt: str = Field(
#         default=PREPROCESS_PROMPT,
#         json_schema_extra={
#             "langgraph_nodes": ["preprocess"],
#             "langgraph_type": "prompt",
#         },
#     )

#     validate_prompt: str = Field(
#         default=VALIDATE_PROMPT,
#         json_schema_extra={
#             "langgraph_nodes": ["validate"],
#             "langgraph_type": "prompt",
#         },
#     )

#     validate_human_prompt: str = Field(
#         default=VALIDATE_HUMAN_PROMPT,
#         json_schema_extra={
#             "langgraph_nodes": ["validate"],
#             "langgraph_type": "prompt",
#         },
#     )

#     @classmethod
#     def from_runnable_config(
#         cls, config: Optional[RunnableConfig] = None
#     ) -> Configuration:
#         """Create a Configuration instance from a RunnableConfig object."""
#         configurable = (config.get("configurable") or {}) if config else {}
#         return cls.model_validate(configurable)


# async def preprocess(state: AgentState, config: RunnableConfig) -> AgentState:
#     configuration = Configuration.from_runnable_config(config)

#     diagnoses = "\n".join([f"- {v['DG']}: {v['NAZ']}" for v in mkn_cis])

#     class MKN10Code(BaseModel):
#         """A diagnosis in MKN-10 classification."""

#         code: str
#         description: str

#     class PreprocessOutput(BaseModel):
#         """Please pick at least one diagnosis that best describes the patient's condition in MKN-10 classification."""

#         codes: list[MKN10Code]

#     result: PreprocessOutput = await router_model.with_structured_output(
#         PreprocessOutput
#     ).ainvoke(
#         [
#             SystemMessage(
#                 content=configuration.preprocess_prompt.format(diagnoses=diagnoses)
#             ),
#             HumanMessage(content=state.report),
#         ]
#     )

#     return {"preprocess_diagnosis": result.model_dump()}


# async def abbrev(state: AgentState, config: RunnableConfig) -> AgentState:
#     result = await chat_model.ainvoke(
#         [
#             SystemMessage(content=abbrev_node.DE_ABBREV_SYSTEM_PROMPT),
#             HumanMessage(content=state.report),
#         ]
#     )

#     return {"report": result.text()}


# async def main_model(state: AgentState, config: RunnableConfig) -> Dict[str, Any]:
#     """Each node does work."""
#     configuration = Configuration.from_runnable_config(config)

#     suggested_vykony = []
#     for item in state.preprocess_diagnosis.get("codes", []):
#         suggested_vykony.extend(utils.get_vykony_per_diagnosis(item))

#     code_refs = []

#     def add_code(code: int, name: str, description: str | None) -> dict[str, Any]:
#         code_refs.append({"$ref": f"#/definitions/{str(code)}"})
#         return {
#             str(code): {
#                 "properties": {
#                     "code": {"const": code, "title": "Code", "type": "integer"},
#                     "name": {"const": name, "title": "Name", "type": "string"},
#                     **(
#                         {
#                             "description": {
#                                 "const": description,
#                                 "title": "Description",
#                                 "type": "string",
#                             }
#                         }
#                         if description
#                         else {}
#                     ),
#                 },
#                 "required": ["code", "name", "description"]
#                 if description
#                 else ["code", "name"],
#                 "title": str(code),
#                 "type": "object",
#             },
#         }

#     schema = {
#         "$schema": "http://json-schema.org/draft-07/schema#",
#         "title": "MedicalReport",
#         "description": "Medical report of the patient",
#         "type": "object",
#         "definitions": reduce(
#             lambda acc, item: {
#                 **acc,
#                 **add_code(item["code"], item["name"], item["description"]),
#             },
#             suggested_vykony,
#             {},
#         ),
#         "properties": {
#             "vykony": {"type": "array", "items": {"anyOf": code_refs}, "minItems": 1}
#         },
#     }

#     diagnoses = "\n".join(
#         [
#             f"- {v['code']}: {v['description']}"
#             for v in state.preprocess_diagnosis.get("codes", [])
#         ]
#     )

#     diagnosis = await chat_model.with_structured_output(schema).ainvoke(
#         [
#             SystemMessage(
#                 content=configuration.system_prompt.format(diagnoses=diagnoses)
#             ),
#             HumanMessage(content=state.report),
#         ]
#     )

#     return {"diagnosis": diagnosis}


# async def validate(state: AgentState, config: RunnableConfig) -> AgentState:
#     configuration = Configuration.from_runnable_config(config)

#     suggested_vykony = []
#     for item in state.preprocess_diagnosis.get("codes", []):
#         suggested_vykony.extend(utils.get_vykony_per_diagnosis(item))

#     class VykonAction(BaseModel):
#         """Action to take on the vykon."""

#         code: int
#         explanation: str
#         action: Literal["keep", "remove"]

#     class ValidateOutput(BaseModel):
#         vykony: list[VykonAction] = Field(
#             description="List of vykony to keep or remove. Must include all of user provided codes."
#         )

#     validation: ValidateOutput = await chat_model.with_structured_output(
#         ValidateOutput
#     ).ainvoke(
#         [
#             SystemMessage(
#                 configuration.validate_prompt.format(
#                     diagnoses="\n".join(
#                         [
#                             f"- {v['code']}: {v['description']}"
#                             for v in state.preprocess_diagnosis.get("codes", [])
#                         ]
#                     ),
#                     expected_codes="\n".join(
#                         utils.vykon_to_prompt(v) for v in suggested_vykony
#                     ),
#                 )
#             ),
#             HumanMessage(
#                 content=configuration.validate_human_prompt.format(
#                     report=state.report,
#                     vykony="\n".join(
#                         [
#                             utils.vykon_to_prompt(v)
#                             for v in state.diagnosis.get("vykony", [])
#                         ]
#                     ),
#                 )
#             ),
#         ]
#     )

#     new_vykony = []
#     for vykon in state.diagnosis.get("vykony", []):
#         validity = next((v for v in validation.vykony if v.code == vykon["code"]), None)
#         if not validity or validity.action != "remove":
#             new_vykony.append(
#                 {**vykon, "explanation": validity.explanation if validity else None}
#             )

#     return {"diagnosis": {"vykony": new_vykony}, "validity": validation.model_dump()}


# async def add_co_occurrence(state: AgentState, config: RunnableConfig) -> AgentState:
#     relevant_docs = await vector_store.asimilarity_search(state.report, k=10)
#     docs = []
#     for doc in relevant_docs:
#         docs.append(json.loads(doc.page_content))

#     docs = pd.DataFrame(docs)

#     to_add_codes = []
#     to_remove_codes = []

#     for code in docs["code"].tolist():
#         df = co_occurrence_df_normalized[["kod", code]]
#         df = df[df["kod"].isin([42022, 42023, 9543])]
#         threshold = 0.6

#         to_add = list(
#             int(x)
#             for x in df.where(df[code] >= threshold)["kod"].replace(np.nan, None)
#             if x is not None
#         )
#         to_remove = list(
#             int(x)
#             for x in df.where(df[code] < threshold)["kod"].replace(np.nan, None)
#             if x is not None
#         )

#         to_add_codes.extend(to_add)
#         to_remove_codes.extend(to_remove)

#     new_vykony = [
#         v for v in state.diagnosis.get("vykony", []) if v["code"] not in to_remove_codes
#     ]
#     for code in set(to_add_codes):
#         if found_vykon := utils.find_vykon_by_code(code):
#             new_vykony.append(found_vykon)

#     return {"diagnosis": {"vykony": new_vykony}}


# async def clear(state: AgentState, config: RunnableConfig) -> AgentState:
#     vykony = state.diagnosis.get("vykony", [])
#     vykony = [(v, utils.find_vykon_by_code(v["code"])) for v in vykony]
#     vykony = [
#         {**valid, "explanation": v.get("explanation")} for v, valid in vykony if valid
#     ]
#     vykony = list({int(v["code"]): v for v in vykony}.values())

#     return {"diagnosis": {"vykony": vykony}}


# workflow = StateGraph(AgentState, config_schema=Configuration)
# workflow.add_node("preprocess", preprocess)
# workflow.add_node("abbrev", abbrev)
# workflow.add_node("model", main_model)
# workflow.add_node("add_co_occurrence", add_co_occurrence)
# workflow.add_node("validate", validate)
# workflow.add_node("clear", clear)


# edge_chain = [
#     "__start__",
#     "preprocess",
#     # "abbrev",
#     "model",
#     "validate",
#     "add_co_occurrence",
#     "clear",
# ]
# for i in range(len(edge_chain) - 1):
#     workflow.add_edge(edge_chain[i], edge_chain[i + 1])

# graph = workflow.compile()






  

class MatchedMaterial(BaseModel):
    """Match material from text against official list"""
    name: str = Field(description="name of the material")
    code: str = Field(description="code of the material")

async def process_text(state: State) -> State:
    """Process text and return structured JSON data."""
    processed_data = await chat_model.with_structured_output(ProcessedData).ainvoke([
        SystemMessage(content="ve ambulantni zpravy najdi materialy, leky, vykony a zdravodnicky pomucky. use explicit text"),
        HumanMessage(content=state["text"])
    ])
    
    try:
        processed_data = processed_data.model_dump()
        
        return {"processed_data": processed_data}
    except json.JSONDecodeError:
        return {"processed_data": {}}

async def match_materials(state: State) -> State:
    """Match materials from state against an official list"""
    if not state.get("processed_data"):
        return {"matched_codes": []}
    
    matched_codes = []

    with open("data/ciselniky/zp_sample.txt") as f:
        zp = [line for line in f if line.strip()]


    print("state", state)
    for material in state.processed_data.materialy:
        if not isinstance(material, str):
            continue
        processed_data = await chat_model.with_structured_output(ProcessedData).ainvoke([
            SystemMessage(content=f"najdi jestli je pouzity nejaky material ze seznamu\n {zp}"),
            HumanMessage(content=material)
        ])
        
    return {"matched_codes": processed_data.model_dump_json()}





# Build the graph
workflow = StateGraph(State)

# Add nodes for each step
workflow.add_node("process_text", process_text)
workflow.add_node("match_materials", match_materials)

# Define the flow
workflow.set_entry_point("process_text")
workflow.add_edge("process_text", "match_materials")

# Compile the graph
graph = workflow.compile()

# async def run_pipeline(text: str) -> list:
#     """Run the text processing pipeline."""
#     result = await graph.ainvoke({
#         "text": text
#     })
#     return result["matched_codes"]
