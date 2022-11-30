from lisatools.fund import ETF

import datetime
import functools
import requests
from bs4 import BeautifulSoup


@functools.singledispatch
def history_url(fund):
    """
    Provide the URL to the Financial Times' historical pricing data for a
    given fund.
    """
    url = f"https://markets.ft.com/data/funds/tearsheet/historical?s={fund.isin}:GBP"
    return url


@history_url.register(ETF)
def _(fund):
    url = (
        f"https://markets.ft.com/data/etfs/tearsheet/historical?s={fund.ticker}:LSE:GBP"
    )
    return url


def retrieve_history(url):
    """
    Find an HTML table from the FT's historical price data page that can be
    further processed by beautifulsoup.
    """
    request = requests.get(url)
    soup = BeautifulSoup(request.content, "html.parser")
    price_history = soup.find(
        "table", {"class": "mod-tearsheet-historical-prices__results"}
    )
    return price_history


def parse_history(price_history):
    """
    Extract the latest price and date from an HTML table of fund pricing
    as provided by the FT.
    """
    # Parse table to get the latest price information (first row of data)
    body = price_history.find("tbody")
    body_rows = body.find_all("tr")
    latest_entry = body_rows[0].find_all("td")

    # Extract positions in the row of the date and (current or closing) price
    head = price_history.find("thead")
    col_names = list(head.stripped_strings)
    date_index = col_names.index("Date")
    price_index = col_names.index("Close")

    # Extract date and price. Note that the date is encoded twice in the HTML
    # (for display on different screen sizes).
    #
    # This implementation assumes that the current locale is identical to the
    # one the FT uses!
    date_str = (
        latest_entry[date_index]
        .find("span", {"class": "mod-ui-hide-medium-above"})
        .get_text()
    )
    date = datetime.datetime.strptime(date_str, "%a, %b %d, %Y").date()
    price = float(latest_entry[price_index].get_text())

    return price, date


def latest_price(fund):
    """
    Return a fund's latest price and matching date using the Financial Times'
    historical pricing data.
    """
    url = history_url(fund)
    price_history = retrieve_history(url)
    price, date = parse_history(price_history)

    return price, date
