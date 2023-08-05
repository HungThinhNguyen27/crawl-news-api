from math import ceil
from datalayer.articles import Article
from datalayer.category import Category_
from flask import jsonify, request, url_for
from model.articles import OutputFormat, Category, News
from typing import List, Dict, Optional, Tuple


class ArticleService:
    def __init__(self) -> None:
        self.articles = Article()
        self.category = Category_()

    def search(self, page: int, limit: int, query: Optional[str]) -> Tuple[Dict[str, List[Dict[str, str]]], int]:

        offset = (page - 1) * limit
        articles = self.articles.search(query, limit, offset)
        total_count = self.articles.count(query)
        total_pages = (total_count + limit - 1) // limit
        articles_dict = []

        for article in articles:
            article_output = OutputFormat(article)
            article_dict = article_output.article_format()
            articles_dict.append(article_dict)

        next_page_url = None
        if page < total_pages:
            next_page_url = (
                f"{request.base_url}?key={query}&page={page + 1}&limit={limit}"
            )

        metadata = {
            "page_number": page,
            "items_per_page": limit,
            "total_count": total_count,
            "total_pages": total_pages,
            "current_url": request.url,
            "next_page_url": next_page_url,
        }
        return {"articles": articles_dict, "metadata": metadata}, total_pages

    def search_by_id(self, id: int) -> Tuple[Dict[str, str], Optional[News]]:
        search_article = self.articles.get_by_id(id)

        if search_article:
            article_output = OutputFormat(search_article)
            article_dict = article_output.article_format()
            return article_dict

    def delete_article_by_id(self, id: int) -> Optional[News]:
        search_article = self.articles.get_by_id(id)

        if search_article:
            self.articles.delete(search_article)
        return search_article

    def add_newspaper_page(self, name_article: str, url: str) -> Optional[Category]:

        categories = self.category.get()
        cat_url = [category.url for category in categories]
        if url == cat_url:
            return None

        new_article = Category(name=name_article, url=url)
        add_new_src_articles = self.category.add(new_article)
        return add_new_src_articles
