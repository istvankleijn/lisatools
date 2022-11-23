import datetime
import lisatools
import pytest


@pytest.fixture
def ftse_global():
    f = lisatools.Fund(
        "FTSE Global All Cap Index Fund",
        172.14,
        isin="GB00BD3RZ582",
        date=datetime.date(2022, 11, 21)
    )
    return f

@pytest.fixture
def gilts():
    f = lisatools.Fund(
        "U.K. Gilt UCITS ETF (VGOV)",
        18.58,
        isin="IE00B42WWV65",
        date=datetime.date(2022, 11, 21)
    )
    return f

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
    f = ftse_global
    assert f.description == "FTSE Global All Cap Index Fund"
    assert f.price == 172.14
    assert f.isin is "GB00BD3RZ582"
    assert f.date == datetime.date(2022, 11, 21)

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
FTSE Global All Cap Index Fund   1.0000   172.14 0.6000 GB00BD3RZ582 2022-11-21
    """.strip()
    assert str(holding) == expected

@pytest.mark.parametrize(
    "p, u, res",
    [
        (2.0, 3.0, 6.0),
        (2.5, 1.0, 2.5),
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
FTSE Global All Cap Index Fund   1.0000   172.14 0.6000 GB00BD3RZ582 2022-11-21
U.K. Gilt UCITS ETF (VGOV)       5.0000    92.90 0.4000 IE00B42WWV65 2022-11-21
    """.strip()
    assert str(two_fund_6040) == expected

@pytest.mark.parametrize(
    "scale_new, res1, res2",
    [
        (True, 1.0/1.5, 0.5/1.5),
        (False, 0.5, 0.5),
    ]
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
    ]
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
        (True, 1.0/1.4, 0.4/1.4),
        (False, 0.6, 0.4),
    ]
)
def test_portfolio_add_target(ftse_global, gilts, scale_new, res1, res2):
    pf = lisatools.Portfolio()
    pf.add_fund(ftse_global, scale_new=False)
    pf.add_target(gilts, 0.4, scale_new=scale_new)
    assert pf[0].target_fraction == pytest.approx(res1)
    assert pf[1].target_fraction == pytest.approx(res2)

def test_target_portfolio(two_fund_6040):
    frac1 = two_fund_6040[0].target_fraction
    frac2 = two_fund_6040[1].target_fraction
    target_pf = two_fund_6040.target_portfolio()
    tpf_total = target_pf.total_value()
    assert tpf_total == pytest.approx(two_fund_6040.total_value())
    assert target_pf[0].value() == pytest.approx(frac1*tpf_total)
    assert target_pf[1].value() == pytest.approx(frac2*tpf_total)
    assert target_pf[0].target_fraction == pytest.approx(frac1)
    assert target_pf[1].target_fraction == pytest.approx(frac2)

@pytest.mark.parametrize("use_target", [True, False])
def test_trade_to_target(
        two_fund_6040,
        two_fund_6040_target,
        ftse_global,
        gilts,
        use_target):
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