#Email Finder:

##Overview:

A command line tool to scrape websites for email addresses.  It will follow all links within the same subdomain only.  For example, given example.com as the domain to search, it will not follow links to blog.example.com.

##Requirements

- BeautifulSoup4
- Selenium
- PhantomJS

##Set-Up
Install the Python libraries with:
```
pip install -r requirements.txt
```

Make sure PhantomJS is installed from [here](http://phantomjs.org/download.html)
or install with npm:
```
npm install phantomjs-prebuilt
```

##Usage
For most sites, simply run:
```python find_email_addresses.py example.com```

For websites that rely heavily on Javascript, there is a flag to load the pages in a headless browser.  This will get results on pages that otherwise may return nothing, however it is significantly slower.

```
> python find_email_addresses.py example.com -b
```
or
```
> python find_email_addresses.py example.com --browser
```

##Example Usage
```
# Here are some examples from udacity.com (subject to change)
> python find_email_addresses.py udacity.com
Found these email addresses:
jobs@udacity.com
mobile-support@udacity.com
engine@Twitter
career-support@udacity.com
uconnect-support@udacity.com
feedbackprogram@udacity.com
teach@udacity.com
payment-support@udacity.com
veterans-information@udacity.com
support@udacity.com
social@udacity.com
media@udacity.com
```

##To-Do
- move to Scrapy for parallelization
