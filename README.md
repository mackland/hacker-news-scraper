# Hacker News Scraper

A simple command line application that outputs the top articles from [Hacker News](https://news.ycombinator.com/news) requested by the user in JSON format.

## Example output
Running `python HackerNewsScraper.py --posts 1` returned the following:
```
[
  {
    'title': 'JPL Open-Source Rover Project Based on the Rovers on Mars',
    'uri': 'https://github.com/nasa-jpl/open-source-rover',
    'author': 'ghosthamlet',
    'comments': 5,
    'points': 46,
    'rank': 1
  }
]
```

## How to run
Python 3 is necessary to run this program. While installing Python, make sure to also install pip during the installation. pip is a package manager needed to install the necessary modules. If you have Python but not pip run:

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

To run the program, make sure you are in the scraper directory and on the command line type:
```
python HackerNewsScraper.py --posts n
```

where `n` is the number of posts you wish to fetch.

## Tests
Make sure you are in the tests directory and run:
```
pytest test_scraper.py
```
this will show the data validation passing the 5 tests on a sample html file that contains 1 article from Hacker News and one with incorrect data.

Tests performed are:
```Title and author are non empty strings not longer than 256 characters.```
```uri is a valid URI```
```Points, comments and rank are integers >= 0.```

## Libraries used and why

### BeautifulSoup
I have used BeautifulSoup before to handle HTML/XML processing and building a web scraper. Since we only need to visit a specific webpage, it is enough to complete the task. Page numbers can easily be changed manually. The reason I used it for my previous project is that it came highly recommended from the community and I found it very easy to use for getting the required data from the webpage. Documentation is also clear and it also helps that it is so frequently used in the Python community when looking for help.

### Requests
Similar to BeautifulSoup, I have used Requests before in my previous project to perform HTTP requests. It was very easy to use and well documented which is the main reason I continued to use it.

### PyTest
I had to look for this module for this project as I have not done much unit testing in Python. The reason I chose it was that it was highly recommended and easy enough to set up a few test cases. I did this writing a small HTML file based on Hacker News layout with one correct article and one incorrect that broke against every one of the desired rules. I then tested the two against the desired rules.

### Validators
This I also had to look up for this project. From what I found online there are some better validators but this was extremely easy to use and got the job done.
