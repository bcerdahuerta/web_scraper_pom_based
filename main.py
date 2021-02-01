import argparse
import logging
import news_page_object as news
import re
import datetime
import csv

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

logging.basicConfig(level=logging.INFO)

from common import config


logger = logging.getLogger(__name__)


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info('Beginning scraper for {}'.format(host))
    logging.info('Finding links in homepage...')
    homepage = news.HomePage(news_site_uid, host)
    articles_list = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)

        if article:
            logger.info("Article fetched!!")
            articles_list.append(article)
            print(article.title)
    _save_articles(news_site_uid, articles_list)

def _save_articles(news_site_uid, articles_list):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(
        news_site_uid=news_site_uid,
        datetime=now)
    csv_headers =['title', 'body', 'url']

    with open(out_file_name, mode='w+', encoding= "utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles_list:
            row = [str(getattr(article,prop)) for prop in csv_headers]
            writer.writerow(row)


def _fetch_article(news_site_uid, host, link):
    logger.info("Start Fetching article at {}".format(link))
    article = None
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning("Errow while fetching the article", exc_info=False)
    if article and not article.body:
        logger.warning("Invalid article, no body",exc_info=False)
        return None
    return article


def _build_link(host, link):
    is_well_formed_link = re.compile('^https?://.+/.+$')
    is_root_path = re.compile('^/.+$')
    if is_well_formed_link.findall(link):
        return link
    elif is_root_path.findall(link):
        return '{}{}'.format(host, link)
    else:
        return '{}/{}'.format(host, link)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site',
                        help='The news site that you want to scrape',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)