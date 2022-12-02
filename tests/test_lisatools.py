import bs4
from copy import deepcopy
import datetime
import lisatools
import pytest


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
def ftse_global_url():
    return "https://markets.ft.com/data/funds/tearsheet/historical?s=GB00BD3RZ582:GBP"


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
def gilts_url():
    return "https://markets.ft.com/data/etfs/tearsheet/historical?s=VGOV:LSE:GBP"


@pytest.fixture
def two_fund_6040(ftse_global, gilts):
    h1 = lisatools.Holding(ftse_global, 1.0, 0.6)
    h2 = lisatools.Holding(gilts, 5.0, 0.4)
    pf = lisatools.Portfolio([h1, h2])
    return pf


@pytest.fixture
def two_fund_6040_target(two_fund_6040):
    tpf = two_fund_6040.target_portfolio()
    return tpf


def test_fund_init(ftse_global):
    """Test the constructor of the `Fund` class"""
    f = lisatools.Fund(
        "FTSE Global All Cap Index Fund",
        172.14,
        isin="GB00BD3RZ582",
        date=datetime.date(2022, 11, 21),
    )
    assert f.description == "FTSE Global All Cap Index Fund"
    assert f.price == 172.14
    assert f.isin == "GB00BD3RZ582"
    assert f.date == datetime.date(2022, 11, 21)


def test_fund_repr(ftse_global):
    """Test the developer representation of the `Fund` class"""
    f = ftse_global
    assert (
        repr(f) == f"Fund({f.description!r}, {f.price!r}, "
        f"date={f.date!r}, isin={f.isin!r})"
    )


def test_fund_eq(ftse_global):
    f = lisatools.Fund(
        "FTSE Global All Cap Index Fund",
        172.14,
        isin="GB00BD3RZ582",
        date=datetime.date(2022, 11, 21),
    )
    assert f == ftse_global


def test_fund_update_price(ftse_global):
    """Test the `update_price` method of the `Fund` class."""
    f = ftse_global
    f.update_price(170.14, date=datetime.date(2022, 11, 1))
    assert f.description == ftse_global.description
    assert f.price == 170.14
    assert f.isin == "GB00BD3RZ582"
    assert f.date == datetime.date(2022, 11, 1)


def test_etf_init(gilts):
    """Test the constructor of the `ETF` class"""
    f = gilts
    assert f.name == "U.K. Gilt UCITS ETF"
    assert f.description == "VGOV: U.K. Gilt UCITS ETF"
    assert f.price == 18.58
    assert f.ticker == "VGOV"
    assert f.isin == "IE00B42WWV65"
    assert f.date == datetime.date(2022, 11, 21)


def test_etf_repr(gilts):
    """Test the developer representation of the `ETF` class"""
    f = gilts
    expected = (
        f"ETF({f.name!r}, {f.price!r}, "
        f"date={f.date!r}, isin={f.isin!r}, ticker={f.ticker!r})"
    )
    assert repr(f) == expected


def test_holding_repr(ftse_global):
    """Test the developer representation of the `Holding` class"""
    h = lisatools.Holding(ftse_global)
    assert repr(h) == f"Holding({h.fund!r}, " f"{h.units!r}, {h.target_fraction!r})"


def test_holding_str(ftse_global):
    """Test the user string function for the `Holding` class"""
    holding = lisatools.Holding(ftse_global, 1.0, 0.6)
    expected = """
Description                       Units    Value Target ISIN         Date
------------------------------ -------- -------- ------ ------------ ----------
FTSE Global All Cap Index Fund   1.0000   172.14 0.6000 GB00BD3RZ582 2022-11-21
    """.strip()
    assert str(holding) == expected


def test_holding_eq(ftse_global):
    h1 = lisatools.Holding(ftse_global, 1.0, 0.6)
    h2 = lisatools.Holding(ftse_global, target_fraction=0.6)
    assert h1 == h2


@pytest.mark.parametrize(
    "p, u, res",
    [
        (2.0, 3.0, 6.0),
        (2.5, 1.0, 2.5),
    ],
)
def test_holding_value(p, u, res):
    """Test the 'value' method of the Holding class."""
    f = lisatools.Fund(price=p)
    h = lisatools.Holding(f, units=u)
    assert h.value() == pytest.approx(res)


def test_portfolio_init(ftse_global, gilts):
    pf = lisatools.Portfolio()
    assert pf.holdings == []
    h1 = lisatools.Holding(ftse_global, 1.0, 0.6)
    h2 = lisatools.Holding(gilts, 5.0, 0.4)
    pf = lisatools.Portfolio([h1, h2])
    assert pf.holdings == [h1, h2]


def test_portfolio_repr(two_fund_6040):
    holdings_repr = [repr(holding) for holding in two_fund_6040.holdings]
    expected = "Portfolio([" + ", ".join(holdings_repr) + "])"
    assert repr(two_fund_6040) == expected


def test_portfolio_str(two_fund_6040):
    """Test the user string function for the `Portfolio` class"""
    expected = """
Description                       Units    Value Target ISIN         Date
------------------------------ -------- -------- ------ ------------ ----------
FTSE Global All Cap Index Fund   1.0000   172.14 0.6000 GB00BD3RZ582 2022-11-21
VGOV: U.K. Gilt UCITS ETF        5.0000    92.90 0.4000 IE00B42WWV65 2022-11-21
    """.strip()
    assert str(two_fund_6040) == expected


def test_portfolio_iter(two_fund_6040, ftse_global, gilts):
    h1, h2 = two_fund_6040
    assert h1 == lisatools.Holding(ftse_global, 1.0, 0.6)
    assert h2 == lisatools.Holding(gilts, 5.0, 0.4)


def test_portfolio_len(two_fund_6040):
    assert len(two_fund_6040) == 2


def test_portfolio_getitem(two_fund_6040, ftse_global, gilts):
    h1 = two_fund_6040[0]
    h2 = two_fund_6040[1]
    assert type(h1) == lisatools.Holding
    assert h1.fund == ftse_global
    assert h2.fund == gilts


def test_portfolio_eq(ftse_global, gilts, two_fund_6040):
    h1 = lisatools.Holding(ftse_global, 1.0, 0.6)
    h2 = lisatools.Holding(gilts, 5.0, 0.4)
    pf = lisatools.Portfolio([h1, h2])
    assert pf == two_fund_6040


@pytest.mark.parametrize(
    "units, target_fractions",
    [
        (None, None),
        ([1.0, 5.0], None),
        (None, [0.6, 0.4]),
        ([1.0, 5.0], [0.6, 0.4]),
    ],
)
def test_portfolio_from_funds(ftse_global, gilts, units, target_fractions):
    pf = lisatools.Portfolio.from_funds(
        [ftse_global, gilts], units=units, target_fractions=target_fractions
    )
    if units is None:
        units = [1.0, 1.0]
    if target_fractions is None:
        target_fractions = [0.5, 0.5]
    h1 = lisatools.Holding(ftse_global, units[0], target_fractions[0])
    h2 = lisatools.Holding(gilts, units[1], target_fractions[1])
    expected = lisatools.Portfolio([h1, h2])
    assert pf == expected
    with pytest.raises(ValueError):
        lisatools.Portfolio.from_funds([ftse_global, gilts], units=[])
    with pytest.raises(ValueError):
        lisatools.Portfolio.from_funds([ftse_global, gilts], target_fractions=[])


@pytest.mark.parametrize(
    "scale_new, res1, res2",
    [
        (True, 1.0 / 1.5, 0.5 / 1.5),
        (False, 0.5, 0.5),
    ],
)
def test_portfolio_add_holding(ftse_global, gilts, scale_new, res1, res2):
    h1 = lisatools.Holding(ftse_global, 1.0, 1.0)
    h2 = lisatools.Holding(gilts, 1.0, 0.5)
    pf = lisatools.Portfolio([h1])
    pf.add_holding(h2, scale_new=scale_new)
    assert pf[0].fund == ftse_global
    assert pf[0].units == 1.0
    assert pf[0].target_fraction == pytest.approx(res1)
    assert pf[1].fund == gilts
    assert pf[1].units == 1.0
    assert pf[1].target_fraction == pytest.approx(res2)


@pytest.mark.parametrize(
    "value, target",
    [
        (None, None),
        (None, 1.0),
        (172.14, None),
        (172.14, 1.0),
    ],
)
def test_portfolio_add_fund(ftse_global, value, target):
    pf = lisatools.Portfolio()
    # Adding a holding to an empty portfolio means that the new allocation must
    # not be scaled, because the empty portfolio does not comply with
    # sum(allocs) == 1.0
    pf.add_fund(ftse_global, value=value, target=target, scale_new=False)
    assert pf[0].fund.description == "FTSE Global All Cap Index Fund"
    assert pf[0].units == pytest.approx(1.0)
    assert pf[0].target_fraction == pytest.approx(1.0)


@pytest.mark.parametrize(
    "scale_new, res1, res2",
    [
        (True, 1.0 / 1.4, 0.4 / 1.4),
        (False, 0.6, 0.4),
    ],
)
def test_portfolio_add_target(ftse_global, gilts, scale_new, res1, res2):
    pf = lisatools.Portfolio()
    pf.add_fund(ftse_global, scale_new=False)
    pf.add_target(gilts, 0.4, scale_new=scale_new)
    assert pf[0].target_fraction == pytest.approx(res1)
    assert pf[1].target_fraction == pytest.approx(res2)


def test_portfolio_update_prices(two_fund_6040):
    pf = deepcopy(two_fund_6040)
    pf.update_prices()
    assert pf[0].fund.description == two_fund_6040[0].fund.description
    assert pf[1].fund.description == two_fund_6040[1].fund.description
    assert pf[0].units == two_fund_6040[0].units
    assert pf[1].units == two_fund_6040[1].units
    assert pf[0].target_fraction == two_fund_6040[0].target_fraction
    assert pf[1].target_fraction == two_fund_6040[1].target_fraction
    date1 = pf[0].fund.date
    delta1 = datetime.date.today() - date1
    date2 = pf[1].fund.date
    delta2 = datetime.date.today() - date2
    assert 0 <= delta1.days < 7
    assert 0 <= delta2.days < 7


def test_target_portfolio(two_fund_6040):
    frac1 = two_fund_6040[0].target_fraction
    frac2 = two_fund_6040[1].target_fraction
    target_pf = two_fund_6040.target_portfolio()
    tpf_total = target_pf.total_value()
    assert tpf_total == pytest.approx(two_fund_6040.total_value())
    assert target_pf[0].value() == pytest.approx(frac1 * tpf_total)
    assert target_pf[1].value() == pytest.approx(frac2 * tpf_total)
    assert target_pf[0].target_fraction == pytest.approx(frac1)
    assert target_pf[1].target_fraction == pytest.approx(frac2)


@pytest.mark.parametrize("use_target", [True, False])
def test_trade_to_target(
    two_fund_6040, two_fund_6040_target, ftse_global, gilts, use_target
):
    if use_target:
        buy, sell = two_fund_6040.trade_to_target(two_fund_6040_target)
    else:
        buy, sell = two_fund_6040.trade_to_target()

    assert type(buy) == lisatools.Portfolio
    assert type(sell) == lisatools.Portfolio
    assert buy[0].fund == gilts
    assert buy[0].units == pytest.approx(0.7059203444564046)
    assert buy[0].target_fraction == pytest.approx(0.4)
    assert sell[0].fund == ftse_global
    assert sell[0].units == pytest.approx(0.0761937957476474)
    assert sell[0].target_fraction == pytest.approx(0.6)


def test_history_url_Fund(ftse_global, ftse_global_url):
    url = lisatools.scraping.history_url(ftse_global)
    assert url == ftse_global_url


def test_history_url_ETF(gilts, gilts_url):
    url = lisatools.scraping.history_url(gilts)
    assert url == gilts_url


def test_retrieve_history(ftse_global_url):
    price_history = lisatools.scraping.retrieve_history(ftse_global_url)
    assert type(price_history) == bs4.element.Tag
    assert price_history.name == "table"


def test_latest_price(ftse_global):
    price, date = lisatools.scraping.latest_price(ftse_global)
    assert type(price) == float
    assert 1.0 <= price <= 1.0e5
    assert type(date) == datetime.date
    delta = datetime.date.today() - date
    assert 0 <= delta.days < 7
