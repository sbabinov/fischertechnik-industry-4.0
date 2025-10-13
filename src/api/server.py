from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
from ..models import CargoListRequest, CoordsListRequest

def create_app(factory, host: str = "127.0.0.1", port: int = 8000):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("start")
        worker_task = asyncio.create_task(async_worker())
        yield

        nonlocal stop_flag
        stop_flag = True
        await task_queue.join()
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass
        print("stop")

    app = FastAPI(lifespan=lifespan)
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

    @app.get("/get_status")
    def get_status():
        return factory.get_status()

    @app.get("/queue_status")
    async def queue_status():
        return {
            "queue_size": task_queue.qsize(),
            "tasks_in_progress": task_queue._unfinished_tasks
        }

    return app, host, port
