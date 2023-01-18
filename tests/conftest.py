import datetime
import pathlib

import pytest

import lisatools


@pytest.fixture
def ftse_global():
    f = lisatools.Fund(
        "FTSE Global All Cap Index Fund",
        172.14,
        isin="GB00BD3RZ582",
        date=datetime.date(2022, 11, 21),
    )
    return f


@pytest.fixture
def gilts():
    f = lisatools.ETF(
        "U.K. Gilt UCITS ETF",
        18.58,
        ticker="VGOV",
        isin="IE00B42WWV65",
        date=datetime.date(2022, 11, 21),
    )
    return f


@pytest.fixture
def two_fund_6040(ftse_global, gilts):
    h1 = lisatools.Holding(ftse_global, 1.0, 0.6)
    h2 = lisatools.Holding(gilts, 5.0, 0.4)
    pf = lisatools.Portfolio([h1, h2])
    return pf


@pytest.fixture
def ftse_global_dict():
    d = {
        "ISIN": "GB00BD3RZ582",
        "description": "FTSE Global All Cap Index Fund",
        "price": 172.14,
        "date": datetime.date(2022, 11, 21),
    }
    return d


@pytest.fixture
def ftse_global_url():
    return "https://markets.ft.com/data/funds/tearsheet/historical?s=GB00BD3RZ582:GBP"


@pytest.fixture
def gilts_url():
    return "https://markets.ft.com/data/etfs/tearsheet/historical?s=VGOV:LSE:GBP"


@pytest.fixture
def two_fund_6040_target(two_fund_6040):
    tpf = two_fund_6040.target_portfolio()
    return tpf


@pytest.fixture
def example_portfolio_path():
    return pathlib.Path(".") / "tests" / "example_portfolio.json"


@pytest.fixture
def example_portfolio(example_portfolio_path):
    return lisatools.Portfolio.load(example_portfolio_path)


@pytest.fixture
def example_json(example_portfolio_path):
    with open(example_portfolio_path, "r") as handle:
        text = handle.read()
    return text
