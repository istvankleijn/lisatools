import argparse

from lisatools.fund import Fund
from lisatools.portfolio import Holding, Portfolio


def main(args=None):
    parser = argparse.ArgumentParser(
        prog="python -m lisatools",
        description="Tools for monitoring a stocks and shares portfolio.",
    )
    parser.add_argument(
        "input",
        help="Input file containing portfolio data in JSON format.",
        metavar="FILE",
    )
    actions = parser.add_argument_group(
        "actions",
        description=(
            "Carry out zero or more actions from the following list. "
            "Actions are executed in the order specified below. "
            "If no action is provided, return the input portfolio. "
        ),
    )
    actions.add_argument(
        "-u",
        "--update",
        help="update price data",
        action="store_true",
    )
    actions.add_argument(
        "-c",
        "--add-cash",
        help="add cash to the portfolio",
        action="store",
        type=float,
        dest="cash_added",
        metavar="VALUE",
    )
    actions.add_argument(
        "-r",
        "--rebalance",
        help="calculate trades required to rebalance to the target allocations",
        action="store_true",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output to file (if no file specified, print to terminal)",
        dest="output_file",
        metavar="FILE",
    )
    parser.add_argument(
        "--json",
        help=(
            "provide output portfolio in JSON format "
            "(default yes if output file specified, no otherwise) "
        ),
        action=argparse.BooleanOptionalAction,
    )
    options = parser.parse_args(args)  # if args == None, uses sys.argv[1:]

    if options.json is None:
        options.json = options.output_file is not None

    pf = Portfolio.load(options.input)

    if options.update:
        pf.update_prices()

    if options.cash_added is not None:
        cash = Fund("Cash", price=100.0)
        pf.add_fund(cash, value=options.cash_added, target=0.0)

    if options.rebalance:
        buy, sell = pf.trade_to_target()
        buy_holdings = buy.holdings
        sell_holdings = [
            Holding(h.fund, -h.units, h.target_fraction) for h in sell.holdings
        ]
        pf = Portfolio(buy_holdings + sell_holdings)

    s = pf.save(file=None, silent=True) if options.json else str(pf)
    if options.output_file is None:
        print(s)
    else:
        with open(options.output_file, "w") as handle:
            handle.write(s)


if __name__ == "__main__":
    main()
