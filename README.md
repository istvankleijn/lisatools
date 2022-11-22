# lisatools

Tools for monitoring my Lifetime ISA portfolio.

## Installation

```bash
$ pip install lisatools
```

## Usage

`lisatools` provides classes and functions that help me manage my Lifetime ISA
fund portfolio. For example, I can calculate the trades required to obtain
my target portfolio as in the following snippet:

```python
import lisatools
import datetime

ftse_global = lisatools.Fund(
    "FTSE Global All Cap Index Fund",
    172.14,
    isin="GB00BD3RZ582",
    date=datetime.date(2022, 11, 21)
)
gilts = lisatools.Fund(
    "U.K. Gilt UCITS ETF (VGOV)",
    18.58,
    isin="IE00B42WWV65",
    date=datetime.date(2022, 11, 21)
)
holding1 = lisatools.Holding(ftse_global, 1.0, 0.6)
holding2 = lisatools.Holding(gilts, 5.0, 0.4)
pf = lisatools.Portfolio([holding1, holding2])

buy, sell = pf.trade_to_target()
print("Buy:\n=====", buy, "\nSell:\n=====", sell, sep = "\n")
```

[A more elaborate example](/docs/example.ipynb) is provided in the /docs/ folder.

## License

`lisatools` was created by Istvan Kleijn. It is licensed under the terms of the MIT license.

## Credits

`lisatools` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
