from common import config
import requests
import bs4

class NewsPage():

    def __init__(self, news_site_uid, url):
        self._config = config()["news_sites"][news_site_uid]
        self.queries = self._config["queries"]
        self._url = url
        self._html = None
        self._visit(url)
    
    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()

        self._html = bs4.BeautifulSoup(response.text, "html.parser")

class HomePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)
        self._config = config()["news_sites"][news_site_uid]
        self.queries = self._config["queries"]
        self._html = None
        self._visit(url)


    @property
    def article_links(self):

        link_list = []
        for link in self._select(self.queries["homepage_article_links"]):
            if link and link.has_attr("href"):
                link_list.append(link)
        return set(link["href"] for link in link_list)

class ArticlePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def title(self):
        result = self._select(self.queries["article_title"])
        return result[0].text if result != None and len(result) else ''

    @property
    def body(self):
        result = self._select(self.queries["article_body"])
        return result[0].text if result != None and len(result) else ''

    @property
    def url(self):
        return self._url