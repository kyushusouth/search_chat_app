from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opensearchpy import OpenSearch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


host = "opensearch-node1"
port = 9200
auth = ("admin", "sldfijaisoefjAAOSIEOIEFEI345345345@@@1@1")
client = OpenSearch(
    hosts=[{"host": host, "port": port}],
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
)


@app.get("/")
def read_root():
    return {"message": "Search API is running!"}


@app.get("/search")
def search_products(q: str):
    if not q:
        return {"hits": []}

    query = {"query": {"multi_match": {"query": q, "fields": ["name", "description"]}}}

    response = client.search(index="products", body=query)

    hits = [hit["_source"] for hit in response["hits"]["hits"]]
    return {"hits": hits}
