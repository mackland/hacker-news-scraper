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
        """
        Fetches all HTML data.
        Each page is limited to 30 stories, this function will ensure enough pages are fetched.
        """
        page = 1

        while(page <= self._total_pages):           # Makes sure to visit sufficient amount of pages
            url = '{}?p={}'.format(self.URL, page)
            
            html = get_html(url)
            self.parse_stories(html)
            page += 1

    
    def parse_stories(self, html):
        """
        Given a BeautifulSoup nested data structure, html. parse_stories(html) will parse the data and select the desired fields.
        After getting title, uri, author, comments, points, and rank, it will save them in dictionary form in self._stories.
        """
        for storytext, subtext in zip(html.find_all('tr', {'class': 'athing'}),
                                    html.find_all('td', {'class': 'subtext'})):
            
            storylink = storytext.find_all('a',{'class':'storylink'})
            sublink = subtext.select('a')
            
            # All requested data being saved in the dictionary story below
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
                    'points' : points,
                    'comments' : comments,
                    'rank' : rank
                    }

            # Make sure data satisfies requirements
            story = validate_story(story)
            
            # self._stories is an array of dictionaries that saves the requested number of stories
            self._stories.append(story)
            
            # If required number of stories met, stop parsing
            if len(self._stories) >= self._total_posts:
                return
    
    
    def print_stories(self):
        """
        Outputs the stories from list of dictionary format to JSON in STDOUT.
        """
        json.dump(self._stories, sys.stdout, indent=4)
    
    
    def get_stories(self):
        """
        Returns the scraped stories to the user in a list of dictionary format.
        Used for testing purposes.
        """
        return self._stories


def get_html(url):
    """
    Runs the HTML data through BeautifulSoup to get a BeautifulSoup object, a nested data structure.
    """
    response = get_response(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')

    return html


def validate_story(story):
    """
    Ensures that all the story data is valid according to the task.
    Will return valid data for each field.
    """
    story['title'] = story['title'][:256]
    if not valid_title(story['title']):
        story['title'] = 'Valid title not found'
    
    story['author'] = story['author'][:256]
    if not valid_author(story['author']):
        story['author'] = 'Valid author not found'

    if not valid_uri(story['uri']):
        story['uri'] = 'Valid URI not found'

    story['comments'] = validate_number(story['comments'])
    story['points'] = validate_number(story['points'])
    story['rank'] = validate_number(story['rank'])

    return story


def valid_title(title):
    """
    Ensures that title is non empty string with <= 256 characters
    """
    return (len(title) <= 256 and title)


def valid_author(author):
    """
    Ensures that author is non empty string and <= 256 characters.
    Solved the issue of not finding an author by checking the fetched data with HN username rules.
    """
    if(author.find(' ') > -1):  #Hacker news username doesnt support whitespace
        return False
    return (len(author) <= 256 and author)


def valid_uri(url):
    """
    To be able to find the scraped stories, we need their URL.
    If data is not a valid URL, return False.
    """
    if(validators.url(url)):
        return True
    return False


def validate_number(numString):
    """
    Will make sure that the returned number is an integer.
    Will strip any non digits from the input and return the first number.
    """
    if numString.find('ago') > -1:      #If not found, 'time since posted' would replace points for example
        return 0
    
    digits = [int(s) for s in numString.split() if s.isdigit()]

    if len(digits) > 0:
        return digits[0]
    return 0


def get_response(url):
    """
    Attempts to get the content at 'url' by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
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
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    Log the errors. Currently just printing them out to user.
    """
    print(e)


def validate_input(arg, arg_max):
    """
    Validate the user input. Makes sure it is less than or equal to 100 posts.
    """
    error_msg = 'Posts cannot exceed {}'.format(arg_max)
    if arg > arg_max:
        raise argparse.ArgumentTypeError(error_msg)


# Parses the number of posts input from user. Default is 10.
def parse_arguments():
    """
    Parses the argument input from the user. Default is 10.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--posts', '-p', metavar='n', type=int, default=10, help='number of posts (max 100)')
    args = parser.parse_args()

    validate_input(args.posts, MAX_NUM_POSTS)

    return args.posts


def main():
    """
    If user input is valid, will create a scraper and fetch requests number of posts and print them to the user.
    """
    try:
        posts = parse_arguments()
        
        hnews_scraper = HackerNewsScraper(posts)
        hnews_scraper.scrape_stories()
        hnews_scraper.print_stories()

    except argparse.ArgumentTypeError as ex:
        log_error(ex)


if __name__ == '__main__':
    main()
