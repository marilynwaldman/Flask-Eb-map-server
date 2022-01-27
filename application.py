from functools import wraps, update_wrapper
import os as os
import datetime as dt
from datetime import datetime
#from xmlrpc.client import APPLICATION_ERROR
from flask import Flask, render_template, render_template_string, request, redirect, url_for, send_file, make_response
from flask import jsonify
from make_map import make_map 

application = Flask(__name__)

application.config['TEMPLATES_AUTO_RELOAD'] = True
application.vars = {}
cwd = os.getcwd()

logo_path = os.path.join(cwd, 'static/img/logo.png' )
application.vars['logo_path'] = logo_path


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

@application.route("/echo/<name>")
def echo(name):
    print(f"This was placed in the url: new-{name}")
    val = {"new-name": name}
    return jsonify(val)

@application.route('/index.html', methods=['GET'])
def index():
    print(f"in maps")
    map_html = make_map()
    if map_html is None:
      print("map not saved")
      return redirect('/maperror.html')
    application.vars['map_html'] = map_html  
    # get the current time in UTC (constant reference timezone)
    
    application.vars['Title_line1'] = 'Current U.S. Weather Statements - 2nd'
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec='minutes')
    print(timestamp)
    application.vars['Title_line2'] = timestamp[0:10]+' '+timestamp[11:16]+' UTC'
    return render_template('display.html', vars=application.vars)

 

@application.route('/maps/map.html')
@nocache
def show_map():
  print("show map")
  return render_template_string(application.vars['map_html'])
  


@application.route('/get_logo')
def get_logo():
  #print("in get logo")
  #logo_path = os.path.join(server.root_path, 'static/img/logo.png' )
  logo_path = application.vars.get("logo_path")
  #logo_file = Path(logo_path)
  #print(logo_path)
  if os.path.exists(logo_path):
    #print("logo found")
    return send_file(logo_path)
  else:
    return render_template('error.html', culprit='logo file', details="the logo file couldn't be loaded")
      


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
