# ruff: noqa: D101

"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Dict, Literal, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from pydantic import BaseModel


class V43629(BaseModel):
    code: Literal[43629]
    description: Literal[
        "VÝROBA INDIVIDUÁLNÍCH FIXAČNÍCH POM��CEK PRO OZAŘOVÁNÍ NEBO MULÁŽ"
    ]


class V43023(BaseModel):
    code: Literal[43023]
    description: Literal["KONTROLNÍ VYŠETŘENÍ RADIAČNÍM ONKOLOGEM"]


class V42023(BaseModel):
    code: Literal[42023]
    description: Literal["KONTROLNÍ VYŠETŘENÍ KLINICKÝM ONKOLOGEM"]


class V42520(BaseModel):
    code: Literal[42520]
    description: Literal["APLIKACE PROTINÁDOROVÉ TERAPIE"]


class V42021(BaseModel):
    code: Literal[42021]
    description: Literal["KOMPLEXNÍ VYŠETŘENÍ KLINICKÝM ONKOLOGEM"]


class V43425(BaseModel):
    code: Literal[43425]
    description: Literal["PLÁNOVÁNÍ BRACHYTERAPIE S POUŽITÍM TPS (PLÁNOVACÍ KONZOLA)"]


class V42510(BaseModel):
    code: Literal[42510]
    description: Literal[
        "NÁROČNÁ APLIKACE REŽIM�� LÉČBY CYTOSTATIKY (1 DEN, NEZAHRNUJE PŘÍPRAVU LÉČIV)"
    ]


class V43021(BaseModel):
    code: Literal[43021]
    description: Literal["KOMPLEXNÍ VYŠETŘENÍ RADIAČNÍM ONKOLOGEM"]


class V43633(BaseModel):
    code: Literal[43633]
    description: Literal[
        "RADIOTERAPIE POMOCÍ URYCHLOVAČE ČÁSTIC S POUŽITÍM TECHNIKY IMRT (1 POLE)"
    ]


class V43621(BaseModel):
    code: Literal[43621]
    description: Literal["LOKALIZACE CÍLOVÉHO OBJEMU, NEBO SIMULACE OZAŘOVACÍHO PLÁNU"]


class V43022(BaseModel):
    code: Literal[43022]
    description: Literal["CÍLENÉ VYŠETŘENÍ RADIAČNÍM ONKOLOGEM"]


class V42022(BaseModel):
    code: Literal[42022]
    description: Literal["CÍLENÉ VYŠETŘENÍ KLINICKÝM ONKOLOGEM"]


class V43631(BaseModel):
    code: Literal[43631]
    description: Literal["PLÁNOVÁNÍ RADIOTERAPIE TECHNIKOU IMRT"]


class V43413(BaseModel):
    code: Literal[43413]
    description: Literal["HDR BRACHYTERAPIE POVRCHOVÁ S POMOCÍ AFTERLOADINGU"]


class V43315(BaseModel):
    code: Literal[43315]
    description: Literal[
        "RADIOTERAPIE LINEÁRNÍM URYCHLOVAČEM S POUŽITÍM FIXAČNÍCH POM��CEK, BLOK��, KOMPENZÁTOR�� APOD. (1 POLE)"
    ]


class V43317(BaseModel):
    code: Literal[43317]
    description: Literal[
        "DIBH – RADIOTERAPIE V HLUBOKÉM NÁDECHU - JEDNO POLE Á 4 MINUTY"
    ]


class V43623(BaseModel):
    code: Literal[43623]
    description: Literal["PŘÍMÁ DOZIMETRIE NA NEMOCNÉM (1 M��ŘÍCÍ MÍSTO)"]


class V43635(BaseModel):
    code: Literal[43635]
    description: Literal["PLÁNOVÁNÍ STEREOTAKTICKÉ RADIOTERAPIE A RADIOCHIRURGIE"]


class V43601(BaseModel):
    code: Literal[43601]
    description: Literal[
        "CT VYŠETŘENÍ PRO PLÁNOVÁNÍ RADIOTERAPIE BEZ POUŽITÍ KONTRASTNÍ LÁTKY"
    ]


class Diagnosis(BaseModel):
    diagnosis: list[
        V43629
        | V43023
        | V42023
        | V42520
        | V42021
        | V43425
        | V42510
        | V43021
        | V43633
        | V43621
        | V43022
        | V42022
        | V43631
        | V43413
        | V43315
        | V43317
        | V43623
        | V43635
        | V43601
    ]


@dataclass(kw_only=True)
class Configuration:
    """The configuration for the agent."""

    # Changeme: Add configurable values here!
    # these values can be pre-set when you
    # create assistants (https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/)
    # and when you invoke the graph
    my_configurable_param: str = "changeme"

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""
        configurable = (config.get("configurable") or {}) if config else {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})


class State(BaseModel):
    report: str = "example"
    diagnosis: Diagnosis | None = None


async def my_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Each node does work."""
    configuration = Configuration.from_runnable_config(config)

    diagnosis = (
        await ChatOpenAI(model="gpt-4o-mini", temperature=1)
        .with_structured_output(Diagnosis)
        .ainvoke(
            [
                SystemMessage(
                    content="Extract the diagnosis from the text. Try to match as many codes as possible"
                ),
                HumanMessage(content=state.report),
            ]
        )
    )

    return {"diagnosis": diagnosis}


workflow = StateGraph(State, config_schema=Configuration)
workflow.add_node("my_node", my_node)
workflow.add_edge("__start__", "my_node")

graph = workflow.compile()
graph.name = "New Graph"  # This defines the custom name in LangSmith
