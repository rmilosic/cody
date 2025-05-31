
from typing import Any, Dict, List, Literal, Optional, Union
from typing import Annotated
from typing_extensions import TypedDict

from pydantic import BaseModel, Field

# Pydantic
class Material(BaseModel):
    """Material basic definition - only for medicine equipment/device, not medicines """
    verbatim_name: str = Field(description="verbatim name of the device/supply/equipment")
    brand: Union[str, None] = Field(description="brand of the material")
    package_size: Union[str, None] = Field(description="package size")
    size_unit: Union[str, None] = Field(description="package size units")
    variation: Union[str, None] = Field(description="variation of the product size (S/M/L) or color")
    
class ProcessedData(BaseModel):
    """Processed Data."""
    text: str = Field(description="initial text")
    vykony: Union[List[str], None] = Field(description="provedeni vykony")
    materialy: Optional[List[Material]] = Field(description="pouzite materialy a zdravotnicke pomucky") 


class Vykon(BaseModel):
    """Vykon basic definition."""
    verbatim_name: Optional[str] = Field(description="verbatim name of the vykon")

class MatchedVykon(Vykon):
    """Matched vykon from text against official list"""
    code: str = Field(description="code of the vykon")
    name: str = Field(description="name of the vykon")
    description: str = Field(description="description of the vykon")

    
class MatchedVykony(BaseModel):
    """Matched vykon from text against official list"""
    results: List[MatchedVykon] = Field(description="matched vykony from text")
    results_deduped: Optional[Dict[str, MatchedVykon]] = Field(description="deduplicated vykony by code")

class ProcessOutput(BaseModel):
    """Output from text processing."""
    data: dict

class MatchedMaterial(Material):
    """Matched material from text against official list"""
    code: Optional[str] = Field(description="code of the material")
    name: Optional[str] = Field(description="name of the material")

class MatchedMaterials(BaseModel):
    results: List[MatchedMaterial] = Field(description="matched materials from text")


class State(TypedDict):
    """Graph state"""
    text: str
    odbornost: str
    diag_primary: str
    diag_others: Optional[List[str]] = None
    vykony: Optional[MatchedVykony] = None
    materialy: Optional[MatchedMaterials] = None
    # leky: Optional[List[Material]] = None