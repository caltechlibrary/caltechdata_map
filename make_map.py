import requests
from caltechdata_api import decustomize_schema
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.tile_providers import STAMEN_TERRAIN
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, Range1d, PanTool,
WheelZoomTool, BoxSelectTool
)
from pyproj import Proj, transform

url = 'https://data.caltech.edu/api/records'

response = requests.get(url+'/?q=subjects:thesis')
hits = response.json()

fig = figure(tools='pan, wheel_zoom', plot_height=600, plot_width=600)
fig.axis.visible = False
fig.add_tile(STAMEN_TERRAIN)

# transform lng/lat to meters
from_proj = Proj(init="epsg:4326")
to_proj = Proj(init="epsg:3857")

for h in hits['hits']['hits']:
    metadata = decustomize_schema(h['metadata'])
    if 'geoLocations' in metadata:
        geo = metadata['geoLocations']
        for g in geo:
            if 'geoLocationBox' in g:
                box = g['geoLocationBox']
                lat=[box['northBoundLatitude'],box['northBoundLatitude'],box['southBoundLatitude'],box['southBoundLatitude']]
                lon=[box['eastBoundLongitude'],box['westBoundLongitude'],box['eastBoundLongitude'],box['westBoundLongitude']]
                tlon,tlat = transform(from_proj,to_proj,lon,lat)
                source = ColumnDataSource(
                   data=dict(
                        lat=tlat,
                        lon=tlon,
                        )
                )
                circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
                fig.add_glyph(source, circle)               
            if 'geoLocationPoint' in g:
                point = g['geoLocationPoint']
                print(point)
            if 'geoLocationPlace' in g:
                place = g['geoLocationPlace']
                print(place)

output_file("stamen_toner_plot.html")
show(fig)
