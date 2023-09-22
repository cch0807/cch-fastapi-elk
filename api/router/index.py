from elasticsearch import Elasticsearch
from fastapi import APIRouter, Depends, HTTPException, Query

from api.schema.test import CreateIndexDataModel, CreateIndexModel
from api.service.index import IndexService


router = APIRouter(prefix="/index")


@router.get("", status_code=200)
async def get_index_handler(
    index_name: str, index_service: IndexService = Depends(IndexService)
):
    try:
        res = index_service.get_index(index_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Index does not exists")
    return {"result": res}


@router.post("", status_code=201)
async def create_index_handler(
    index: CreateIndexModel, index_service: IndexService = Depends(IndexService)
) -> None:
    index_name = index.indexname

    res = index_service.create_index(index_name)

    if not res:
        raise HTTPException(status_code=400, detail="Bad Request")

    return {"result": res}


@router.delete("", status_code=204)
async def delete_index_handler(
    index_name: str, index_service: IndexService = Depends(IndexService)
):
    print(index_name)
    index_service.delete_index(index_name=index_name)


@router.get("/data", status_code=200)
async def get_index_data_handler(
    query_key: str = 1,
    query_value: str = 1,
    size: int = 1,
    index_name: list = Query([]),
    index_service: IndexService = Depends(IndexService),
):
    es: Elasticsearch = index_service.get_es()
    index = index_name
    body = {"size": size, "query": {"match": {query_key: query_value}}}
    try:
        es.search(index=index, body=body)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Bad Request")
    result = es.search(index=index, body=body)

    return {"result": result}


@router.get("/data/all", status_code=200)
async def get_index_data_all_handler(
    size: int = 100,
    scroll: str = "1m",
    index_name: list = Query([]),
    index_service: IndexService = Depends(IndexService),
):
    es: Elasticsearch = index_service.get_es()
    index_name = index_name
    body = {"size": size, "query": {"match_all": {}}}
    response = es.search(index=index_name, body=body, scroll=scroll)

    res = []
    while True:
        results = response["hits"]["hits"]

        for hit in results:
            res.append(hit["_source"])

        scroll_id = response["_scroll_id"]
        response = es.scroll(scroll_id=scroll_id, scroll=scroll)

        if not results:
            break

    return {"result": res}


@router.post("/data", status_code=201)
async def create_index_data_handler(
    request: CreateIndexDataModel,
    index_name: str,
    index_service: IndexService = Depends(IndexService),
):
    index_service.create_index_data(index_name=index_name, data=request.data)
    return {"result": request}
