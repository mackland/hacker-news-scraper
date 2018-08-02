from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

class HackerNewsScraper:

    def __init__(self, posts):

    def scrape_stories(self):

    def parse_stories(self, html):

    def print_stories(self, stories):

def get_html(url):
    response = get_response(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')

    return html

def get_response(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):

def log_error(e):

if __name__ == '__main__':

