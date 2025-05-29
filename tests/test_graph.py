# ruff: noqa: D101

import pytest
from dotenv import load_dotenv
from langsmith import testing as t

from agent.graph import graph
from agent.utils import dedupe_vykony

load_dotenv()


# @pytest.mark.langsmith
# async def test_sql_generation_select_all() -> None:
#     result = await graph.ainvoke({"report": "1234"})
#     assert result is None

def test_dedupe_vykony():
    """Deduplicate vykony by code."""
    matched_vykony = {
        "results": [
            {"code": "001", "name": "Vykon A", "verbatim_name": "verbatim 1"},
            {"code": "002", "name": "Vykon B", "verbatim_name": "Vykon B"},
            {"code": "001", "name": "Vykon A", "verbatim_name": "verbatim 2"},
    ]}
    result = dedupe_vykony(matched_vykony)
    assert len(result) == 2
    assert result["001"]["verbatim_name"] == "verbatim 1, verbatim 2"
    