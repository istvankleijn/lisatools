from lisatools import scraping


_str_prefix = """
Description                       Units    Value Target ISIN         Date
------------------------------ -------- -------- ------ ------------ ----------
""".strip()

class Holding:
    """
    Specification of a fund with units held and target allocation.
    
    Parameters
    ----------
    fund : lisatools.Fund
        Details inherent to the fund.
    units : float, default 1.0
        Number of units held in the portfolio line (non-negative).
    target_fraction : float, default 0.0
        Fraction of the total portfolio that should be allocated towards the
        fund in question. Expected to be between 0 and 1.
    
    Example
    -------

    Constructing a Holding from a `Fund`, number of units and target allocation.
    
    >>> f = lisatools.Fund()
    >>> lisatools.Holding(f, 1.234, 0.5)
    """
    def __init__(self, fund, units = 1.0, target_fraction = 0.0):
        self.fund = fund
        self.units = units
        self.target_fraction = target_fraction
    
    def __repr__(self):
        return (
            f"Holding({self.fund!r}, {self.units!r}, {self.target_fraction!r})"
        )
    
    def __str__(self):
        line = self._str_line()
        return _str_prefix + "\n" + line
    
    def value(self):
        """
        Return the value of the holding based on the latest fund price
        available.
        """
        return self.units * self.fund.price
    
    def _str_line(self):
        line = " ".join([
            f"{self.fund.description:<30}",
            f"{self.units:>8.4f}",
            f"{self.value():>8.2f}",
            f"{self.target_fraction:>6.4f}",
            f"{self.fund.isin:<12}",
            f"{self.fund.date:%Y-%m-%d}"
        ])
        return line
    

class Portfolio(list):
    """
    A collection of funds held in defined amounts with target allocations.

    Example
    -------
    Constructing a Portfolio from two Holdings.

    >>> h1 = lisatools.Holding(lisatools.Fund("Fund 1", 1.0), 1.0, 0.6)
    >>> h2 = lisatools.Holding(lisatools.Fund("Fund 2", 2.0), 2.0, 0.4)
    >>> lisatools.Portfolio([h1, h2])
    """
    def __repr__(self):
        holdings_repr = ", ".join(f"{holding!r}" for holding in self)
        return "Portfolio(" + holdings_repr + ")"
    
    def __str__(self):
        lines = "\n".join(holding._str_line() for holding in self)
        return _str_prefix + "\n" + lines

    def total_value(self):
        """
        Return the total value of all the holdings based on the latest fund
        prices available.
        """
        return sum(holding.value() for holding in self)

    def add_holding(self, new_holding, scale_new=True):
        """
        Add a holding to the portfolio while ensuring that the sum of all target
        allocations is equal to 1.0 after the addition.

        There are two strategies implemented that satisfy the requirement that
        the sum of all allocations equals 1.0:
        1. All of the target allocations, both of the old portfolio and of the
        newly added holding, are scaled.
        2. The old allocations are scaled before adding the new holding to the
        portfolio. 

        Parameters
        ----------
        new_holding : lisatools.Holding
            The holding that is to be added to the portfolio.
        scale_orig : bool, default True
            Controls whether the holding's `target_fraction` is scaled before
            adding it to the portfolio or not. If truthy, strategy 1 (see above)
            is employed; otherwise strategy 2 is chosen.
        
        Examples
        --------
        Strategy 1 (scale new and old allocations):

        >>> h1 = lisatools.Holding(lisatools.Fund("Fund 1"), 1.0, 1.0)
        >>> h2 = lisatools.Holding(lisatools.Fund("Fund 2"), 1.0, 0.5)
        >>> pf1 = lisatools.Portfolio([h1])
        >>> pf1.add_holding(h2, scale_new=True)
        >>> print(pf1)
        Description                       Units    Value Target ISIN         Date
        ------------------------------ -------- -------- ------ ------------ ----------
        Fund 1                           1.0000     1.00 0.6667 None         2022-11-23
        Fund 2                           1.0000     1.00 0.3333 None         2022-11-23
        
        Strategy 2 (scale only the old allocations):

        >>> h3 = lisatools.Holding(lisatools.Fund("Fund 3"), 1.0, 1.0)
        >>> h4 = lisatools.Holding(lisatools.Fund("Fund 4"), 1.0, 0.5)
        >>> pf2 = lisatools.Portfolio([h3])
        >>> pf2.add_holding(h4, scale_new=False)
        >>> print(pf2)
        Description                       Units    Value Target ISIN         Date
        ------------------------------ -------- -------- ------ ------------ ----------
        Fund 3                           1.0000     1.00 0.5000 None         2022-11-23
        Fund 4                           1.0000     1.00 0.5000 None         2022-11-23
        """
        if scale_new:
            self.append(new_holding)
            for holding in self:
                holding.target_fraction /= 1.0 + new_holding.target_fraction
        else:
            scale_factor = 1.0 - new_holding.target_fraction
            for holding in self:
                holding.target_fraction *= scale_factor
            self.append(new_holding)
    
    def add_fund(self, fund, *, value=None, units=1.0, target=None, **kwargs):
        """
        Construct a holding based on the specified fund and add it to
        the portfolio.

        By default, a specified number of units is added and it is assumed
        that the fund is added in exactly the target allocation. Alternatively,
        the target allocation can be specified. Insteady of specifying the
        number of units, the fund can be added by a specified monetary value 
        using the `value` keyword.

        Parameters
        ----------
        fund : lisatools.Fund
            The fund from which a holding is to be constructed and added to
            the portfolio.
        value : float or None, default None
            If specified, the fund is added by the monetary value specified by
            the `value` parameter.
        units : float, default 1.0
            If `value` is left unspecified, the fund is added by the number of
            units specified by the `units` parameter.
        target : float or None, default None
            If specified, the `target_fraction` of the new holding is set to
            this value. By default, it is calculated as the ratio of the value
            of the new holding and the total value of the portfolio after adding
            the fund.
        **kwargs
            Optional keyword arguments passed to the `add_holding` method.
        
        See also
        --------
        add_holding
        """
        if value is None:
            if target == None:
                value_new = units * fund.price
                total_value = self.total_value() + value_new
                target = value_new / total_value            
            holding = Holding(fund, units, target)
            self.add_holding(holding, **kwargs)
        else:
            units = value / fund.price
            self.add_fund(fund, units=units, target=target, **kwargs)
    
    def add_target(self, fund, target, **kwargs):
        """
        Construct a zero-unit holding from the specified fund and target
        allocation and add it to the portfolio.

        Parameters
        ----------
        fund : lisatools.Fund
            The fund from which a holding is to be constructed and added to
            the portfolio.
        target : float
            The `target_fraction` to which the new holding is set.
        **kwargs
            Optional keyword arguments passed to the `add_holding` method.
        
        See also
        --------
        add_holding
        """
        holding = Holding(fund, 0.0, target)
        self.add_holding(holding, **kwargs)
    
    def target_portfolio(self):
        """
        Based on the allocation fractions specified in the current portfolio,
        construct a target portfolio with the same total value where these
        fractions are exactly met.

        Returns
        -------
        lisatools.Portfolio
            The constructed target portfolio.      
        """
        total_value = self.total_value()
        target = Portfolio()
        for orig in self:
            target_value = orig.target_fraction * total_value
            target_units = target_value / orig.fund.price
            holding = Holding(orig.fund, target_units, orig.target_fraction)
            target.append(holding)
        return target
    
    def trade_to_target(self, target_portfolio=None):
        """
        Return the required buy and sell instructions to reach the target
        portfolio.

        Arguments
        ---------
        target_portfolio : lisatools.Portfolio or None, default None
            Target to rebalance the portfolio into. If unspecified, calculate
            this based on the target allocations defined by `target_fraction`s.

        Returns
        -------
        buy : lisatools.Portfolio
            Funds to purchase to reach the target. Positive `units` values
            indicate the number of units that must be bought.
        sell : lisatools.Portfolio
            Funds to sell to reach the target. Positive `units` values indicate
            the number of units that must be sold.
        """
        if target_portfolio is None:
            target_portfolio = self.target_portfolio()

        buy = Portfolio()
        sell = Portfolio()
        for orig, target in zip(self, target_portfolio):
            diff = target.units - orig.units
            if diff > 0:
                trade = Holding(orig.fund, diff, orig.target_fraction)
                buy.append(trade)
            elif diff < 0:
                trade = Holding(orig.fund, -diff, orig.target_fraction)
                sell.append(trade)
        
        return buy, sell
    
    def update_prices(self):
        """
        Silently update the fund prices and dates for all the funds held in
        the portfolio.

        This scrapes the Financial Times web site for historical pricing data
        using the `lisatools.scraping` module. It may take a couple of seconds
        to run.
        """
        for holding in self:
            price, date = scraping.latest_price(holding.fund)
            holding.fund.update_price(price, date=date)