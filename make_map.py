import requests
from caltechdata_api import decustomize_schema
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.tile_providers import STAMEN_TERRAIN
from bokeh.models import (
  CustomJS, TapTool, ColumnDataSource, Circle, Range1d, PanTool,
WheelZoomTool, BoxSelectTool, Segment, HoverTool
)
from pyproj import Proj, transform

url = 'https://data.caltech.edu/api/records'

response = requests.get(url+'/?size=1000&q=subjects:thesis')
hits = response.json()

hover = HoverTool(tooltips=[
    ("Title", "@title"),
    ("Author", "@author"),
    ("Year", "@year"),
])

fig = figure(tools=[hover,'wheel_zoom','pan'], active_scroll='wheel_zoom', plot_height=600, plot_width=600)
fig.axis.visible = False
fig.add_tile(STAMEN_TERRAIN)

# transform lng/lat to meters
from_proj = Proj(init="epsg:4326")
to_proj = Proj(init="epsg:3857")

print(len(hits['hits']['hits']))

#Collect data for plot
pt_lat=[]
pt_lon=[]
identifier=[]
author = []
title = []
year = []
x0=[]
y0=[]
x1=[]
y1=[]

for h in hits['hits']['hits']:
    print(h['id'])
    metadata = decustomize_schema(h['metadata'])
    if 'geoLocations' in metadata:
        geo = metadata['geoLocations']
        for g in geo:
            if 'geoLocationBox' in g:
                box = g['geoLocationBox']
                lat=[box['northBoundLatitude'],box['northBoundLatitude'],box['southBoundLatitude'],box['southBoundLatitude']]
                lon=[box['eastBoundLongitude'],box['westBoundLongitude'],box['eastBoundLongitude'],box['westBoundLongitude']]
                tlon,tlat = transform(from_proj,to_proj,lon,lat)
                pt_lat=pt_lat+tlat
                pt_lon= pt_lon+tlon
                iden = []
                auth = []
                t = []
                y = []
                for i in range(4):
                    iden.append(metadata['identifier']['identifier'])
                    auth.append(metadata['creators'][0]['creatorName'])
                    t.append(metadata['titles'][0]['title'].split(':')[0])
                    y.append(metadata['publicationYear'])
                identifier=identifier+iden
                author=author+auth
                title=title+t
                year = year+y
                #Write box edges
                x0 = x0 + [tlon[0],tlon[2],tlon[0],tlon[1]]
                x1 = x1 + [tlon[1],tlon[3],tlon[2],tlon[3]]
                y0 = y0 + [tlat[0],tlat[2],tlat[0],tlat[1]]
                y1 = y1 + [tlat[1],tlat[3],tlat[2],tlat[3]]
            if 'geoLocationPoint' in g:
                point = g['geoLocationPoint']
                print(point)
            if 'geoLocationPlace' in g:
                place = g['geoLocationPlace']
                print(place)

source = ColumnDataSource(
    data=dict(pt_lat=pt_lat,pt_lon=pt_lon,identifier=identifier,x0=x0,x1=x1,y0=y0,y1=y1,title=title,author=author,year=year))
#print(source.data)
circle = Circle(x="pt_lon", y="pt_lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
fig.add_glyph(source, circle) 

segment =\
    Segment(x0="x0",y0="y0",x1="x1",y1="y1",line_color="blue",line_width=3)
fig.add_glyph(source, segment)

open_url = CustomJS(args=dict(source=source), code="""
source.inspected._1d.indices.forEach(function(index) {
    var name = source.data["identifier"][index];
    var url = "https://doi.org/" + encodeURIComponent(name);
    window.open(url);
});
""")

fig.add_tools(TapTool(callback=open_url, behavior="inspect"))

output_file("stamen_toner_plot.html")
show(fig)
