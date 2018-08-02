from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from math import ceil
import json, sys, argparse, validators

MAX_NUM_POSTS = 100

class HackerNewsScraper:
    URL = 'https://news.ycombinator.com/news'

    def __init__(self, posts):
        self._total_posts = posts
        self._total_pages = int(ceil(posts/30))
        self._stories = []

    
    def scrape_stories(self):
        page = 1

        while(page <= self._total_pages):
            url = '{}?p={}'.format(self.URL, page)
            
            html = get_html(url)
            self.parse_stories(html)
            page += 1


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
            
            story = validate_story(story)
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


def validate_story(story):
    if not valid_title(story['title']):
        story['title'] = 'Valid title not found'

    if not valid_author(story['author']):
        story['author'] = 'Valid author not found'

    if not valid_uri(story['uri']):
        story['uri'] = 'Valid URI not found'

    story['comments'] = validate_number(story['comments'])
    story['points'] = validate_number(story['points'])
    story['rank'] = validate_number(story['rank'])

    return story


def valid_title(title):
    return (len(title) <= 256 and title)


def valid_author(author):
    if(author.find(' ') > -1):  #Hacker news username doesnt support whitespace
        return False
    return (len(author) <= 256 and author)


def valid_uri(url):
    if(validators.url(url)):
        return True
    return False


def validate_number(numString):
    if numString.find('ago') > -1:      #If not found, time since posted would replace points
        return 0
    
    digits = [int(s) for s in numString.split() if s.isdigit()]

    if len(digits) > 0:
        return digits[0]
    return 0


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
#        print(posts)
        hnews_scraper = HackerNewsScraper(posts)
        hnews_scraper.scrape_stories()
        hnews_scraper.print_stories()

    except argparse.ArgumentTypeError as ex:
        log_error(ex)


if __name__ == '__main__':
    main()
