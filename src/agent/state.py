from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class AgentState(BaseModel):
    report: str = "example"
    diagnosis: dict[str, Any] | None = None
    preprocess_diagnosis: dict[str, Any] | None = None

    validity: dict[str, Any] | None = None
    explanation: str | None = None
