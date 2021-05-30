import pandas as pd
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 1000)
df = pd.read_csv('tripadvisor_european_restaurants_reduced.zip', compression='zip')
print(df.head())
hotel = pd.DataFrame(df)
print(hotel.columns.tolist())
hotel.pop('keywords')
hotel.pop('city')
hotel.pop('province')
hotel.pop('address')
hotel.pop('atmosphere')
print(hotel.shape)
hotel['awards']= hotel['awards'].fillna('None')
hotel['features']= hotel['features'].fillna('None')
hotel_refine = hotel[pd.notnull(hotel['value'])]
print(hotel_refine.shape)
hotel_refine1 = hotel_refine[pd.notnull(hotel_refine['price_level'])]
print(hotel_refine1.shape)
hotel_refine2 = hotel_refine1[pd.notnull(hotel_refine1['avg_rating'])]
print(hotel_refine2.shape)
hotel_refine3 = hotel_refine2[pd.notnull(hotel_refine2['cuisines'])]
print(hotel_refine3.shape)
hotel_refine4 = hotel_refine3[pd.notnull(hotel_refine3['region'])]
print(hotel_refine4.shape)
print(hotel_refine4.head())
print(hotel_refine4.isnull().sum())
print(hotel_refine4['country'].value_counts())

import numpy as np
from matplotlib import pyplot as plt
#colours = {'France':'blue', 'England':'red', 'Ireland': 'green'}
plt.scatter(x=hotel_refine4['avg_rating'], y=hotel_refine4['total_reviews_count'])
plt.xlabel('Average rating of restaurant')
plt.ylabel('No. of total reviews')
plt.title('Scatter plot showing effect of total no of reviews on average rating')
plt.show()
plt.close()
#Too much data
#Use Ireland only
hotel_refine4.set_index('country', inplace = True)
restaurant_ireland = hotel_refine4.loc[['Ireland','Northern Ireland']]
print(restaurant_ireland.head())
#Drop Dunmurry as only 1 item and makes no sense
restaurant_ireland= restaurant_ireland[restaurant_ireland != 'Dunmurry']
#Change Belfast to Ulster
restaurant_ireland['region'] = restaurant_ireland['region'].replace(['Belfast'],'Province of Ulster')
print(restaurant_ireland['region'].value_counts())
plt.scatter(x=restaurant_ireland['avg_rating'], y=restaurant_ireland['total_reviews_count'])
plt.xlabel('Average rating of restaurants in Ireland')
plt.ylabel('No. of total reviews')
plt.title('Scatter plot showing effect of total no of reviews on average rating in Ireland')
plt.show()

#Lets see 5star resturant distribution
restaurant_ireland5 = restaurant_ireland.loc[restaurant_ireland['avg_rating'] == 5.0]
print(restaurant_ireland5.head())
plt.hist(restaurant_ireland5['region'])
plt.xlabel('Region')
plt.ylabel('No. of 5star restaurants')
plt.title('Locations of 5star rated restaurants in Ireland')
plt.show()

#Michelin Star Restaurants
df_onestar = pd.read_csv('one-star-michelin-restaurants.csv')
df_twostar = pd.read_csv('two-stars-michelin-restaurants.csv')
df_threestar = pd.read_csv('three-stars-michelin-restaurants.csv')

one_star_restaurant= pd.DataFrame(df_onestar)
two_star_restaurant = pd.DataFrame(df_twostar)
three_star_restaurant =pd.DataFrame(df_threestar)
print(one_star_restaurant.columns.tolist())
one_star_restaurant['Star'] = '1'
two_star_restaurant['Star'] = '2'
three_star_restaurant['Star'] = '3'
#No longer need to check these three.
#print(one_star_restaurant.head())
#print(two_star_restaurant.head())
#print(three_star_restaurant.head())
star_restaurant_df = [one_star_restaurant, two_star_restaurant, three_star_restaurant]
star_restaurant = pd.concat(star_restaurant_df)
print(star_restaurant.head())
print(star_restaurant.columns.tolist())





#import requests

#url = "https://travel-advisor.p.rapidapi.com/restaurants/list"

#querystring = {"location_id":"293919","restaurant_tagcategory":"10591","restaurant_tagcategory_standalone":"10591","currency":"USD","lunit":"km","limit":"30","open_now":"false","lang":"en_US"}

#headers = {
 #   'x-rapidapi-key': "3e5ee6b200msh8bafd806e6e5a41p142121jsn0f80884ee934",
  #  'x-rapidapi-host': "travel-advisor.p.rapidapi.com"
   # }

#response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

