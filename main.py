import pandas as pd
df = pd.read_csv('tripadvisor_european_restaurants_reduced.zip', compression='zip')
print(df.head())
hotel = pd.DataFrame(df)
print(hotel.columns.tolist())
hotel.pop('keywords')
print(hotel.shape)
hotel_refine = hotel.dropna(how = 'all' , subset =['value','price_level'] )
print(hotel_refine.shape)
print(hotel_refine.head())


