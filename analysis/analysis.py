from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
VIZ = BASE / "visualizations"
VIZ.mkdir(exist_ok=True)

wages = pd.read_csv(DATA / "wages.csv")
cpi = pd.read_csv(DATA / "cpi.csv")
prices = pd.read_csv(DATA / "consumer_prices.csv")

df = wages.merge(cpi, on="year")
df["nominal_wage_growth_percent"] = df["average_monthly_nominal_wage_amd"].pct_change() * 100
df["wage_index_2019_100"] = (
    df["average_monthly_nominal_wage_amd"]
    / df.loc[df["year"] == 2019, "average_monthly_nominal_wage_amd"].iloc[0]
    * 100
)

price_index = [100.0]
for inflation in df.loc[df["year"] > 2019, "annual_average_inflation_percent"]:
    price_index.append(price_index[-1] * (1 + inflation / 100))
df["cpi_index_2019_100"] = price_index
df["real_wage_index_2019_100"] = (
    df["wage_index_2019_100"] / df["cpi_index_2019_100"] * 100
)

wage_2019 = df.loc[df["year"] == 2019, "average_monthly_nominal_wage_amd"].iloc[0]
wage_2024 = df.loc[df["year"] == 2024, "average_monthly_nominal_wage_amd"].iloc[0]
wage_change = (wage_2024 / wage_2019 - 1) * 100

prices["price_change_percent"] = (prices["price_2024"] / prices["price_2019"] - 1) * 100
prices["units_affordable_2019"] = wage_2019 / prices["price_2019"]
prices["units_affordable_2024"] = wage_2024 / prices["price_2024"]
prices["affordability_change_percent"] = (
    prices["units_affordable_2024"] / prices["units_affordable_2019"] - 1
) * 100

df.to_csv(DATA / "derived_indicators.csv", index=False)
prices.to_csv(DATA / "consumer_prices_analysis.csv", index=False)

plt.figure(figsize=(9, 5.5))
plt.plot(df["year"], df["wage_index_2019_100"], marker="o", label="Average nominal wage")
plt.plot(df["year"], df["cpi_index_2019_100"], marker="o", label="Consumer price level")
plt.axhline(100, linewidth=0.8)
plt.title("Average Wage vs. Consumer Price Level in Armenia")
plt.xlabel("Year")
plt.ylabel("Index (2019 = 100)")
plt.legend()
plt.tight_layout()
plt.savefig(VIZ / "wage_vs_cpi.png", dpi=180)
plt.close()

growth = df.dropna(subset=["nominal_wage_growth_percent"])
x = np.arange(len(growth))
width = 0.38
plt.figure(figsize=(9, 5.5))
plt.bar(x - width/2, growth["nominal_wage_growth_percent"], width, label="Nominal wage growth")
plt.bar(x + width/2, growth["annual_average_inflation_percent"], width, label="Inflation")
plt.xticks(x, growth["year"])
plt.axhline(0, linewidth=0.8)
plt.title("Annual Wage Growth vs. Inflation")
plt.xlabel("Year")
plt.ylabel("Percent")
plt.legend()
plt.tight_layout()
plt.savefig(VIZ / "wage_inflation.png", dpi=180)
plt.close()

plt.figure(figsize=(9, 5.5))
plt.plot(df["year"], df["real_wage_index_2019_100"], marker="o")
plt.axhline(100, linewidth=0.8)
plt.title("Estimated Real Wage Index in Armenia")
plt.xlabel("Year")
plt.ylabel("Index (2019 = 100)")
plt.tight_layout()
plt.savefig(VIZ / "real_wage_index.png", dpi=180)
plt.close()

# Retail-price case study: compare wage growth with rice-price growth
rice_change = prices.loc[0, "price_change_percent"]
y_wage = [100, 100 * (1 + wage_change / 100)]
y_rice = [100, 100 * (1 + rice_change / 100)]

plt.figure(figsize=(8.5, 5.5))
plt.plot([2019, 2024], y_wage, marker="o", linewidth=2.5, label="Average wage")
plt.plot([2019, 2024], y_rice, marker="o", linewidth=2.5, label="Rice price")
plt.xticks([2019, 2024])
plt.ylabel("Index (2019 = 100)")
plt.title("Wages Rose Faster Than the Price of Rice")
plt.text(2024, y_wage[1] + 2, f"{y_wage[1]:.1f}", ha="center")
plt.text(2024, y_rice[1] + 2, f"{y_rice[1]:.1f}", ha="center")
plt.text(2019, 102, "100", ha="center")
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(VIZ / "wage_vs_rice_price.png", dpi=180, bbox_inches="tight")
plt.close()

# Translate affordability into an intuitive quantity: kg of rice purchasable with one average monthly wage
q2019 = prices.loc[0, "units_affordable_2019"]
q2024 = prices.loc[0, "units_affordable_2024"]

plt.figure(figsize=(7.5, 5.5))
bars = plt.bar(["2019", "2024"], [q2019, q2024], width=0.58)
plt.ylabel("Kilograms of rice")
plt.title("How Much Rice Could One Average Monthly Wage Buy?")
for bar, value in zip(bars, [q2019, q2024]):
    plt.text(bar.get_x() + bar.get_width()/2, value + 4, f"{value:.0f} kg", ha="center", fontweight="bold")
plt.text(0.5, max(q2019, q2024) * 0.55, f"+{(q2024/q2019 - 1)*100:.1f}% purchasing capacity", ha="center")
plt.ylim(0, max(q2019, q2024) * 1.18)
plt.tight_layout()
plt.savefig(VIZ / "rice_purchasing_power.png", dpi=180, bbox_inches="tight")
plt.close()

print(df.round(2))
print()
print(prices.round(2))
