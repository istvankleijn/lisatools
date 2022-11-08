import datetime
import lisatools
import pytest


@pytest.fixture
def ftse_global():
    d = "FTSE Global All Cap Index Fund"
    f = lisatools.Fund(d, 123.45)
    return f

def test_fund_init(ftse_global):
    """Test the constructor of the `Fund` class"""
    f = ftse_global
    assert f.description == "FTSE Global All Cap Index Fund"
    assert f.price == 123.45
    assert f.isin is None
    assert f.date == datetime.date.today()

def test_fund_update_price(ftse_global):
    """Test the `update_price` method of the `Fund` class."""
    f = ftse_global
    f.update_price(170.14, date=datetime.date(2022, 11, 1))
    assert f.description == ftse_global.description
    assert f.price == 170.14
    assert f.isin is None
    assert f.date == datetime.date(2022, 11, 1)

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