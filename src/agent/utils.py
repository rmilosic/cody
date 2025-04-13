import json
from typing import Any

with open("data/ciselniky/vykon.jsonl") as f:
    vykony_cis = [json.loads(line) for line in f if line.strip()]


def find_vykon_by_code(code: int | None):
    return next((v for v in vykony_cis if v["code"] == code), None)


def normalize_vykon(vykon: dict[str, Any]) -> dict[str, Any]:
    return {
        "code": vykon["code"],
        "name": vykon.get("name"),
        "description": vykon.get("description"),
    }


def vykon_to_prompt(vykon: dict[str, Any]) -> str:
    return f"- <code>{vykon['code']}</code>: {vykon['description'] or vykon['name']}"
