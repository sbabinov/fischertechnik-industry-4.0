from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, validator
from typing import List
from src.factory import Factory
import json

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
    return {"success": True}

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
    return {"success": True}

@app.get("/status/{index}")
async def getStatus(index: int):
    isRunning = factory.getStatus(index)
    return {"isRunning": isRunning}

@app.post("/write/{storage}")
async def writeStorage(storage: str):
    try:
        storage_data = json.loads(storage)
        if not isinstance(storage_data, list) or not all(isinstance(row, list) 
                                                         for row in storage_data):
            return {"success": False}
        factory.writeStorage(storage_data)
        return {"success": True}
    except json.JSONDecodeError:
        return {"success": False}

@app.post("/process/color/{color}")
async def processColorCargo(color: int):
    for row in range(3):
        for col in range(3):
            if factory.getStorage(row, col) == color:
                factory.processCargo(row, col, wait=False)
                return {"success": True}
    return {"success": False}

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.137.1", port=8000)
