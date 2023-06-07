from math import ceil
from articles_datalayer import ArticleMysql
from flask import jsonify, request, url_for
from model import ArticleOutput, Category, News
from typing import List, Dict, Optional, Tuple


class ArticleService:
    def __init__(self) -> None:
        self.datalayer = ArticleMysql()

    def search_all_articles(
        self, page: int, limit: int, query: Optional[str]
    ) -> Tuple[Dict[str, List[Dict[str, str]]], int]:
        
        offset = (page - 1) * limit
        articles = (
            self.datalayer.get_first_articles(query)
            if query
            else self.datalayer.get_all_articles()
        )
        total_count = len(articles)
        total_pages = (total_count + limit - 1) // limit

        paginated_articles = articles[offset : offset + limit]
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
        search_article = self.datalayer.get_articles_by_id(id)

        if search_article:
            article_output = ArticleOutput(search_article)
            article_dict = article_output.output()
            return article_dict, search_article

    def delete_article_by_id(self, id: int) -> Optional[News]:
        search_article = self.datalayer.get_articles_by_id(id)
        if search_article:
            self.datalayer.delete_article_by_id(search_article)
            return search_article

    def create_new_src_article(self, name_article: str, url: str) -> Optional[Category]:
        check_src_article = self.datalayer.get_category_url(url)

        if check_src_article:
            return check_src_article

        new_article = Category(name=name_article, url=url)

        add_new_src_articles = self.datalayer.add_new_src_articles(new_article)

        return add_new_src_articles
