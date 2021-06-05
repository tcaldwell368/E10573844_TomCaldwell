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
import seaborn as sns
hotel_refine4['country'].value_counts().sort_values(ascending = False).plot(kind='bar')
plt.title('No of restaurants in each Country')
plt.xlabel('Country')
plt.ylabel('Number of restaurants')
plt.show()
plt.scatter(x=hotel_refine4['avg_rating'], y=hotel_refine4['total_reviews_count'])
plt.xlabel('Average rating of restaurant')
plt.ylabel('No. of total reviews')
plt.title('Scatter plot showing effect of total no of reviews on average rating')
plt.show()
plt.close()

#Showing if having nutritional options helps wth avg_rating
#Use height and aspect to make graphs more appealing, can see trend better
#g = sns.PairGrid(hotel_refine4, y_vars="avg_rating",
 #                x_vars=["vegetarian_friendly", "vegan_options", "gluten_free"],
  #               height=7, aspect=1)
#g.map(sns.pointplot, color="xkcd:coral")
#plt.show()


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

#Get awards to say Yes or None, None already added
restaurant_ireland.loc[restaurant_ireland['awards'] != 'None', 'awards'] = 'Yes'
#print(restaurant_ireland.head()) , check complete, any award is replaced with Yes

ax = sns.violinplot(x="price_level", y="avg_rating", hue="awards",
                    data=restaurant_ireland, order=['€','€€-€€€','€€€€'], palette="muted", split=True)
plt.legend(loc='lower right')
plt.show()

#Michelin Star Restaurants
#Only contains updated restaurants to some countries for last 2 years
df_onestar = pd.read_csv('one-star-michelin-restaurants.csv')
df_twostar = pd.read_csv('two-stars-michelin-restaurants.csv')
df_threestar = pd.read_csv('three-stars-michelin-restaurants.csv')

one_star_restaurant= pd.DataFrame(df_onestar)
two_star_restaurant = pd.DataFrame(df_twostar)
three_star_restaurant =pd.DataFrame(df_threestar)
print(one_star_restaurant.columns.tolist())
one_star_restaurant['Star'] = 1
two_star_restaurant['Star'] = 2
three_star_restaurant['Star'] = 3
#No longer need to check these three.
#print(one_star_restaurant.head())
#print(two_star_restaurant.head())
#print(three_star_restaurant.head())
star_restaurant_df = [one_star_restaurant, two_star_restaurant, three_star_restaurant]
star_restaurant = pd.concat(star_restaurant_df)
print(star_restaurant.head())
print(star_restaurant.columns.tolist())
print(star_restaurant.shape)

#Change some cities name to the regions
us_cities=['California','Chicago','New York City','Washington DC']
brazil_cities=['Rio de Janeiro','Sao Paulo']
star_restaurant['region'] = star_restaurant['region'].replace(us_cities,'USA')
star_restaurant['region'] = star_restaurant['region'].replace(brazil_cities,'Brazil')
star_count_region = star_restaurant.groupby('region',as_index= False)['Star'].agg({'sum','count'})
star_count_region.sort_values(by=['sum'], ascending =False)
print(star_count_region)
print(star_count_region.columns.tolist())

# Plot the total 'new stars'
sns.set_color_codes("bright")
sns.barplot(x="sum", y=star_count_region.index, data=star_count_region,
            label="Total Stars Updated", color='g')
# Plot the sum of restaurants updated
sns.set_color_codes("dark")
sns.barplot(x="count", y=star_count_region.index, data=star_count_region,
            label="Top restaurants updated",color='g')
plt.legend(ncol=2, loc="lower right", frameon=True)
plt.ylabel('Region')
plt.xlabel('Count of updated stars')
plt.show()


#Take EU ones, merge with hotel_refine4 or take restaurant and merge with irish ones



#No of Michelin Star Restaurants in the previously used df
#print(hotel_refine4['latitude'].isin(star_restaurant['latitude']).value_counts())
#print(hotel_refine4['longitude'].isin(star_restaurant['longitude']).value_counts())
star_restaurant.rename(columns={'name':'restaurant_name'},inplace=True)

#Inner Join all updated michelin resturants into
#restaurants_and_stars = hotel_refine4.merge(star_restaurant,on=('restaurant_name'),suffixes=('_rest','_star' ))
#print(restaurants_and_stars.head())
#print(restaurants_and_stars.shape)






#import requests
#import json
#url = "https://travel-advisor.p.rapidapi.com/restaurants/list-by-latlng"

#querystring = {"latitude":"53.35014","longitude":"-6.266155","limit":"30","distance":"10","open_now":"false","lunit":"km","min_rating":"3"}

#headers = {
 #   'x-rapidapi-key': "3e5ee6b200msh8bafd806e6e5a41p142121jsn0f80884ee934",
  #  'x-rapidapi-host': "travel-advisor.p.rapidapi.com"
   # }

#response = requests.request("GET", url, headers=headers, params=querystring)

#things=response.text
#data_api = json.loads(things)
#data_api_normal=pd.json_normalize(data_api,'data')
#print(data_api_normal.head())
