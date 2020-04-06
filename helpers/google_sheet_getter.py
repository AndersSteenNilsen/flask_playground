from datetime import datetime

import pandas as pd
import requests
import json

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSMEaeKFECXRmgRDVnk7Fr59xi2A6Kr-0jwEQjqUbXoZfukcqZ8PySOw_Y85DHK5aLCAfCcgECmE5fg/pub?output=csv&gid=0'
df = pd.read_csv(url)


def get_feature_collection(street):
    parameters = {'q': street,
                  'format': 'geojson',
                  'polygon_geojson': '1',
                  'addressdetails': '1',
                  'viewbox': '10.49137,59.97305,11.14368,59.88704',
                  'bounded': '1',
                  'email': 'asteennilsen@gmail.com'}
    url = 'https://nominatim.openstreetmap.org/search?'
    return requests.get(url=url, params=parameters)


def add_wash_date_property(features, date):
    for features in features:
        features['properties']['wash_date'] = date
        features['properties']['washed'] = datetime.now() > datetime.strptime(date, '%d.%m.%Y')


def json_dump(data, path='../static/json/streetdata.json'):
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=2)


all_streets = get_feature_collection(df['Gatenavn'][0]).json().copy()


def get_data(df):
    for index, row in df.iterrows():
        try:
            response = get_feature_collection(row['Gatenavn'])
            if response.status_code == 200:
                features = response.json()
            else:
                print(index, row['Gatenavn'], 'Could not be found')
                continue
            street_features = [street for street in features['features'] if street['geometry']['type'] == 'LineString']
            add_wash_date_property(street_features, row['Dato'])
            all_streets['features'] += street_features
            print(index, '/', len(df))
        except json.JSONDecodeError:
            print('decodeError', index)
        except:
            print('error', index)


get_data(df)
json_dump(all_streets)
# print(df)
