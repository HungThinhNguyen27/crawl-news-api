
from model.articles import News
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from config import Config
from typing import List, Dict
from datalayer.articles import Article

INDEX = Config.INDEX
ES_HOST = Config.ES_HOST


elasticsearch = Elasticsearch(hosts=[ES_HOST])


class ElasticSearch_:

    def __init__(self) -> None:
        self.es = elasticsearch
        self.articles = Article()

    def add_data(self):
        articles = self.articles.get()
        actions = [
            {
                "_index": INDEX,
                "_source": {
                    "title": article.title,
                    "content": article.content,
                }
            }
            for article in articles
        ]
        bulk(self.es, actions)

    def search_document(self, query, field_name) -> Dict:
        result = self.es.search(
            request_timeout=30,
            index=INDEX,
            body={
                'query': {
                    'match': {
                        field_name: {
                            'query': query
                        }
                    }
                }
            }
        )

        return result
