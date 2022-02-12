from functools import wraps, update_wrapper
import os as os
import datetime as dt
from datetime import datetime
from flask import Flask, render_template, render_template_string, redirect, send_file, make_response
#from flask import jsonify
#from make_map import make_map 
from weather_data import  get_weather_data
from weather_map import make_weather_map 
#import geopandas as gpd
#import pandas as pd

application = Flask(__name__)

application.config['TEMPLATES_AUTO_RELOAD'] = True
application.vars = {}
cwd = os.getcwd()

lpath = os.path.join(cwd, 'static/img/logo.png' )
application.vars['logo_path'] = lpath


# Set up cache headers and directives
def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)


@application.route('/')
def main():
    return redirect('/index.html')

#  Define the index route: GET 

@application.route('/index.html', methods=['GET'])
def index():
    
    # Get weather data (geopandas dataframe)
    weather_df =  get_weather_data()

    if weather_df is None:
        return redirect('/dataerror.html')

    # Create the map

    map_html = make_weather_map(weather_df)
    
    #print("in maps")
    #map_html = make_map()
    if map_html is None:
        print("map not saved")
        return redirect('/maperror.html')
    application.vars['map_html'] = map_html  
    # get the current time in UTC (constant reference timezone)
    
    application.vars['Title_line1'] = 'Current U.S. Weather Statements '
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec='minutes')
    print(timestamp)
    application.vars['Title_line2'] = timestamp[0:10]+' '+timestamp[11:16]+' UTC'
    return render_template('display.html', vars=application.vars)

 

@application.route('/maps/map.html')
@nocache
def show_map():
    # return the map "string" to the display templateß
    print("show map")
    return render_template_string(application.vars['map_html'])
  


@application.route('/get_logo')
def get_logo():

    # return the logo png to the browser
    logo_path = application.vars.get("logo_path")
    if os.path.exists(logo_path):
        return send_file(logo_path)
    else:
        return render_template('error.html', culprit='logo file', details="the logo file couldn't be loaded")

      
@application.route('/error.html')
def error():
    details = "There was some kind of error."
    return render_template('error.html', culprit='logic', details=details)

@application.route('/apierror.html')
def apierror():
    details = "There was an error with one of the API calls you attempted."
    return render_template('error.html', culprit='API', details=details)

@application.route('/maperror.html')
def maperror():
    details = "Map not found."
    return render_template('error.html', culprit='the Map', details=details)

@application.route('/dataerror.html')
def dataerror():
    details = "Data not available or timed out while fetching."
    return render_template('error.html', culprit='the Map', details=details)



if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
