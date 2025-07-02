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


from agent.types import MatchedMaterials, MatchedVykon, MatchedVykony, DataGeneratorState, ProcessedData, MatchedMaterial, Material, Vykon

import difflib

logger = logging.getLogger(__name__)

chat_model = ChatOpenAI(model="gpt-4.1", temperature=0)
# router_model = (model="gpt-4o-mini", temperature=0)

# # EMBEDDINGS = "huggingface-retromae-small-cs" # or "openai-embeddings"
# EMBEDDINGS = "huggingface"
# HUGGINGFACE_MODEL = "sentence-transformers/all-mpnet-base-v2"

# if EMBEDDINGS == "huggingface":
#     embeddings = HuggingFaceEmbeddings(model_name=HUGGINGFACE_MODEL)
# elif EMBEDDINGS == "openai-":
#     embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# vectorstore_path = os.path.join("data", EMBEDDINGS)
# if not os.path.exists(vectorstore_path):
    # os.makedirs(vectorstore_path)

# # load vector store
# try:
#     vector_store = InMemoryVectorStore.load(f"data/{EMBEDDINGS}/vectorstore", embedding=embeddings)
# except BaseException as e:
#     raise ValueError(f"Failed to load vector store: {e}")
    
odbornost_df = pd.read_csv("data/ciselniky/odbornosti_filter.csv", dtype={"KOD": str, "NAZ": str})

async def write_medical_text(state: DataGeneratorState) -> DataGeneratorState:
    """Write medical text to the state."""
    # Here we can write the medical text to the state
    # For now, we just return the state as is
    # if "text" not in state:
    #     raise ValueError("State must contain 'text' key with medical text.")
    
    # get odbornost and vykony from state
    
    odbornost = state.get("odbornost", None)
    vykony: List[MatchedVykon] = state.get("vykony", None)

    if not odbornost or not vykony:
        raise ValueError("State must contain 'odbornost' and 'vykony' keys.")
    
    # load odbornost name

    first_vykon: MatchedVykon = vykony[0] if isinstance(vykony, list) and len(vykony) > 0 else None
    
    if first_vykon is None:
        raise ValueError("State must contain at least one 'vykon'.")


    odbornost_name = odbornost_df[odbornost_df["KOD"] == odbornost].iloc[0]["NAZ"]
    
    # roll the dice to decide if materials should be included in the text
    include_materials = np.random.rand() < 0.7  # 70% chance to include materials

    result = await chat_model.ainvoke(
        [
            HumanMessage(
                content=f"""Jste zdravotním personalem z odborností {odbornost_name}. Potrebujete napsat zpravu na zaklade vaše odbornosti
                -----
                Provedli jste vykon '{first_vykon.get("name", None)}' s kódem '{first_vykon.get("code", None)}'.
                Popis: '{first_vykon.get("description", None)}'.
                -----
                { "ne" if not include_materials else None }zahrňte materiály, které by mohly být použity při tomto výkonu.
                
                Vymislite primarni diagnozu, ktera by mohla byt stanovena pacientovi pred navstevou u vas.

                Napište lékařský text, který by mohl být použit jako součást lékařské zprávy.
                Text by měl být v češtině a měl by být napsan v profesionálním lékařském stylu.
                Nezařazujte žádné osobní údaje pacienta, jako je jméno, adresa nebo rodné číslo
                Nezařazujte vykon nebo material doslova, použijte je pouze jako inspiraci pro text. 
                Nestruktujte text, aby obsahoval konkrétní vykon nebo material, ale spíše použijte jejich význam a kontext.
                Nezařazujte žádné další informace, které nejsou relevantní pro lékařský text.

                Delate zapis pro konkretni udalost v jeden den, ne pro delsi dobu. 
                Nepište diagnozy do zpravy.
                """
            )
        ]
    )
    # use vykon and odbornost (name + code) to generate a medical text
    # decide for a primary diagnosis before the patient visited based on the odbornost and vykony
    # decide if materials should be included in the text 0.7 chance
    # if yes, use materials that make sense for the procedure
    # generat text 

    return {
        "text": result.content,
    }



# Build the graph
workflow = StateGraph(DataGeneratorState)

# Add nodes for each step
workflow.set_entry_point("write_medical_text")

workflow.add_node("write_medical_text", write_medical_text)

workflow.add_edge("write_medical_text", END)



# Compile the graph
graph = workflow.compile()

# async def run_pipeline(text: str) -> list:
#     """Run the text processing pipeline."""
#     result = await graph.ainvoke({
#         "text": text
#     })
#     return result["matched_codes"]
