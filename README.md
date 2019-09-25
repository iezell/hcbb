# healthcarebluebook

Web Scrapping Project for healthcarebluebook
Current Status: Work in Progress

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install healthcarebluebook.

```bash
pip3 install scrapy
pip3 install selenium
pip3 install bs4
#(Maybe others?)
#Needs Google CHrome 77 with latest selenium
```

## Usage

Currently the scraper goes through /ui/consumerfront with proper search term and zipcode, passes the prompted window,
pulls the variations of MRIs, goes through the procedure page, and has the data ready to be parsed into a CSV.

Known Issues:
  - Does not handle errors at all, so the application will bork if it can't find an element that hasn't loaded
  - Currently tries to go back to the search window of different MRIs but does not load elements of other
    forms of MRIs to continue crawling
  - Not performance tested. Performs very slow and does not utilize multiple spiders
  - No logging
  - Not portable i.e. no virtualenv or docker container
  - Poorly written and needs cleaned up.
