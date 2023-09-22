import timeit
from elasticsearch import Elasticsearch

# Elasticsearch 호스트 및 포트 설정
es = Elasticsearch([{"host": "localhost", "port": 9200}])

# 검색 대상이 될 인덱스 리스트
index_list = ["samsung", "apple"]


# 데이터 추출을 위한 함수
def extract_data_from_indices(indices):
    data = []
    for index in indices:
        # match_all 쿼리를 사용하여 해당 인덱스에서 모든 데이터 검색
        query = {"size": 100, "query": {"match_all": {}}}
        result = es.search(index=index, body=query, scroll="1m")

        # 검색 결과에서 문서 데이터 추출
        hits = result["hits"]["hits"]
        for hit in hits:
            data.append(hit["_source"])

    return data


def test():
    query = {"size": 1000, "query": {"match_all": {}}}
    response = es.search(index="samsung", body=query, scroll="1m")
    # 여러 인덱스에서 데이터 추출
    # all_data = extract_data_from_indices(index_list)

    while True:
        results = response["hits"]["hits"]

        for hit in results:
            print(hit["_source"])

        scroll_id = response["_scroll_id"]
        response = es.scroll(scroll_id=scroll_id, scroll="1m")

        if not results:
            break


# 추출한 데이터 사용
# for document in all_data:
#     print(document)

print(timeit.timeit(test, number=1))
