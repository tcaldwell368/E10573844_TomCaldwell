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
hotel_refine4['country'].value_counts().sort_values(ascending = False).plot(kind='bar', figsize = (16,9))
plt.title('No of restaurants in each Country')
plt.xlabel('Country')
plt.ylabel('Number of restaurants')
plt.xticks(rotation=30, horizontalalignment="center")
plt.show()

#No real trend seen
#Showing only for restaurants will more than 6000 reviews
plt.figure(figsize=(15,10))
plt.scatter(x=hotel_refine4['total_reviews_count'], y=hotel_refine4['avg_rating'],s=150, alpha=0.4,edgecolor='red')
plt.xlabel('Average rating of restaurant')
plt.ylabel('No. of total reviews')
plt.title('Scatter plot showing effect of total no of reviews on average rating')
plt.show()
#See if no. of reviews controls it
plt.figure(figsize=(15,10))
plt.scatter(x=hotel_refine4['total_reviews_count'], y=hotel_refine4['avg_rating'],s=150, alpha=0.4,edgecolor='red')
plt.xlabel('Average rating of restaurant')
plt.ylabel('No. of total reviews')
plt.title('Scatter plot of total no. of reviews on average rating, with at least 6000 reviews')
plt.xlim(6000)
plt.show()

country_names=['Italy','France','England','Spain','Germany','Greece','Portugal','Belgium','Austria', 'Scotland','Poland'\
               , 'Ireland', 'Wales', 'Czech','Croatia','Sweden','Slovakia','Hungary','NI']
country_names_sort= sorted(country_names)
#Use of pivot table and numpy
#Use of dictionary for aggfunc
#Use of looping/itterows for annotate
restaurant_pivot = pd.pivot_table(hotel_refine4, index =['country'], values=['avg_rating', 'total_reviews_count'],
           aggfunc={'avg_rating':[np.mean], 'total_reviews_count':np.sum})
print(restaurant_pivot)
country_numbers = hotel_refine4['country'].value_counts()
plt.figure(figsize=(20,8))
plt.scatter(x= restaurant_pivot['total_reviews_count'], y= restaurant_pivot['avg_rating'], s= (country_numbers/300)\
            , alpha = 0.5)

for idx, row in restaurant_pivot.iterrows():
    plt.annotate(idx, (row['total_reviews_count'], row['avg_rating']) )


plt.show()


#Use Ireland only
hotel_refine4.set_index('country', inplace = True)
restaurant_ireland = hotel_refine4.loc[['Ireland','Northern Ireland']]
print(restaurant_ireland.head())
#Drop Dunmurry as only 1 item and makes no sense
restaurant_ireland= restaurant_ireland[restaurant_ireland != 'Dunmurry']
#Change Belfast to Ulster
restaurant_ireland['region'] = restaurant_ireland['region'].replace(['Belfast'],'Province of Ulster')
print(restaurant_ireland['region'].value_counts())

#Total reviews affect avg_rating in Ireland?
ax = sns.stripplot(x="avg_rating", y="total_reviews_count",data = restaurant_ireland, edgecolor='gray',linewidth=1, jitter = 0.4)
plt.xlabel('Avg Rating')
plt.ylabel('Total Review Counts')
plt.title('Total reviews against Avg Rating for Ireland')
plt.show()
#Same for region, lets investigate further,

#Lets see 5star resturant distribution, region affect ?
restaurant_ireland5 = restaurant_ireland.loc[restaurant_ireland['avg_rating'] == 5.0]
print(restaurant_ireland5.head())
plt.hist(restaurant_ireland5['region'], color = 'green')
plt.xlabel('Region')
plt.ylabel('No. of 5star restaurants')
plt.title('Locations of 5star rated restaurants in Ireland by Region')
plt.show()
#5 Star rating across all Ireland

#Get awards to say Yes or None, None already added
restaurant_ireland.loc[restaurant_ireland['awards'] != 'None', 'awards'] = 'Yes'
#print(restaurant_ireland.head()) , check complete, any award is replaced with Yes

#See if awards helps with avg_rating, and looking at price_level as well
ax = sns.violinplot(x="price_level", y="avg_rating", hue="awards",
                    data=restaurant_ireland, order=['€','€€-€€€','€€€€'], palette="muted", split=True)
plt.xlabel('Price Ranges')
plt.ylabel('Avg Rating')
plt.title('Violin Plot of Distribution of Avg Rating by Price Level')
plt.legend(loc='lower right')
plt.show()


#Showing if having nutritional options helps wth avg_rating in Ireland
#Use height and aspect to make graphs more appealing, can see trend better
g = sns.PairGrid(restaurant_ireland, y_vars="avg_rating",
             x_vars=["vegetarian_friendly", "vegan_options", "gluten_free"],
              height=6.5, aspect=1.3)
g.map(sns.pointplot, color="xkcd:coral")
plt.xlabel('Nutritional Options')
plt.ylabel('Avg Rating')
plt.title('Showing changes in Avg Rating when Nutritional Options Offered')
plt.show()
#Side by sie can see that have the nutritional options helps customer rating

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

#Change some cities name to the regions/country
us_cities=['California','Chicago','New York City','Washington DC']
brazil_cities=['Rio de Janeiro','Sao Paulo']
star_restaurant['region'] = star_restaurant['region'].replace(us_cities,'USA')
star_restaurant['region'] = star_restaurant['region'].replace(brazil_cities,'Brazil')
star_count_region = star_restaurant.groupby('region',as_index= False)['Star'].agg({'sum','count'})
star_count_region.sort_values(by='sum', ascending =False)
print(star_count_region)
print(star_count_region.columns.tolist())

#Exploring regions getting new michelin stars, See new total sum stars added to a region,
#and no. restaurants restaurants getting new stars
#The difference is figures is that some restaurants could be changing to 2 stars.
# Plot the total 'new stars'
plt.figure(figsize=(15,10))
sns.set_color_codes("bright")
sns.barplot(x="sum", y=star_count_region.index, data=star_count_region,
            label="Sum of Totals New Stars in Region", color='r')
# Plot the sum of restaurants updated
sns.set_color_codes("dark")
sns.barplot(x="count", y=star_count_region.index, data=star_count_region,
            label="Total Restaurants getting new Star",color='r')
plt.legend(ncol=2, loc="upper right", frameon=True)
plt.ylabel('Country')
plt.xlabel('Count of updated stars')
plt.title('Barplot showing Total number of Michelin Star changes for Country')
plt.show()
#UK and other europe regions present, lets see if no stars have correlation to the ratings

#Change hotel_refine4 to say UK, and restaurant_name to be name
#Merge with star_restaurants on name, will merge the European places.
#Need to reset index of hotel_refine4 as country used as index before
#Change column names so can merge on them (Could do left_on and right_on)
#Inner join to keep only michelin restaurants
hotel_refine4.reset_index(inplace=True)
hotel_refine4["country"].replace({"England": "United Kingdom", "Scotland": "United Kingdom", "Wales" : "United Kingdom"}, inplace=True)
star_restaurant.rename(columns={'region':'country'}, inplace= True)
hotel_refine4.rename(columns={'restaurant_name':'name'}, inplace= True)
restaurant_euro_star = hotel_refine4.merge(star_restaurant, on=('name','country'), suffixes=('_rest','_star'))
print(restaurant_euro_star.head())
print(restaurant_euro_star['country'].value_counts())
#Primarily UK included now
restaurant_euro_star.loc[restaurant_euro_star['features'] != 'None', 'features'] = 'Yes'
restaurant_euro_star['rating_metric'] = restaurant_euro_star['food']+restaurant_euro_star['service']+ \
            restaurant_euro_star['value']
#See how stared restaurants,
ax =  sns.swarmplot(x="rating_metric", y="features", hue="Star",
                   data=restaurant_euro_star,palette = 'bright', edgecolor='red', linewidth=0.3, size=3.2)
plt.show()
#Features little change,


#import requests
#import json
#url = "https://travel-advisor.p.rapidapi.com/restaurants/list-by-latlng"

#querystring = {"latitude":"53.35014","longitude":"-6.266155","limit":"30","distance":"10","open_now":"false","lunit":"km","min_rating":"3"}

#headers = {
#   'x-rapidapi-key': "3e5ee6b200msh8bafd806e6e5a41p142121jsn0f80884ee934",
#   'x-rapidapi-host': "travel-advisor.p.rapidapi.com"
 #   }

#response = requests.request("GET", url, headers=headers, params=querystring)

#things=response.text
#data_api_dub = json.loads(things)
#data_api_dub_normal= pd.json_normalize(data_api_dub,'data')
#print(data_api_dub_normal.head())






