import requests
from caltechdata_api import decustomize_schema
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.palettes import brewer
from bokeh.tile_providers import STAMEN_TERRAIN
from bokeh.models import (
  CustomJS, TapTool, ColumnDataSource, Circle, Range1d, PanTool,
WheelZoomTool, BoxSelectTool, Segment, HoverTool, Legend, OpenURL
)
from pyproj import Proj, transform
from jinja2 import Template

url = 'https://data.caltech.edu/api/records'

response = requests.get(url+'/?size=1000&q=subjects:"thesis"+"gps"')
hits = response.json()

hover = HoverTool(tooltips=[
    ("Title", "@title"),
    ("Author", "@author"),
    ("Year", "@year"),
])

fig =\
figure(tools=[hover,'zoom_in','zoom_out','wheel_zoom','pan','undo','redo','help'], active_scroll='wheel_zoom',\
        plot_height=500, plot_width=1000)
fig.axis.visible = False
fig.add_tile(STAMEN_TERRAIN)

# transform lng/lat to meters
from_proj = Proj(init="epsg:4326")
to_proj = Proj(init="epsg:3857")

print("Number of records: ",len(hits['hits']['hits']))

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
color=[]
palette = brewer['Spectral'][11]
lkey =\
["1920's","1930's","1940's","1950's","1960's","1970's","1980's","1990's","2000's","2010's","2020's"]

for h in hits['hits']['hits']:
    print("Adding record: ",h['id'])
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
                cen = metadata['publicationYear'][1]
                dec = metadata['publicationYear'][2]
                if cen == '9':
                    clo = palette[int(dec)-2]
                    #First color is 1920
                if cen == '0':
                    clo = palette[int(dec)+8]
                #We duplicate metadata for every point
                for i in range(4):
                    identifier.append(metadata['identifier']['identifier'])
                    author.append(metadata['creators'][0]['creatorName'])
                    title.append(metadata['titles'][0]['title'].split(':')[0])
                    year.append(metadata['publicationYear'])
                    color.append(clo)
                x0 = x0 + [tlon[0],tlon[2],tlon[0],tlon[1]]
                x1 = x1 + [tlon[1],tlon[3],tlon[2],tlon[3]]
                y0 = y0 + [tlat[0],tlat[2],tlat[0],tlat[1]]
                y1 = y1 + [tlat[1],tlat[3],tlat[2],tlat[3]]
            if 'geoLocationPoint' in g:
                point = g['geoLocationPoint']
                tlon,tlat =\
                transform(from_proj,to_proj,point['pointLongitude'],point['pointLatitude'])
                pt_lat=pt_lat+[tlat]
                pt_lon= pt_lon+[tlon]
                identifier=identifier+[metadata['identifier']['identifier']]
                author=author+[metadata['creators'][0]['creatorName']]
                title=title+[metadata['titles'][0]['title'].split(':')[0]]
                year = year+[metadata['publicationYear']]
                cen = metadata['publicationYear'][1]
                dec = metadata['publicationYear'][2]
                if cen == '9':
                    clo = palette[int(dec)-2]
                    #First color is 1920
                if cen == '0':
                    clo = palette[int(dec)+8]
                color.append(clo)
                #Useless data so all fields are complete
                x0 = x0 + [tlon]
                x1 = x1 + [tlon]
                y0 = y0 + [tlat]
                y1 = y1 + [tlat]
            #Don't know what to do with just place names
            #if 'geoLocationPlace' in g:
            #    place = g['geoLocationPlace']

source = ColumnDataSource(
    data=dict(pt_lat=pt_lat,pt_lon=pt_lon,identifier=identifier,x0=x0,x1=x1,y0=y0,y1=y1,\
            title=title,author=author,year=year,color=color))
segment =\
    Segment(x0="x0",y0="y0",x1="x1",y1="y1",line_color="color",line_width=3)
fig.add_glyph(source, segment)
    
circle = Circle(x="pt_lon",\
        y="pt_lat",size=8,fill_color="color")
fig.add_glyph(source, circle) 

url = "https://doi.org/@identifier"
fig.add_tools(TapTool(callback=OpenURL(url=url)))
items = []
#Dummy points for legend
for i in range(len(lkey)):
    circle = Circle(x=0,y=0,fill_color=palette[i],size=0,line_color=None)
    render = fig.add_glyph(circle)
    items.append((lkey[i],[render]))
legend = Legend(items = items, location=(0,0), orientation="horizontal") 
fig.add_layout(legend,'below')

infile = open('tem.html','r')
tem = infile.read()
template = Template(tem)
file_done = file_html(fig, CDN, "CaltechDATA Map",template)
outfile = open("caltechdata_map.html",'w')
outfile.write(file_done)
