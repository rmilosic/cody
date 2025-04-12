# ruff: noqa: D101

import pytest
from dotenv import load_dotenv
from langsmith import testing as t

from agent.graph import graph

load_dotenv()


@pytest.mark.langsmith
async def test_sql_generation_select_all() -> None:
    sql = await graph.ainvoke({"report": "1234"})
    assert sql is None
