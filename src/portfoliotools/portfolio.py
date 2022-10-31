class Holding:
    """A fund held in a certain number of units together with the target allocation fraction"""
    def __init__(self, fund, units = 1.0, target_fraction = 0.0):
        self.fund = fund
        self.units = units
        self.target_fraction = target_fraction
    
    def value(self):
        return self.units * self.fund.price


class Portfolio(list):
    """A collection of funds held in defined proportions"""
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
        
        assert sum(holding.target_fraction for holding in self) == 1.0
    
    def add_fund(self, fund, *, value=None, units=1.0, target="auto"):
        if value is None:
            if target == "auto":
                value_new = units * fund.price
                total_value = self.total_value() + value_new
                target = value_new / total_value            
            holding = Holding(fund, units, target)
            self.add_holding(fund, holding)
        else:
            units = value / fund.price
            self.add_fund(fund, units=units, target=target)
    
    def add_target(self, fund, target):
        holding = Holding(fund, 0.0, target)
        self.add_holding(holding)