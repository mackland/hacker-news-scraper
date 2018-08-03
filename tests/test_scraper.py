import sys
sys.path.append('../scraper')
from HackerNewsScraper import *
from bs4 import BeautifulSoup

with open('test_scraper.html', encoding='utf-8') as f:
    html_doc = f.read()
    html = BeautifulSoup(html_doc, 'html.parser')

test_scraper = HackerNewsScraper(2)
test_scraper.parse_stories(html)
stories = test_scraper.get_stories()

def test_string_length():
    assert len(stories[0]['title']) <= 256
    assert len(stories[1]['title']) <= 256
    assert len(stories[0]['author']) <= 256
    assert len(stories[1]['author']) <= 256

def test_empty_string():
    assert len(stories[0]['title']) > 0
    assert len(stories[1]['title']) > 0
    assert len(stories[0]['author']) > 0
    assert len(stories[1]['author']) > 0

def test_URL():
    assert stories[0]['uri'] != 'Valid URI not found'
    assert stories[1]['uri'] == 'Valid URI not found'

def test_integers():
    assert isinstance(stories[0]['points'], int)
    assert isinstance(stories[1]['points'], int)
    assert isinstance(stories[0]['comments'], int)
    assert isinstance(stories[1]['comments'], int)
    assert isinstance(stories[0]['rank'], int)
    assert isinstance(stories[1]['rank'], int)

def test_numbers_range():
    assert stories[0]['points'] >= 0
    assert stories[1]['points'] >= 0
    assert stories[0]['comments'] >= 0
    assert stories[1]['comments'] >= 0
    assert stories[0]['rank'] >= 1
    assert stories[1]['rank'] >= 1
