import requests
from caltechdata_api import decustomize_schema

url = 'https://data.caltech.edu/api/records'

response = requests.get(url+'/?q=subjects:thesis')
hits = response.json()

for h in hits['hits']['hits']:
    metadata = decustomize_schema(h['metadata'])
    if 'geoLocations' in metadata:
        geo = metadata['geoLocations']
        for g in geo:
            if 'geoLocationBox' in g:
                box = g['geoLocationBox']
                print(box)
            if 'geoLocationPoint' in g:
                point = g['geoLocationPoint']
                print(point)
            if 'geoLocationPlace' in g:
                place = g['geoLocationPlace']
                print(place)
