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
    factory.sort(wait=False)
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
    factory.processCargo(row, col, wait=False)
    return {"sucess": True}

@app.get("/status/{index}")
async def getStatus(index: int):
    isRunning = factory.getStatus(index)
    return {"isRunning": isRunning}

@app.post("/write/{storage}")
async def writeStorage(storage: List[List[int]]):
    factory.writeStorage(storage)
    return {"sucess": True}

@app.post("/process/color/{color}")
async def processColorCargo(color: int):
    for row in range(3):
        for col in range(3):
            if factory.getStorage(row, col) == color:
                factory.processCargo(row, col, wait=False)
                return {"sucess": True}
    return {"sucess": False}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
