from flask import request, url_for
from flask.ext.api import FlaskAPI
#import mysql.connector

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


# Setup Flask API and use custom JSON encoder for decimal issue
app = FlaskAPI(__name__)
app.config['DEBUG'] = True

@app.route("/routes/", methods=['GET', 'OPTIONS'])
def routes():
	# Loop through the routes and populate each route
	routes = []

	for (route_id, name) in q_cursor:
		# Add route information and add to routes list
		route = {
			"id": route_id,
			"name": name
		}

		routes.append(route)

	# Process response and return
	response = {
		"meta": {
			"num_records": len(routes)
		},
		"data": {
			"routes": routes
		}
	}

	return response
