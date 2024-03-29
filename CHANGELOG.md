# Changelog

<!--next-version-placeholder-->

## v0.5.1 (2023-01-24)
### Fix
* **Portfolio.__getitem__:** Use operator.index ([`7402eca`](https://github.com/istvankleijn/lisatools/commit/7402eca4db71c4d946cc654a14a7ed4753f52b6f))

## v0.5.0 (2023-01-18)
### Feature
* Remember fund price data using time-to-live cache ([`d64c650`](https://github.com/istvankleijn/lisatools/commit/d64c65045257c6ec67b1cd7dd86e314e9a2471b8))
* **Portfolio.save:** Optionally silence output ([`458babb`](https://github.com/istvankleijn/lisatools/commit/458babb4f551f0bf93354e946632cb1088ac10b9))
* Provide command-line interface for price updates,  rebalancing, and new purchases ([`f43c4f3`](https://github.com/istvankleijn/lisatools/commit/f43c4f37d78dced00dc89a223b16234c56d91494))

## v0.4.0 (2023-01-04)
### Feature
* Extend JSON saving/loading to handle ETF holdings ([`d4a007a`](https://github.com/istvankleijn/lisatools/commit/d4a007aa9758d73ec800d218619c9b4c67481341))
* **Portfolio:** Add load and save functionality in JSON format ([`e2e383a`](https://github.com/istvankleijn/lisatools/commit/e2e383a707cc6b6a0fda3fa5ac23e52686c32b40))
* Provide custom JSON encoder and decoder ([`e2d69e5`](https://github.com/istvankleijn/lisatools/commit/e2d69e5d7448cbb0cf1c3b61e7488a4bfa4ae4ec))
* **Fund:** Use update_price to handle ISO strings ([`99e180e`](https://github.com/istvankleijn/lisatools/commit/99e180eaa89f937e799a5de89d8909404bc6a874))
* Convert Funds/Holdings to/from dictionaries ([`3055b6f`](https://github.com/istvankleijn/lisatools/commit/3055b6f377efe945229e9025bd03e2daa195eff3))

## v0.3.2 (2022-12-21)
### Fix
* Add dependencies for scraping ([`8b666ec`](https://github.com/istvankleijn/lisatools/commit/8b666ec98a284cd12c701fe25d447238878ae937))

## v0.3.1 (2022-12-21)
### Documentation
* Updated example notebook ([`8d88a84`](https://github.com/istvankleijn/lisatools/commit/8d88a84c645b2865962ace4c732d443c324db135))

## v0.3.0 (2022-12-02)
### Feature
* **Portfolio:** Construct portfolio directly from funds ([`98d3185`](https://github.com/istvankleijn/lisatools/commit/98d31854178d0a449a273132497a9fa55ea40778))
* **Portfolio:** Allow iteration over holdings ([`dcd11e3`](https://github.com/istvankleijn/lisatools/commit/dcd11e3ab1d55954ee7968a48c8e33f3dace3254))
* Implement equality checking ([`ffac284`](https://github.com/istvankleijn/lisatools/commit/ffac284ee32b6de956541cd8eb1011e3b30ee336))
* **Portfolio:** Implement basic sequence protocol ([`20f8b9a`](https://github.com/istvankleijn/lisatools/commit/20f8b9ac2eaaf889c3254eb7f55771b1948d3e21))
* Move Portfolio data to holdings attribute ([`da712e7`](https://github.com/istvankleijn/lisatools/commit/da712e7e3fd1cf2013c98b0049f38169fd4aaf16))

### Fix
* **Portfolio.from_funds:** Assert equal lengths of funds, units held, and target fractions ([`af543aa`](https://github.com/istvankleijn/lisatools/commit/af543aabd970136f160bdac32a695f25388bbc3e))

## v0.2.4 (2022-11-30)
### Fix
* Fix issues from initial flakeheaven run ([`41a29a5`](https://github.com/istvankleijn/lisatools/commit/41a29a546ea61f643fd4d51b07e9ad02031632da))

- Format code with Black
- Lint code with flakeheaven

## v0.2.3 (2022-11-29)

- Set up continuous deployment with PSR

## v0.2.1 (2022-11-29)

- Set up continuous integration
- Correct handling of current date

## v0.2.0 (2022-11-28)

- Added ETF class
- Implemented price updating using FT data scraping

## v0.1.0 (2022-11-23)

- First public release!
- Bugfixes
- Rewritten tests
- Expanded documentation

## v0.0.3 (2022-11-22)

- Implemented target portfolio and trades to reach it
- Added string representation methods
- Provided usage examples

## v0.0.2 (8/11/2022)

- Populated package namespace
- Added explicit implementation of `Fund` class

## v0.0.1 (1/11/2022)

- First release of `lisatools`!