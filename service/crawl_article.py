import hashlib
import newspaper
import time
import schedule
from model.articles import Base, News, Category
from datalayer.articles import Article
from datalayer.category import Category_
from typing import Optional


class CrawlNewsService:
    def __init__(self) -> None:
        self.article = Article()
        self.category = Category_()

    def calculate_hash(self, text: str) -> str:
        md5 = hashlib.md5()
        md5.update(text.encode("utf-8", "ignore"))
        return md5.hexdigest()

    def check_hash_valid(self, hash: str):
        articles = self.article.get()
        for article in articles:
            if article.hash == hash:
                return None

    def add_new_articles(self, url: str, category: int) -> None:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        hash = self.calculate_hash(article.text)
        if not self.check_hash_valid(hash):
            print("Duplicated Post!")
        else:
            new_post_template = News(
                title=article.title,
                img_links=article.top_image,
                content=article.text,
                original_url=article.url,
                category_id=category,
                hash=hash,
            )
            self.article.add(new_post_template)

    def crawl_all_url_news(self) -> None:
        cats = self.category.get()
        for cat in cats:
            cat_id = cat.id
            cat_url = cat.url
            source = newspaper.build(cat_url)
            for subcat_url in source.category_urls():
                subcat_source = newspaper.build(subcat_url)
                for article in subcat_source.articles:
                    try:
                        print("====", article.url)
                        self.add_new_articles(article.url, cat_id)
                    except Exception as ex:
                        print(" Error : " + str(ex))

        self.article.commit()

    def crawl_one_url_news(self, url: str) -> Category:

        existing_article = self.category.get_by_url(url)
        source = newspaper.build(existing_article.url)
        for subcat_url in source.category_urls():
            subcat_source = newspaper.build(subcat_url)
            for article in subcat_source.articles:
                try:
                    print("====", article.url)
                    self.add_new_articles(article.url, existing_article.id)
                except Exception as ex:
                    print(" Error : " + str(ex))

        self.article.commit()
        return existing_article

    def run_everyday(self) -> None:
        schedule.every().day.at("16:09").do(self.crawl_all_url_news)
        allow_crawling = True
        start_time = time.time()
        while allow_crawling:
            schedule.run_pending()
            elapsed_time = time.time() - start_time
            if elapsed_time == 120:
                break
