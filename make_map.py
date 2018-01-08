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
    ("Thesis", "@identifier"),
    ("Thesis", "@identifier"),
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
                for i in range(4):
                    iden.append(metadata['identifier']['identifier'])
                identifier=identifier+iden
                #source = ColumnDataSource(
                #   data=dict(
                #        lat=tlat,
                #        lon=tlon,
                #        )
                #)
                #circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
                #fig.add_glyph(source, circle) 
                #source = ColumnDataSource(
                #   data=dict(x0=[tlon[0]],y0=[tlat[0]],x1=[tlon[1]],y1=[tlat[1]])
                #)
                #segment =\
                        #Segment(x0="x0",y0="y0",x1="x1",y1="y1",line_color="blue",line_width=3)
                #fig.add_glyph(source, segment)
                #source = ColumnDataSource(
                #   data=dict(x0=[tlon[2]],y0=[tlat[2]],x1=[tlon[3]],y1=[tlat[3]])
                #)
                #segment =\
                        #Segment(x0="x0",y0="y0",x1="x1",y1="y1",line_color="blue",line_width=3)
                #fig.add_glyph(source, segment)
                #source = ColumnDataSource(
                #   data=dict(x0=[tlon[0]],y0=[tlat[0]],x1=[tlon[2]],y1=[tlat[2]])
                #)
                #segment =\
                        #Segment(x0="x0",y0="y0",x1="x1",y1="y1",line_color="blue",line_width=3)
                #fig.add_glyph(source, segment)
                #source = ColumnDataSource(
                #   data=dict(x0=[tlon[1]],y0=[tlat[1]],x1=[tlon[3]],y1=[tlat[3]])
                #)
                #segment =\
                        #Segment(x0="x0",y0="y0",x1="x1",y1="y1",line_color="blue",line_width=3)
                #fig.add_glyph(source, segment)
            if 'geoLocationPoint' in g:
                point = g['geoLocationPoint']
                print(point)
            if 'geoLocationPlace' in g:
                place = g['geoLocationPlace']
                print(place)



source = ColumnDataSource(
    data=dict(pt_lat=pt_lat,pt_lon=pt_lon,identifier=identifier))
print(source.data)
circle = Circle(x="pt_lon", y="pt_lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
fig.add_glyph(source, circle) 

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
