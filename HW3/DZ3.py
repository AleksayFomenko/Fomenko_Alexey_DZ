import pandas as pd
df = pd.read_csv('Electronic_sales_Sep2023-Sep2024.csv', sep=',', header=0, date_format='%Y-%m-%d')

# Определения предпочитаемого метода оплаты на основе потраченных денег

df.dropna(subset=['Payment Method', 'Total Price', 'Add-on Total'], inplace=True)
Grouped_pay_methods = df.groupby(by = [ 'Customer ID', 'Payment Method' ]).agg(
    {
        'Total Price' : 'sum'
    }
)
Pref_payment_ind = Grouped_pay_methods.groupby("Customer ID")['Total Price'].idxmax()
Pref_payment_method = Grouped_pay_methods.loc[Pref_payment_ind].reset_index()


Sum_and_ads = df.groupby('Customer ID').agg(
    {
        'Total Price' : 'sum',
        'Add-on Total' : 'sum'
    }
).reset_index()


result = pd.merge(Pref_payment_method.drop('Total Price',axis=1), Sum_and_ads, on="Customer ID")
print(result)
