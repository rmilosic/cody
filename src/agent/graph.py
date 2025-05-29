# ruff: noqa: D101

"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from __future__ import annotations

import json
import os

import logging
from functools import reduce
from typing import List, Union

from sqlalchemy import JSON

from agent.utils import dedupe_vykony, vector_vykon_filter_funct, vector_material_filter_funct

import numpy as np
import pandas as pd

from langchain.vectorstores import FAISS
from langchain_core.vectorstores import InMemoryVectorStore

from langchain_huggingface import HuggingFaceEmbeddings

from langgraph.graph.message import add_messages

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.documents import Document

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import StateGraph, START, END

from agent import abbrev_node, utils
from agent.state import AgentState


from agent.types import MatchedVykon, MatchedVykony, State, ProcessedData, MatchedMaterial, Material, Vykon

import difflib

logger = logging.getLogger(__name__)

match_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
extract_model = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
# router_model = (model="gpt-4o-mini", temperature=0)

# EMBEDDINGS = "huggingface-retromae-small-cs" # or "openai-embeddings"
EMBEDDINGS = "huggingface"
HUGGINGFACE_MODEL = "sentence-transformers/all-mpnet-base-v2"

if EMBEDDINGS == "huggingface":
    embeddings = HuggingFaceEmbeddings(model_name=HUGGINGFACE_MODEL)
elif EMBEDDINGS == "openai-":
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore_path = os.path.join("data", EMBEDDINGS)
if not os.path.exists(vectorstore_path):
    os.makedirs(vectorstore_path)

# load vector store
try:
    vector_store = InMemoryVectorStore.load(f"data/{EMBEDDINGS}/vectorstore", embedding=embeddings)
except BaseException as e:
    raise ValueError(f"Failed to load vector store: {e}")
    




async def process_text(state: State) -> State:
    """Process text and return structured JSON data."""
    processed_data = await extract_model.with_structured_output(ProcessedData).ainvoke([
        SystemMessage(content="""
                      Jseš personal ve zdravotnim zarizeni. Ze zpravy najdi zdravotnice pomucky nebo zarizeni ktere lze vykazat pojistovne. 
                      Najdi jenom materialy a pomucky ktery byly pouzity/predepsané v ramci teto zpravi. 
                      Ne nachazet leky.
                      Pouzij verbatim text.
                      """),
        HumanMessage(content=state["text"])
    ])
    try:
        processed_data = processed_data.model_dump()
        return {
            "materialy": processed_data.get("materialy", []),
            "odbornost": state.get("odbornost", None),
            "diag_primary": state.get("diag_primary", None),
            "diag_others": state.get("diag_others", None)
        }
    except json.JSONDecodeError:
        return {"processed_data": {}}

async def match_materials(state: State) -> State:
    """Match materials from state against an official list"""
    
    if not state.get("materialy"):
        return state
    
    materialy: List[MatchedMaterial] = state.get("materialy", [])

    # materialy_df = pd.read_json("data/ciselniky/materialy.jsonl", orient="records", lines=True)

    for idx, material in enumerate(materialy):
        # Convert materialy_df to list of dicts for easier matching
        # material_list = materialy_df.to_dict('records')
        
        # Get the best match using difflib
        # best_match = None
        # best_ratio = 0
        
        materials: List[Document] = vector_store.similarity_search(material.get("verbatim_name"), k=10, filter=vector_material_filter_funct)

        # dump Document object to json as a line
        materials_text = "\n".join([json.dumps(material.metadata) for material in materials])
        # Use the chat model to find the best match



        matched_material: MatchedMaterial = await match_model.with_structured_output(MatchedMaterial).ainvoke([
            SystemMessage(content=f"from the provided materials, find the best match for the material."),
            HumanMessage(content=f"""material: \n {material.get("verbatim_name")} \n\n 
                         possible matches: \n {materials_text} """)
        ])

        materialy[idx] = matched_material.model_dump()
    return {
        "materialy": materialy,
        "odbornost": state.get("odbornost", None),
        "diag_primary": state.get("diag_primary", None),
        "diag_others": state.get("diag_others", None)
    }

async def match_vykony(state: State) -> State:
    """Match vykony from state against an official list"""
    
    vykony_df = pd.read_json("data/ciselniky/vykon.jsonl", orient="records", lines=True)


    # get a list of all vykony limited by ODB
    odbornost = state.get("odbornost", None)

    if not len(vykony_df) > 0:
        raise ValueError("No vykony provided in the state.")

    if odbornost:
        print("len vykony_df before filtering:", len(vykony_df))
        print("type odbornost:", type(odbornost))
        print("type odb vykony_df", vykony_df["ODB"].dtype)
        vykony_df = vykony_df[vykony_df['ODB'].astype(str) == odbornost]
        print("len vykony_df after filtering:", len(vykony_df))

    vykony_txt = "\n".join(str(vykon) for vykon in vykony_df.to_dict("records"))

    vykony: MatchedVykony = await match_model.with_structured_output(MatchedVykony).ainvoke([
        SystemMessage(content="""
                      Jseš personal ve zdravotnim zarizeni. Ze zpravy najdi vykony ktere lze vykazat pojistovne. 
                      Najdi jenom vykony ktery byly provedene v ramci teto zpravi.
                      Pokud si nejsi jistý, nech vykon prázdný. 
                      """),
        HumanMessage(content=f"""zprava: \n {state["text"]} \n\n možne vykony: \n {vykony_txt}""")
    ]
    )
        
    
    
    return {
        "vykony": vykony.model_dump()
    }

async def finnish_processing(state: State) -> State:
    """Finish processing and return the final state."""
    # Here we can do any final processing or cleanup if needed
    # For now, we just return the state as is
    # TODO: deduplicate vykony and materialy
    # for duplicates in vykony, join verbatim names into single vykon entry
    original_vykony = state.get("vykony").get("results", [])
    deduped_vykony: dict[str, MatchedVykon] = dedupe_vykony(state.get("vykony", {}))
    
    # if "vykony" in state:
    #     vykony = state["vykony"].get("results", [])
    #     if isinstance(vykony, list):
            
    #         unique_vykony = {v["code"]:  for v in vykony}.values()    
    #         state["vykony"] = list(unique_vykony)
    #     elif isinstance(vykony, dict):
    #         # single vykon, no deduplication needed
    #         pass


    return {
        "vykony": {
            "results": original_vykony,
            "results_deduped": deduped_vykony
        },
        "materialy": state.get("materialy", []),
    }

# Build the graph
workflow = StateGraph(State)

# Add nodes for each step
workflow.add_node("process_text", process_text)
workflow.add_node("match_materials", match_materials)
workflow.add_node("match_vykony", match_vykony)

# Define the flow
workflow.set_entry_point("process_text")

workflow.add_edge("process_text", "match_materials")
workflow.add_edge("process_text", "match_vykony")

workflow.add_node("finish processing", finnish_processing)

workflow.add_edge("match_materials", "finish processing")
workflow.add_edge("match_vykony", "finish processing")

workflow.add_edge("finish processing", END)



# Compile the graph
graph = workflow.compile()

# async def run_pipeline(text: str) -> list:
#     """Run the text processing pipeline."""
#     result = await graph.ainvoke({
#         "text": text
#     })
#     return result["matched_codes"]
