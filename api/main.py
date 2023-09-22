import random
import string
import time

from fastapi import FastAPI, Query, Request
from api.common.logger_handler import create_logger
from api.router import index
from api.schema.main import GetMainModel

app = FastAPI()

app.include_router(index.router)

test_logger = create_logger("test-log")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    print(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    formatted_process_time = "{0:.3f}".format(process_time)
    print(
        f"rid={idem} completed_in={formatted_process_time}s status_code={response.status_code}"
    )

    return response


@app.get("/")
async def root(items: list = Query([])) -> GetMainModel:
    print(items)
    return GetMainModel(result="success")
