
from model.articles import News
from datalayer.database import Database


class ElasticSearch(Database):

    def add(self, news: News) -> None:
        body = {
            "id": id,
            "title": news.title,
            "content": news.content,
            "img_links": news.img_links,
            "original_url": news.original_url,
        }
        self.es.index(index="news", body=body)
