import pandas as pd

bookings = 'Bookings.csv'
df_bookings = pd.read_csv(bookings, delimiter=',')

properties = 'Properties.csv'
df_properties= pd.read_csv(properties, delimiter=',')

print("DataFrame 1:")
print(df_bookings.head())

print("\nDataFrame 2:")
print(df_properties.head())