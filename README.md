# Wages, Inflation, and Purchasing Power in Armenia (2019–2024)

A reproducible Python data-analysis project examining whether growth in Armenia's average nominal wage translated into higher purchasing power after consumer-price inflation.

## Research question

**Did Armenia's average wage grow faster than consumer prices between 2019 and 2024, and what does that imply for purchasing power?**

## Main findings

- Armenia's average monthly nominal wage increased from **AMD 182,673 in 2019** to **AMD 287,172 in 2024**, a rise of **57.2%**.
- Using 2019 as the analytical base year and compounding annual-average inflation from 2020 through 2024, the estimated consumer-price level increased by about **20.5%**.
- The resulting constructed real-wage index rises by approximately **30.4%** between 2019 and 2024.
- In the retail-price case study available in the source material, rice rose from **AMD 775/kg** to **AMD 986/kg** (**27.2%**), slower than wages.
- On this simple wage-to-price measure, rice affordability increased by about **23.6%**.

> **Important:** This is a descriptive purchasing-power exercise. It does not claim that every household became 30.4% better off.

## Repository structure

```text
armenia-wages-purchasing-power/
├── README.md
├── requirements.txt
├── .gitignore
├── analysis/
│   ├── analysis.py
│   └── wages_purchasing_power.ipynb
├── data/
│   ├── wages.csv
│   ├── cpi.csv
│   ├── consumer_prices.csv
│   ├── consumer_prices_analysis.csv
│   └── derived_indicators.csv
├── visualizations/
│   ├── wage_vs_cpi.png
│   ├── wage_inflation.png
│   ├── real_wage_index.png
│   ├── wage_vs_rice_price.png
│   └── rice_purchasing_power.png
└── report/
    └── analysis.md
```

## Visualizations

### Wage index vs. consumer-price level

![Wage vs CPI](visualizations/wage_vs_cpi.png)

### Annual wage growth vs. inflation

![Wage growth vs inflation](visualizations/wage_inflation.png)

### Estimated real wage index

![Real wage index](visualizations/real_wage_index.png)

### Wage growth compared with the rice price

![Wage vs rice price](visualizations/wage_vs_rice_price.png)

Both series start at 100 in 2019. By 2024, the wage index reaches **157.2**, while the rice-price index reaches **127.2**. The distance between the two lines makes the result immediately visible: the average wage rose substantially faster than the price of rice.

### Rice purchasing power of one average monthly wage

![Rice purchasing power](visualizations/rice_purchasing_power.png)

This chart translates the percentage result into a concrete quantity. One average monthly wage was equivalent to about **236 kg of rice in 2019** and **291 kg in 2024**. This is an increase of about **23.6%** in this product-specific purchasing-power measure.

## Methodology

### Nominal wage growth

```text
Wage growth = (Wage_t / Wage_(t-1) - 1) × 100
```

### Consumer-price index

2019 is set to 100. Annual-average inflation rates from 2020 onward are compounded:

```text
PriceIndex_t = PriceIndex_(t-1) × (1 + inflation_t / 100)
```

### Constructed real wage index

```text
RealWageIndex_t = WageIndex_t / PriceIndex_t × 100
```

### Item affordability

For an item priced in AMD per unit:

```text
Affordable quantity = Average monthly wage / Item price
```

and:

```text
Affordability change = (Quantity_2024 / Quantity_2019 - 1) × 100
```

## Data sources

1. **Statistical Committee of the Republic of Armenia (Armstat)** — average monthly nominal wages/salaries.
2. **Armstat / ArmStatBank** — annual-average consumer-price inflation.
3. **Armstat retail-price table supplied during project preparation** — selected retail-price observation used for the rice case study.

Source links:
- Armstat SDG wage indicator: https://sdg.armstat.am/8-5-1-a-iframe/
- ArmStatBank Consumer Prices: https://statbank.armstat.am/pxweb/en/ArmStatBank/ArmStatBank__1%20Econnomy%20and%20finance__12%20Consumer%20Prices/

## Reproduce the project

```bash
git clone <your-repository-url>
cd armenia-wages-purchasing-power
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -r requirements.txt
python analysis/analysis.py
```

You can also open `analysis/wages_purchasing_power.ipynb` in Jupyter Notebook or Google Colab.

## Limitations

- Average wages do not describe the full wage distribution and can differ substantially across sectors, regions, and workers.
- CPI measures the price movement of a representative basket, not the exact basket purchased by every household.
- Gross nominal wages are not the same as disposable household income.
- The retail-price section currently uses the specific product observation supported by the supplied project material; it should not be interpreted as a complete household basket.
- The analysis is descriptive and does not identify causal effects.

## Author

**Nane Narimanyan**  
Data Science student | Economic and data analysis

## License

This project is shared for portfolio and educational purposes. The statistical data remain attributable to their original source.
