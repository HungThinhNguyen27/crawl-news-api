from math import ceil
from datalayer.articles import Article
from datalayer.category import Category_
from flask import jsonify, request, url_for
from model.articles import ArticleOutput, Category, News
from typing import List, Dict, Optional, Tuple


class ArticleService:
    def __init__(self) -> None:
        self.articles = Article()
        self.category = Category_()

    def search_all_articles(
        self, page: int, limit: int, query: Optional[str]
    ) -> Tuple[Dict[str, List[Dict[str, str]]], int]:

        offset = (page - 1) * limit
        articles, total_count = self.articles.search(query, limit, offset)
        total_pages = (total_count + limit - 1) // limit

        paginated_articles = articles[offset: offset + limit]
        articles_dict = []

        for article in paginated_articles:
            article_output = ArticleOutput(article)
            article_dict = article_output.output()
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

    def search_article_by_id(self, id: int) -> Tuple[Dict[str, str], Optional[News]]:
        search_article = self.articles.get(id)

        if search_article:
            article_output = ArticleOutput(search_article)
            article_dict = article_output.output()
            return article_dict, search_article

    def delete_article_by_id(self, id: int) -> Optional[News]:
        search_article = self.articles.get(id)
        if search_article:
            self.articles.delete(search_article)
            return search_article

    def create_new_src_article(self, name_article: str, url: str) -> Optional[Category]:
        check_src_article = self.category.get_category_url(url)

        if check_src_article:
            return check_src_article

        new_article = Category(name=name_article, url=url)

        add_new_src_articles = self.articles.add(new_article)

        return add_new_src_articles
