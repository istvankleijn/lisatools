import datetime
import lisatools


def test_fund():
    """Test the methods of Fund class."""
    f = lisatools.Fund("FTSE Global All Cap Index Fund", 123.45)
    assert f.description == "FTSE Global All Cap Index Fund"
    assert f.price == 123.45
    assert f.isin is None
    assert f.date == datetime.date.today()
    f.update_price(170.14, date=datetime.date(2022, 11, 1))
    assert f.description == "FTSE Global All Cap Index Fund"
    assert f.price == 170.14
    assert f.isin is None
    assert f.date == datetime.date(2022, 11, 1)
    
def test_holding():
    """Test the methods of the Holding class."""
    f = lisatools.Fund(price = 2.0)
    h = lisatools.Holding(f, units = 3.0)
    assert h.value() == 6.0