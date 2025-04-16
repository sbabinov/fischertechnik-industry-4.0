from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import List
from src.stages.stage import Cargo
from src.factory import Factory

factory = Factory()

class CargoResponse(BaseModel):
    row: int
    col: int
    state: Cargo


class CargoListResponse(BaseModel):
    storage: List[CargoResponse] 
    

app = FastAPI()

@app.get("/")
async def main():
    return {"ok": "Hello world"}


@app.get("/storage", response_model=CargoListResponse)
async def getAllCargos():
    cargos = []
    for row in range(3):
        for col in range(3):
            cargo = factory.getStorage(row, col)
            cargos.append({
                "row": row,
                "col": col,
                "cargo": cargo
                })
    return {"storage": cargos}


@app.get("/storage/{row}/{col}")
async def getSingleCargo(row: int, col: int):
    cargo = factory.getStorage(row, col)
    return {"row": row,
            "col": col,
            "cargo": cargo}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
