from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

import sys
from pathlib import Path

# Добавляем родительскую папку (fischer-technik) в PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from factory import Factory
from stages.stage import Cargo
import uvicorn
import asyncio
import json

class CargoListRequest(BaseModel):
    cargos: List[List[Cargo]]

class CoordsListRequest(BaseModel):
    coords: List[List[int]]

with open("config.json", 'r') as file:
    ips = json.load(file)
factory = Factory(ips)

task_queue = asyncio.Queue()
stop_flag = False

async def async_worker():
    while not stop_flag:
        try:
            task_func, kwargs = await task_queue.get()
            print(f"STATUS:\t  Starting task { task_func.__name__ }")
            await task_func(**kwargs)
            print(f"STATUS:\t  Finished task { task_func.__name__ }")
            task_queue.task_done()
        except Exception as e:
            print(f"STATUS:\t  Task failed: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(async_worker())
    yield
    global stop_flag
    stop_flag = True
    await task_queue.join()

app = FastAPI(lifespan=lifespan)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(async_worker())

@app.on_event("shutdown")
async def shutdown_event():
    global stop_flag
    stop_flag = True
    await task_queue.join()

@app.post("/write_storage")
async def run_task1(request: CargoListRequest):
    await task_queue.put((factory.write_storage, { "new_storage": request.cargos }))
    return { "status": "queued", "task": "write_storage"}

@app.post("/process_cargos")
async def run_task2(request: CoordsListRequest):
    await task_queue.put((factory.process_cargos, { "coords": request.coords }))
    return { "status": "queued", "task": "process_cargos" }

@app.post("/return_cargos")
async def run_task3(request: CargoListRequest):
    await task_queue.put((factory.return_cargos, { "new_storage": request.cargos }))
    return { "status": "queued", "task": "return_cargos" }

@app.post("/sort_cargos")
async def run_task4(request: CargoListRequest):
    await task_queue.put((factory.sort_cargos, { "new_storage": request.cargos }))
    return { "status": "queued", "task": "sort_cargos" }

@app.get("/get_storage")
def get_storage():
    return factory.get_storage()

@app.get("/queue_status")
async def queue_status():
    return {
        "queue_size": task_queue.qsize(),
        "tasks_in_progress": task_queue._unfinished_tasks
    }

if __name__ == "__main__":
    uvicorn.run(app, host="10.160.58.154", port=8000)
