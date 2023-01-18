from pathlib import Path

import pytest

from lisatools import cli, Fund, Holding, Portfolio


@pytest.mark.parametrize("option", ("-h", "--help"))
def test_help(capsys, option):
    try:
        cli.main([option])
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert "usage: python -m lisatools" in out
    assert "show this help message and exit" in out
    assert err == ""


def test_plain(capsys, example_portfolio_path, example_portfolio):
    try:
        cli.main([str(example_portfolio_path)])
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert out.strip() == str(example_portfolio)
    assert err == ""


def test_json(capsys, example_portfolio_path, example_json):
    args = [str(example_portfolio_path), "--json"]
    try:
        cli.main(args)
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert out.strip() == example_json
    assert err == ""


@pytest.mark.parametrize("option", ("-o", "--output"))
def test_output(capsys, option, example_portfolio_path, example_json, tmp_path):
    file = tmp_path / "out.json"
    args = [str(example_portfolio_path), option, str(file)]
    try:
        cli.main(args)
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""
    with open(file, "r") as handle:
        written = handle.read()
    assert written.strip() == example_json


@pytest.mark.parametrize("option", ("-o", "--output"))
def test_output_plain(
    capsys, option, example_portfolio_path, example_portfolio, tmp_path
):
    file = tmp_path / "out.json"
    args = [str(example_portfolio_path), "--no-json", option, str(file)]
    try:
        cli.main(args)
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""
    with open(file, "r") as handle:
        written = handle.read()
    assert written.strip() == str(example_portfolio)


@pytest.mark.parametrize("option", ("-u", "--update"))
def test_update(capsys, option, example_portfolio_path, example_portfolio):
    args = [str(example_portfolio_path), option]
    try:
        cli.main(args)
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert err == ""
    example_portfolio.update_prices()
    assert out.strip() == str(example_portfolio)


@pytest.mark.parametrize("option", ("-c 100", "--add-cash 100"))
def test_cash(capsys, option, example_portfolio_path, example_portfolio):
    args = [str(example_portfolio_path), option]
    try:
        cli.main(args)
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert err == ""
    cash = Fund("Cash", price=100.0)
    cash_value = float(option.split(" ")[-1])
    example_portfolio.add_fund(cash, value=cash_value, target=0.0)
    assert out.strip() == str(example_portfolio)


@pytest.mark.parametrize("option", ("-r", "--rebalance"))
def test_update(capsys, option, example_portfolio_path, example_portfolio):
    args = [str(example_portfolio_path), option]
    try:
        cli.main(args)
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert err == ""
    buy, sell = example_portfolio.trade_to_target()
    buy_holdings = buy.holdings
    sell_holdings = [
        Holding(h.fund, -h.units, h.target_fraction) for h in sell.holdings
    ]
    output_portfolio = Portfolio(buy_holdings + sell_holdings)
    assert out.strip() == str(output_portfolio)
