from lisatools import fund, portfolio


def test_holding():
    """Test methods of Holding class"""
    f = fund.Fund(price = 2.0)
    h = portfolio.Holding(f, units = 3.0)
    assert h.value() == 6.0
