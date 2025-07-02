import json
from typing import Any, List, TypedDict
import logging

from agent.types import MatchedVykon, MatchedVykony

logger = logging.getLogger(__name__)

from langchain_core.documents import Document

def vector_material_filter_funct(doc: Document) -> bool:
    """Vector filter function"""
    return doc.metadata.get("record") ==  "material"

def vector_vykon_filter_funct(doc: Document) -> bool:
    """Vector filter function"""
    return doc.metadata.get("record") ==  "vykon"


def dedupe_vykony(vykony: MatchedVykony) -> dict[str, MatchedVykon]:
    """Deduplicate vykony by code."""
    seen = set()
    deduped: dict[any] = {}
    orig_vykony: List[MatchedVykon] = vykony.get("results") 

    for vykon in orig_vykony:
        if vykon["code"] not in seen:
            seen.add(vykon["code"])
            deduped[vykon["code"]] = vykon
        else:
            existing_verbatim = deduped[vykon["code"]].get("verbatim_name")
            deduped[vykon["code"]]["verbatim_name"] = ", ".join(
                filter(
                    None,
                    [existing_verbatim, vykon.get("verbatim_name")],
                )
            )
            
    return deduped

# with open("data/stats/diag_code_proportion.") as f:
#     diag_code_proportion: dict[str, list[int]] = json.load(f)


# def find_vykon_by_code(code: int | None):
#     return next((v for v in vykony_cis if v["code"] == code), None)


# def normalize_vykon(vykon: dict[str, Any]) -> dict[str, Any]:
#     return {
#         "code": vykon["code"],
#         "name": vykon.get("name"),
#         "description": vykon.get("description"),
#     }


# def vykon_to_prompt(vykon: dict[str, Any]) -> str:
#     if description := vykon.get("description"):
#         return f"- **{vykon['code']}**: {vykon['name']} - {description}"
#     else:
#         return f"- **{vykon['code']}**: {vykon['name']}"


# class DiagnosisCode(TypedDict):
#     code: str
#     description: str


# def get_vykony_per_diagnosis(item: DiagnosisCode) -> list[dict[str, Any]]:
#     code = str(item["code"])
#     if code not in diag_code_proportion:
#         logger.warning(f"Code {code} not found in diag_code_proportion")
#         return []

#     suggested_vykony = []
#     for code in diag_code_proportion[code]:
#         if found_vykon := find_vykon_by_code(code):
#             suggested_vykony.append(found_vykon)

#     return suggested_vykony
