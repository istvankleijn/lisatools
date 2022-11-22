import datetime
import lisatools
import pytest


@pytest.fixture
def ftse_global():
    d = "FTSE Global All Cap Index Fund"
    f = lisatools.Fund(d, 100.0, isin="GB00BD3RZ582")
    return f

@pytest.fixture
def long_gilts():
    d = "UK Long-term Gilts"
    f = lisatools.Fund(d, 50.0)
    return f

@pytest.fixture
def two_fund_6040(ftse_global, long_gilts):
    h1 = lisatools.Holding(ftse_global, 1.0, 0.6)
    h2 = lisatools.Holding(long_gilts, 2.0, 0.4)
    pf = lisatools.Portfolio([h1, h2])
    return pf

def test_fund_init(ftse_global):
    """Test the constructor of the `Fund` class"""
    f = ftse_global
    assert f.description == "FTSE Global All Cap Index Fund"
    assert f.price == 100.0
    assert f.isin is "GB00BD3RZ582"
    assert f.date == datetime.date.today()

def test_fund_repr(ftse_global):
    """Test the developer representation of the `Fund` class"""
    f = ftse_global
    assert repr(f) == f"Fund({f.description!r}, {f.price!r}, " \
                      f"date={f.date!r}, isin={f.isin!r})"

def test_fund_update_price(ftse_global):
    """Test the `update_price` method of the `Fund` class."""
    f = ftse_global
    f.update_price(170.14, date=datetime.date(2022, 11, 1))
    assert f.description == ftse_global.description
    assert f.price == 170.14
    assert f.isin is "GB00BD3RZ582"
    assert f.date == datetime.date(2022, 11, 1)

def test_holding_repr(ftse_global):
    """Test the developer representation of the `Holding` class"""
    h = lisatools.Holding(ftse_global)
    assert repr(h) == f"Holding({h.fund!r}, " \
                      f"{h.units!r}, {h.target_fraction!r})"

def test_holding_str(ftse_global):
    """Test the user string function for the `Holding` class"""
    holding = lisatools.Holding(ftse_global, 1.0, 0.6)
    expected = """
Description                       Units    Value Target ISIN         Date
------------------------------ -------- -------- ------ ------------ ----------
FTSE Global All Cap Index Fund   1.0000   100.00 0.6000 GB00BD3RZ582 2022-11-22
    """.strip()
    assert str(holding) == expected

@pytest.mark.parametrize(
    "p, u, res",
    [
        (2.0, 3.0, 6.0),
        (2.5, 1.0, 2.5)
    ]
)
def test_holding_value(p, u, res):
    """Test the 'value' method of the Holding class."""
    f = lisatools.Fund(price = p)
    h = lisatools.Holding(f, units = u)
    assert h.value() == pytest.approx(res)

def test_portfolio_repr(two_fund_6040):
    holdings_repr = [repr(holding) for holding in two_fund_6040]
    expected = "Portfolio(" + ", ".join(holdings_repr) + ")"
    assert repr(two_fund_6040) == expected

def test_portfolio_str(two_fund_6040):
    """Test the user string function for the `Portfolio` class"""
    expected = """
Description                       Units    Value Target ISIN         Date
------------------------------ -------- -------- ------ ------------ ----------
FTSE Global All Cap Index Fund   1.0000   100.00 0.6000 GB00BD3RZ582 2022-11-22
UK Long-term Gilts               2.0000   100.00 0.4000 None         2022-11-22
    """.strip()
    assert str(two_fund_6040) == expected

def test_portfolio_add_fund(ftse_global):
    pf = lisatools.Portfolio()
    pf.add_fund(ftse_global)
    assert pf[0].fund.description == "FTSE Global All Cap Index Fund"
    assert pf[0].units == pytest.approx(1.0)
    assert pf[0].target_fraction == pytest.approx(1.0)

def test_portfolio_integration(ftse_global):
    pf = lisatools.Portfolio()
    pf.add_fund(ftse_global)
    target_fund = lisatools.Fund("New target", 2.0)
    pf.add_target(target_fund, 0.4)
    assert pf[0].target_fraction == pytest.approx(0.6)
    assert pf[1].target_fraction == pytest.approx(0.4)

@pytest.mark.parametrize(
    "price2, frac1",
    [
        (2.0, 0.6),
        (2.0, 0.7),
        (0.5, 0.6)
    ]
)
def test_target_portfolio(price2, frac1, ftse_global):    
    frac2 = 1.0 - frac1
    f2 = lisatools.Fund("Fund 2", price2)
    pf = lisatools.Portfolio()
    pf.add_fund(ftse_global)
    pf.add_target(f2, frac2)
    tpf = pf.target_portfolio()
    tpf_total = tpf.total_value()
    assert tpf_total == pytest.approx(pf.total_value())
    assert tpf[0].value() == pytest.approx(frac1*tpf_total)
    assert tpf[1].value() == pytest.approx(frac2*tpf_total)
    assert tpf[0].target_fraction == pytest.approx(frac1)
    assert tpf[1].target_fraction == pytest.approx(frac2)

def test_trade_to_target(two_fund_6040, ftse_global, long_gilts):
    buy, sell = two_fund_6040.trade_to_target()
    assert buy[0].fund == ftse_global
    assert buy[0].units == pytest.approx(0.2)
    assert buy[0].target_fraction == pytest.approx(0.6)
    assert sell[0].fund == long_gilts
    assert sell[0].units == pytest.approx(0.4)
    assert sell[0].target_fraction == pytest.approx(0.4)