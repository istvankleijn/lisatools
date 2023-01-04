import datetime


class Fund:
    """
    Details of a fund, including its current market price.

    Attributes
    ----------
    description : str
        Description of the fund, for example the name given by its provider.
    price : float, default 1.0
        Latest market price available for the fund.
    isin : str, default "None"
        If a real fund, the International Securities Identification Number
        (ISIN) of the fund should be specified.
        The ISIN is a unique 12-character alphanumerical identifier.
    date : datetime.date
        Date at which the `price` was last updated. If not specified, will be
        initialized to the current one (at runtime).

    Examples
    --------

    Constructing a Fund from a description and current price.

    >>> f = lisatools.Fund("FTSE Global All Cap Index Fund", 170.14)

    Constructing a Fund with all optional details.

    >>> f = lisatools.Fund("FTSE Global All Cap Index Fund", 170.14,
    ...                    isin="GB00BD3RZ582",
    ...                    date=datetime.date(2022, 11, 1))
    """

    def __init__(
        self,
        description="Default fund",
        price=1.0,
        *,
        isin="None",  # UNSPECIFIED9 is a valid ISIN
        date=None,
    ):
        self.description = description
        self.isin = isin
        self.update_price(price, date=date)

    def __repr__(self):
        return (
            f"Fund({self.description!r}, {self.price!r}, "
            f"date={self.date!r}, isin={self.isin!r})"
        )

    def __eq__(self, other):
        return (
            self.description == other.description
            and self.price == other.price
            and self.date == other.date
            and self.isin == other.isin
        )

    def update_price(self, price, *, date=None):
        """
        Set the price of the fund to a given value and optionally specify the
        date at which this price is correct.

        Parameters
        ----------
        price : float
            The new price of one unit of the fund.
        date : datetime.date, str, or None, default None
            The date when the fund had the given price. Can be provided as an
            ISO-formatted date string. If left unspecified, the date is set to the
            current one (at runtime).
        """
        self.price = price
        if isinstance(date, datetime.date):
            self.date = date
        elif isinstance(date, str):
            self.date = datetime.date.fromisoformat(date)
        elif date is None:
            self.date = datetime.date.today()
        else:
            raise TypeError(
                "date must be a `datetime.date` or an ISO-formatted date string"
            )

    def as_dict(self):
        """
        Encode the fund as a dictionary.

        The ISIN is encoded with dictionary key 'ISIN'; the other keys are equal to the
        names of the class attributes.
        """
        return {
            "ISIN": self.isin,
            "description": self.description,
            "price": self.price,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, d):
        """
        Construct a lisatools.Fund from a dictionary, respecting the class
        constructor defaults.

        The `isin` class attribute is set from the 'ISIN' dictionary key.

        Parameters
        ----------
        d : dict
            The dictionary from which the Fund is constructed.
        """
        return cls(
            d["description"],
            d["price"],
            isin=d.get("ISIN", "None"),
            date=d.get("date", None),
        )


class ETF(Fund):
    """
    Details of an exchange-traded fund, including its current market price.

    Attributes
    ----------
    description
        Description of the ETF. By default, this will be equal to the ticker
        symbol and the `name` attribute separated by a colon.
    price : float
        Latest market price available for the fund.
    name : str
        Name of the ETF, for example as given by its provider.
    isin : str
        If a real fund, the International Securities Identification Number
        (ISIN) of the fund should be specified.
        The ISIN is a unique 12-character alphanumerical identifier.
    date : datetime.date
        Date at which the `price` was last updated. If not specified, will be
        initialized to the current one (at runtime).

    Parameters
    ----------
    name : str
    price : float, default 1.0
    ticker : str or None, default None
    isin : str, default "None"
    date : datetime.date or None, default None

    Examples
    --------

    Constructing an ETF from a name and current price.

    >>> f = lisatools.ETF("U.K. Gilt UCITS ETF", 18.58)

    Constructing a Fund with all optional details.

    >>> f = lisatools.ETF(
    ...     "U.K. Gilt UCITS ETF",
    ...     18.58,
    ...     ticker="VGOV",
    ...     isin="IE00B42WWV65",
    ...     date=datetime.date(2022, 11, 21))
    """

    def __init__(self, name, price=1.0, *, ticker=None, isin="None", date=None):
        self.name = name
        if ticker is None:
            self.description = name
        else:
            self.description = f"{ticker}: {name}"
        self.ticker = ticker
        self.isin = isin
        self.update_price(price, date=date)

    def __repr__(self):
        return (
            f"ETF({self.name!r}, {self.price!r}, "
            f"date={self.date!r}, isin={self.isin!r}, ticker={self.ticker!r})"
        )

    def as_dict(self):
        """
        Encode the ETF as a dictionary.

        The ISIN is encoded with dictionary key 'ISIN'; the other keys are equal to the
        names of the class attributes.
        """
        return {
            "ISIN": self.isin,
            "description": self.description,
            "ticker": self.ticker,
            "name": self.name,
            "price": self.price,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, d):
        """
        Construct a lisatools.ETF from a dictionary, respecting the class
        constructor defaults.

        The `isin` class attribute is set from the 'ISIN' dictionary key.

        Parameters
        ----------
        d : dict
            The dictionary from which the ETF is constructed.
        """
        return cls(
            d["name"],
            d["price"],
            ticker=d.get("ticker", None),
            isin=d.get("ISIN", "None"),
            date=d.get("date", None),
        )
