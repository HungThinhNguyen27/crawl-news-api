import hashlib
import newspaper
import time
import schedule
from model import Base, News, Category
from datalayer import CrawlDataMysql


class CrawlNewsService:
    def __init__(self):
        self.datalayer = CrawlDataMysql()

    def calculate_hash(self, text):
        md5 = hashlib.md5()
        md5.update(text.encode("utf-8", "ignore"))
        return md5.hexdigest()

    def add_new_articles(self, url, category):
        article = newspaper.Article(url)
        article.download()
        article.parse()
        hash = self.calculate_hash(article.text)

        if not self.datalayer.detect_duplicate(hash):
            new_post_template = News(
                title=article.title,
                img_links=article.top_image,
                content=article.text,
                original_url=article.url,
                category_id=category,
                hash=hash,
            )

            add_new_post_template = self.datalayer.add_new_post(new_post_template)

        else:
            print("Duplicated Post!")

    def crawl_all_news(self):
        cats = self.datalayer.query_all_src_news()

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

        self.datalayer.commit()

    def crawl_one_news(self, url):
        existing_article = self.datalayer.query_url_src_news(url)

        source = newspaper.build(existing_article.url)

        for subcat_url in source.category_urls():
            subcat_source = newspaper.build(subcat_url)
            for article in subcat_source.articles:
                try:
                    print("====", article.url)
                    self.add_new_articles(article.url, existing_article.id)
                except Exception as ex:
                    print(" Error : " + str(ex))

        self.datalayer.commit()
        return existing_article

    def run_everyday(self):
        schedule.every().day.at("11:29").do(self.crawl_all_news)
        allow_crawling = True
        start_time = time.time()

        while allow_crawling:
            schedule.run_pending()
            elapsed_time = time.time() - start_time
            if elapsed_time == 120:
                break
