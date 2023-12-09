import pandas as pd
import json

dane = pd.read_csv('dane.csv').drop('Unnamed: 0', axis=1)

dane['device'] = dane['device'].apply(lambda x: json.loads(x))
dane['geoNetwork'] = dane['geoNetwork'].apply(lambda x: json.loads(x))


device_norm = pd.json_normalize(dane['device'])
geo_norm = pd.json_normalize(dane['geoNetwork'])


result = pd.concat([dane, device_norm, geo_norm], axis=1).drop(['device','geoNetwork'],axis=1)

#Memory release
dane = None

result['date'] = pd.to_datetime(result['date'], format='%Y%m%d')
result['fullVisitorId'] = result['fullVisitorId'].astype(int)
result['isMobile'] = result['isMobile'].astype(bool)
#The rest remains the same in this case due to the demo data version

# Taking only the 5 most recent ones for each country
last_5 = result[['date','fullVisitorId', 'browser', 'country']] \
    .sort_values(by=['country', 'date'], ascending=[True, False]) \
    .groupby('country').head(5)


#Removing the lack of a country
last_5 = last_5[last_5['country'] != '(not set)']

#Changing the date format to a string to enable saving to JSON
last_5['date'] = last_5['date'].dt.strftime('%Y-%m-%d')


#Building a dictionary that will be transformed into JSON
json_dane = {}

for index, row in last_5.iterrows():
    country = row['country']
    browser = row['browser']
    fullVisitorId = row['fullVisitorId']
    date = row['date']
    
    if country not in json_dane:
        json_dane[country] = {}
    
    if browser not in json_dane[country]:
        json_dane[country][browser] = []
    
    json_dane[country][browser].append({fullVisitorId: date})


with open('dane.json', 'w') as json_file:
    json.dump(json_dane, json_file, indent=2)