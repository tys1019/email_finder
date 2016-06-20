import argparse
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from time import time
from urlparse import urlparse
from requests.exceptions import InvalidURL, ReadTimeout, ConnectionError


parser = argparse.ArgumentParser(description='Find all email addresses on a domain.')
parser.add_argument('domain', help="The web domain to search for email addresses (example.com)")
parser.add_argument('--browser', '-b', action='store_true', help="Use selenium to load the page in a headless browser.")

args = parser.parse_args()
DOMAIN = args.domain

def make_url(url):
    url = url if url.startswith('http') else u"http://{}".format(url)
    return url

def get_html(url):
    """Gets the HTML content for a website using selenium or requests."""

    if args.browser:
        driver.get(url)
        return driver.page_source

    else:
        try:
            request = requests.get(url, timeout=5)
            return request.content
        except (InvalidURL, ReadTimeout, ConnectionError) as e:
            return ''

def get_mailto_links(soup):
    """
    Finds all mailto links and return just the email addresses

    Args:
        soup: a BeautifulSoup processed html object
    """

    mailto_links = set()
    for a in soup.find_all('a'):
        if a.get('href', '').startswith('mailto:') and "@" in a['href']:
            mailto_links.add(a['href'].replace('mailto:', ''))
    return mailto_links

def get_follow_links(soup):
    """
    Finds all links within a domain and returns a set of urls.

    Args:
        soup: a BeautifulSoup processed html object
    """

    links = set()
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if urlparse(href).netloc == DOMAIN:
            links.add(make_url(a.get('href')))

        elif href.startswith('/'):
            links.add(make_url(u"{}{}".format(DOMAIN_URL, href)))

    # Get all Angular redirects
    for s in soup.find_all('span'):
        ng_click = s.get('ng-click', '')
        if 'changeRoute' in ng_click:
            path = ng_click.replace("changeRoute('", '').replace("')", '')
            links.add(make_url(u"{}/{}".format(DOMAIN_URL, path)))

    return links


# Build a running set of urls to visit, ones that have been visited and emails
try:
    DOMAIN_URL = make_url(DOMAIN)
    if args.browser:
        driver = webdriver.PhantomJS()

    visited_urls = set()
    all_urls = {DOMAIN_URL}
    mailto_links = set()

    while all_urls - visited_urls:
        for url in all_urls - visited_urls:
            start = time()

            html = get_html(url)
            soup = BeautifulSoup(html, 'lxml')

            all_urls.update(get_follow_links(soup))
            mailto_links.update(get_mailto_links(soup))

            visited_urls.add(url)

            loading_time = round(time() - start, 2)

            print u"{}. Loaded {} in {}s".format(len(visited_urls), url, loading_time)

except Exception, e:
    raise e

finally:
    if args.browser:
        driver.quit()
    print u"Found these email addresses:\n{}".format('\n'.join(mailto_links))
