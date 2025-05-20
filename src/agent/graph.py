# ruff: noqa: D101

"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from __future__ import annotations

import json
import logging
from functools import reduce
from typing import Any, Dict, List, Literal, Optional, Union
from typing import Annotated

import numpy as np
import pandas as pd

from langchain.vectorstores import FAISS
from langchain_core.vectorstores import InMemoryVectorStore

from langchain_anthropic import ChatAnthropic
from langgraph.graph.message import add_messages

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.documents import Document

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import StateGraph, START
from pydantic import BaseModel, Field


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
    text: str
    processed_data: Optional[ProcessedData] = None
    matched_materials: Optional[list] = None


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
    
    matched_materials: List[MatchedMaterial] = []

    with open("data/ciselniky/zp_sample.txt") as f:
        zp = [line for line in f if line.strip()]

    print("state", state)
    
    for material in state["processed_data"].get("materialy", []):
        if not isinstance(material, str):
            continue
        
        
        matched_material: Union[MatchedMaterial, None] = await chat_model.with_structured_output(MatchedMaterial).ainvoke([
            SystemMessage(content=f"najdi jestli je pouzity nejaky material ze seznamu\n {zp}"),
            HumanMessage(content=material)
        ])

        matched_materials.extend([matched_material.model_dump()])

        
        
    return {"matched_materials": matched_materials}


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
