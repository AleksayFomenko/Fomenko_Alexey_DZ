import pandas as pd
df = pd.read_csv('Electronic_sales_Sep2023-Sep2024.csv', sep=',',  header=0, date_format='%Y-%m-%d')

'''
#если надо вычислять 
df['high'] = pd.to_numeric(df['high'])
df['low'] = pd.to_numeric(df['low'])

# Теперь можем выполнить вычисления
df['high_low_diff'] = df['high'] - df['low']
'''