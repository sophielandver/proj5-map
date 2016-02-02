"""
Very Flask web site displaying a map. 

"""

import flask
from flask import render_template
from flask import request
from flask import url_for

import json
import logging


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG


import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
  
    list_list = []
    file = open("POI.txt", "r")
    for line in file:
        line = line.rstrip()
        list_split = line.split(" ", 2)
        list_list.append(list_split) #have list of lists
   
    POI ={} #dictionary of desc:[lat, long]
    for line in list_list:
        desc = line[2]
        lat = float(line[0])
        long = float(line[1])
        POI[desc] = [lat, long]
    
    flask.session['POI'] = POI 
    return flask.render_template('map.html') 


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("index")
    return flask.render_template('page_not_found.html'), 404




#############
#    
# Set up to run from cgi-bin script, from
# gunicorn, or stand-alone.
#


if __name__ == "__main__":
    # Standalone, with a dynamically generated
    # secret key, accessible outside only if debugging is not on
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    if app.debug: 
        print("Accessible only on localhost")
        app.run(port=CONFIG.PORT)  # Accessible only on localhost
    else:
        print("Opening for global access on port {}".format(CONFIG.PORT))
        app.run(port=CONFIG.PORT, host="0.0.0.0")
else:
    # Running from cgi-bin or from gunicorn WSGI server, 
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service. 
    app.secret_key = CONFIG.secret_key
    app.debug=False