class Holding:
    """
    Specification of a fund with units held and target allocation.
    
    Attributes
    ----------
    fund : lisatools.Fund
        Details inherent to the fund.
    units : float, default 1.0
        Number of units held in the portfolio line (non-negative).
    target_fraction : float, default 0.0
        Fraction of the total portfolio that should be allocated towards the
        fund in question. Expected to be between 0 and 1.
    
    Example
    --------

    Constructing a Holding from a `Fund`, number of units and target allocation.
    
    >>> f = lisatools.Fund()
    >>> lisatools.Holding(f, 1.234, 0.5)
    """

    def __init__(self, fund, units = 1.0, target_fraction = 0.0):
        self.fund = fund
        self.units = units
        self.target_fraction = target_fraction
    
    def value(self):
        """The value of the holding based on the latest fund price available."""
        return self.units * self.fund.price


class Portfolio(list):
    """A collection of funds held in defined amounts with target allocations."""
    def total_value(self):
        return sum(holding.value() for holding in self)

    def add_holding(self, new_holding, scale_orig=True):
        if scale_orig:
            scale_factor = 1.0 - new_holding.target_fraction
            for holding in self:
                holding.target_fraction *= scale_factor
            self.append(new_holding)
        else:
            self.append(new_holding)
            for holding in self:
                holding.target_fraction /= 1.0 + new_holding.target_fraction
        
        # assert sum(holding.target_fraction for holding in self) == 1.0
    
    def add_fund(self, fund, *, value=None, units=1.0, target="auto", **kwargs):
        if value is None:
            if target == "auto":
                value_new = units * fund.price
                total_value = self.total_value() + value_new
                target = value_new / total_value            
            holding = Holding(fund, units, target)
            self.add_holding(holding, **kwargs)
        else:
            units = value / fund.price
            self.add_fund(fund, units=units, target=target, **kwargs)
    
    def add_target(self, fund, target):
        holding = Holding(fund, 0.0, target)
        self.add_holding(holding)
    
    def target_portfolio(self, update_prices=False):
        total_value = self.total_value()
        target = Portfolio()
        for orig in self:
            target_value = orig.target_fraction * total_value
            target_units = target_value / orig.fund.price
            holding = Holding(orig.fund, target_units, orig.target_fraction)
            target.append(holding)
        return target