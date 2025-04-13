import json
from typing import Any, TypedDict
import logging

logger = logging.getLogger(__name__)

with open("data/ciselniky/vykon.jsonl") as f:
    vykony_cis = [json.loads(line) for line in f if line.strip()]


with open("data/stats/diag_code_proportion.json") as f:
    diag_code_proportion: dict[str, list[int]] = json.load(f)


def find_vykon_by_code(code: int | None):
    return next((v for v in vykony_cis if v["code"] == code), None)


def normalize_vykon(vykon: dict[str, Any]) -> dict[str, Any]:
    return {
        "code": vykon["code"],
        "name": vykon.get("name"),
        "description": vykon.get("description"),
    }


def vykon_to_prompt(vykon: dict[str, Any]) -> str:
    if description := vykon.get("description"):
        return f"- **{vykon['code']}**: {vykon['name']} - {description}"
    else:
        return f"- **{vykon['code']}**: {vykon['name']}"


class DiagnosisCode(TypedDict):
    code: str
    description: str


def get_vykony_per_diagnosis(item: DiagnosisCode) -> list[dict[str, Any]]:
    code = str(item["code"])
    if code not in diag_code_proportion:
        logger.warning(f"Code {code} not found in diag_code_proportion")
        return []

    suggested_vykony = []
    for code in diag_code_proportion[code]:
        if found_vykon := find_vykon_by_code(code):
            suggested_vykony.append(found_vykon)

    return suggested_vykony
