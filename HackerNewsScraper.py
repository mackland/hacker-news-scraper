from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json, sys, argparse

MAX_NUM_POSTS = 100

class HackerNewsScraper:
    URL = 'https://news.ycombinator.com/news'

    def __init__(self, posts):
        self._total_posts = posts
        self._stories = []

    def scrape_stories(self):
        html = get_html(self.URL)
        self.parse_stories(html)

    def parse_stories(self, html):
        for storytext, subtext in zip(html.find_all('tr', {'class': 'athing'}),
                                    html.find_all('td', {'class': 'subtext'})):
            
            storylink = storytext.find_all('a',{'class':'storylink'})
            sublink = subtext.select('a')

            title = storylink[0].text.strip()
            uri = storylink[0]['href']
            author = sublink[0].text
            comments = sublink[-1].text
            points = subtext.select('span')[0].text
            rank = storytext.select('span.rank')[0].text.strip('.')

            story = {
                    'title' : title,
                    'uri' : uri,
                    'author' : author,
                    'comments' : comments,
                    'points' : points,
                    'rank' : rank
                    }

            self._stories.append(story)
            if len(self._stories) >= self._total_posts:
                return
    
    def print_stories(self):
        json.dump(self._stories, sys.stdout, indent=4)


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
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

def validate_input(arg, arg_max):
    error_msg = 'Posts cannot exceed {}'.format(arg_max)
    if arg > arg_max:
        raise argparse.ArgumentTypeError(error_msg)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--posts', '-p', metavar='n', type=int, default=10, help='number of posts (max 100)')
    args = parser.parse_args()

    validate_input(args.posts, MAX_NUM_POSTS)

    return args.posts

def main():
    try:
        posts = parse_arguments()

        hnews_scraper = HackerNewsScraper(posts)
        hnews_scraper.scrape_stories()
        hnews_scraper.print_stories()

    except argparse.ArgumentTypeError as ex:
        log_error(ex)

if __name__ == '__main__':
    main()
