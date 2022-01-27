# Program wxwarning
# by Todd Arbetter (todd.e.arbetter@gmail.com)
# Software Engineer, IXMap, Golden, CO

# collects latests National Weather Service Warnings, Watches, Advisories,
# and Statements, plots shapefiles on an interactive map in various colors.
# The map is able to pan and zoom, and on mouseover will give the type of
# weather statement, start, and expiry.

import folium as fl
from folium.plugins import MiniMap




def make_map():
    #print("in make weather map")
    #print(weather_df.head(2))
    # weather_df - shape files with weather warnings
    # map_path - path to file with generated weather map, ie .html file

    # get the current time in UTC (constant reference timezone)
    
    # Use branca.colormap instead of choropleth
    # augment df with color features
    
    mbr = fl.Map(location=[40.0,-95.0],zoom_start=4,tiles="Stamen Toner")

    
    MiniMap(tile_layer='stamenterrain',zoom_level_offset=-5).add_to(mbr)
    #print("after map title")
    html_string = mbr.get_root().render()
    #vars['map_html'] = html_string
    return html_string


    
    




