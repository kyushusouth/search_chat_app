from opensearchpy import OpenSearch, helpers


def main():
    host = "localhost"
    port = 9200
    auth = ("admin", "sldfijaisoefjAAOSIEOIEFEI345345345@@@1@1")
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=False,
    )

    index_name = "products"
    index_body = {
        "settings": {
            "index": {"number_of_shards": 1},
            "analysis": {
                "char_filter": {
                    "normalize": {
                        "type": "icu_normalizer",
                        "name": "nfkc",
                        "mode": "compose",
                    }
                },
                "analyzer": {
                    "kuromoji_analyzer": {
                        "type": "custom",
                        "char_filter": ["normalize"],
                        "tokenizer": "kuromoji_tokenizer",
                        "filter": ["kuromoji_readingform"],
                    }
                },
            },
        },
        "mappings": {
            "properties": {
                "name": {
                    "type": "text",
                    "analyzer": "kuromoji_analyzer",
                    "search_analyzer": "kuromoji_analyzer",
                },
                "description": {
                    "type": "text",
                    "analyzer": "kuromoji_analyzer",
                    "search_analyzer": "kuromoji_analyzer",
                },
            }
        },
    }
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)
    client.indices.create(index=index_name, body=index_body)

    documents = [
        {
            "_id": 1,
            "name": "高機能コーヒードリッパー",
            "description": "誰でもプロの味を再現できるセラミック製のドリッパー。",
        },
        {
            "_id": 2,
            "name": "静音設計ワイヤレスキーボード",
            "description": "オフィスでも静かに使える。打鍵感が心地よいメカニカルキーボード。",
        },
        {
            "_id": 3,
            "name": "自動追尾型Webカメラ",
            "description": "AIが人物を認識し、常にフレームの中心に捉える高画質カメラ。",
        },
        {
            "_id": 4,
            "name": "アロマディフューザー加湿器",
            "description": "超音波でミストを発生させ、好きな香りでリラックス空間を演出。",
        },
    ]
    documents = [{"_index": index_name, **doc} for doc in documents]

    helpers.bulk(client, documents, max_retries=5)


if __name__ == "__main__":
    main()
