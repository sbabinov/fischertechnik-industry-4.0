from pydantic import BaseModel
from typing import List
from ..core.stages.stage import Cargo

class CargoListRequest(BaseModel):
    cargos: List[List[Cargo]]

class CoordsListRequest(BaseModel):
    coords: List[List[int]]
