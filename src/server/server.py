from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, validator
from typing import List
from src.factory import Factory

factory = Factory()


class CargoResponse(BaseModel):
    row: int
    col: int
    state: int


class CargoListResponse(BaseModel):
    storage: List[CargoResponse] 
    

app = FastAPI()

@app.get("/")
async def main():
    return {"ok": "Hello world"}


@app.post("/sort")
async def sort():
    factory.sort()
    return {"sucess": True}

@app.get("/storage")
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

@app.post("/process/{row}/{col}")
async def processSingleCargo(row: int, col: int):
    factory.processCargo(row, col)
    return {"sucess": True}


@app.get("/status/{index}")
async def getStatus(index: int):
    isRunning = factory.getStatus(index)
    return {"isRunning": isRunning}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
