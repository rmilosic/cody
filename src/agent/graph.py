# ruff: noqa: D101

"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from __future__ import annotations

import json
import logging
from functools import reduce
from typing import List, Union

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

from agent import abbrev_node, utils
from agent.state import AgentState


from agent.types import State, ProcessedData, MatchedMaterial

logger = logging.getLogger(__name__)


chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# router_model = (model="gpt-4o-mini", temperature=0)

# load vector store
try:
    vector_store = InMemoryVectorStore.load("data/vectorstore", embedding=OpenAIEmbeddings())
except BaseException as e:
    raise e

async def process_text(state: State) -> State:
    """Process text and return structured JSON data."""
    processed_data = await chat_model.with_structured_output(ProcessedData).ainvoke([
        SystemMessage(content="ve ambulantni zpravy najdi materialy, leky, vykony a zdravodnicky pomucky. use explicit text"),
        HumanMessage(content=state["text"])
    ])
    try:
        processed_data = processed_data.model_dump()
        return {
            "vykony": processed_data.get("vykony", []),
            "materialy": processed_data.get("materialy", [])
        }
    except json.JSONDecodeError:
        return {"processed_data": {}}

async def match_materials(state: State) -> State:
    """Match materials from state against an official list"""
   
    materialy: List[str] = state["processed_data"].get("materialy", [])
    for _, material in enumerate(materialy):
        if not isinstance(material, str):
            continue
        
        # zp = vector_store.similarity_search(material, k=10, filter=utils.vector_material_filter_funct)
        # 1. faza  - rozkoskovat material
        extracted_material: Union[MatchedMaterial, None] = await chat_model.with_structured_output(MatchedMaterial).ainvoke([
            SystemMessage(content="Vyextrahuj verbatim strukturu materiala (brand, velikost baleni, velikost produktu. Pokud si nejseš jisti, vynech pole prazdne"),
            HumanMessage(content=material)
        ])
        
        materialy[_] = extracted_material.model_dump()
    
    return {
        "processed_data": {
            "vykony": state["processed_data"].get("vykony"), 
            "materialy": materialy
        }
    }


# Build the graph
workflow = StateGraph(State)

# Add nodes for each step
workflow.add_node("process_text", process_text)
# workflow.add_node("match_materials", match_materials)

# Define the flow
workflow.set_entry_point("process_text")
# workflow.add_edge("process_text", "match_materials")

# Compile the graph
graph = workflow.compile()

# async def run_pipeline(text: str) -> list:
#     """Run the text processing pipeline."""
#     result = await graph.ainvoke({
#         "text": text
#     })
#     return result["matched_codes"]
