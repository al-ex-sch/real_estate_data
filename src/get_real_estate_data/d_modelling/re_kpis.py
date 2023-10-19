##
import pandas as pd
import numpy_financial as npf

# Dummy data for 3 properties
data = {
    'price': [200000, 300000, 250000],
    'prediction': [1500, 2000, 1800],
    'down_payment': [40000, 60000, 50000],
    'closing_costs': [5000, 7500, 6000],
    'renovation_costs': [10000, 15000, 12000]
}
df = pd.DataFrame(data)

# Calculate annual rent, expenses (5%), and net profit
df['annual_rent'] = df['prediction'] * 12
df['expenses'] = df['annual_rent'] * 0.05
df['net_profit'] = df['annual_rent'] - df['expenses']

# Calculate total cash invested
df['total_cash_invested'] = df['down_payment'] + df['closing_costs'] + df['renovation_costs']

# Calculate Cash-on-Cash return
df['cash_on_cash_return'] = (df['net_profit'] / df['total_cash_invested']) * 100

# Dummy cash flows for IRR calculation (initial investment, 5 years of net profit, final sale proceeds)
cash_flows = [
    [-55000, 18000, 18000, 18000, 18000, 18000, 220000],
    [-82500, 24000, 24000, 24000, 24000, 24000, 330000],
    [-68000, 21600, 21600, 21600, 21600, 21600, 270000]
]

# Calculate IRR for each property
df['irr'] = [npf.irr(cf) * 100 for cf in cash_flows]

# Display results
print(df[['price', 'prediction', 'net_profit', 'total_cash_invested', 'cash_on_cash_return', 'irr']])
