from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class State(BaseModel):
    report: str = "example"
    diagnosis: dict[str, Any] | None = None
    preprocess_diagnosis: dict[str, Any] | None = None

    embedded_vykony: list[dict[str, Any]] = []
    validity: dict[str, Any] | None = None
    explanation: str | None = None
