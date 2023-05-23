from math import ceil
from datalayer import ArticleMysql
from flask import jsonify, request, url_for
from model import ArticleOutput, category
from flask_jwt_extended import get_jwt_identity


class ArticleService:
    def __init__(self):
        self.datalayer = ArticleMysql()

    def get_all_articles(self, page, limit, query):
        offset = (page - 1) * limit
        articles, total_count = self.datalayer.get_all_articles(query, limit, offset)

        total_pages = int(ceil(total_count / limit))
        articles_dict = []

        for article in articles:
            article_output = ArticleOutput(article)
            article_dict = article_output.output()
            articles_dict.append(article_dict)

        next_page = page + 1 if page < total_pages else None

        if query:
            next_page_url = (
                url_for(
                    "article.get_all_articles", limit=limit, page=next_page, key=query
                )
                if next_page
                else None
            )
        else:
            next_page_url = (
                url_for("article.get_all_articles", limit=limit, page=next_page)
                if next_page
                else None
            )

        metadata = {
            "page_number": page,
            "items_per_page": limit,
            "total_count": total_count,
            "total_pages": total_pages,
            "current_url": request.url,
            "next_page_url": next_page_url,
        }

        return {"articles": articles_dict, "metadata": metadata}, int(total_pages)

    def search_article_by_id(self, id):
        search_article = self.datalayer.get_article_by_id(id)

        if search_article:
            article_output = ArticleOutput(search_article)
            article_dict = article_output.output()
            return article_dict, search_article

    def delete_article_by_id(self, id):
        search_article = self.datalayer.get_article_by_id(id)
        if search_article:
            self.datalayer.delete_article_by_id(search_article)
            return search_article

    def create_new_src_article(self, name_article, url):
        check_src_article = self.datalayer.check_existing_src_article(url)

        if check_src_article:
            return check_src_article

        new_article = category(name=name_article, url=url)

        add_new_src_articles = self.datalayer.add_new_src_articles(new_article)

        return add_new_src_articles
