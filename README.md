# Hacker News Scraper

A simple command line application that outputs the top articles from [Hacker News](https://news.ycombinator.com/news) requested by the user in JSON format.

## How to run
Python 3 is necessary to run this program. While installing Python, make sure to also install pip during the installation.

pip is a package manager needed to install the necessary modules. If you have Python but not pip run:

```
sudo easy_install pip
```

After that, modules can be installed with:

```
pip install <module>
```

Modules that need to be installed
- `BeautifulSoup`
- `requests`
- `validators`
- `pytest`

From the standard library the app will use `argparse`, `json`, `math`. These are installed with Python and do not need to be added.

To run the program, make sure you are in the scraper/ directory and on the command line type:
```
python HackerNewsScraper.py --posts n
```

where n is the number of posts you wish to fetch.

## Tests
Make sure you are in the tests/ directory and run:
```
pytests test_scraper.py
```
this will show the data validation passing the tests on a sample html file that contains 1 article from Hacker News and one with incorrect data.

## Libraries used and why

### BeautifulSoup


### Requests


### PyTest


### Validators
