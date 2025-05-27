
from typing import Any, Dict, List, Literal, Optional, Union
from typing import Annotated
from typing_extensions import TypedDict

from pydantic import BaseModel, Field

# Pydantic
class Material(BaseModel):
    """Material basic definition"""
    verbatim_name: str = Field(description="verbatim name of the material")
    brand: Union[str, None] = Field(description="brand of the material")
    package_size: Union[str, None] = Field(description="package size")
    size: Union[str, None] = Field(description="product size (S/M/L) or metric/inch units")
    
class ProcessedData(BaseModel):
    """Processed Data."""
    text: str = Field(description="initial text")
    vykony: Union[List[str], None] = Field(description="provedeni vykony")
    materialy: Optional[List[Material]] = Field(description="pouzite materialy a zdravotnicke pomucky") 


class ProcessOutput(BaseModel):
    """Output from text processing."""
    data: dict

class MatchedMaterial(Material):
    """Matched material from text against official list"""
    code: str = Field(description="code of the material")

class State(TypedDict):
    """Graph state"""
    text: str
    odbornost: str
    diag_primary: str
    diag_others: Optional[List[str]] = None
    vykony: Optional[List[str]] = None
    materialy: Optional[List[Material]] = None