from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions
from accessControl import crossdomain
import mysql.connector

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


# Setup Flask API and use custom JSON encoder for decimal issue
app = FlaskAPI(__name__)

@app.route("/routes/", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def routes():
	# Create DB connection
	cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='cis_delivery')

	# Create DB cursor
	q_cursor = cnx.cursor(buffered=True)

	# Generate and perform query on DB to get routes
	query = ('SELECT id, name FROM route')

	q_cursor.execute(query)

	# Loop through the routes and populate each route
	routes = []

	for (route_id, name) in q_cursor:
		# Add route information and add to routes list
		route = {
			"id": route_id,
			"name": name
		}

		routes.append(route)

	# Cleanup DB stuff
	q_cursor.close()
	cnx.close()

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

@app.route("/routes/<int:route_id>/", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def route_detail(route_id):
	# Create DB connection
	cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='cis_delivery')

	# Create DB cursor
	q_cursor = cnx.cursor(buffered=True)

	# Generate and perform query on DB to get routes
	query = ('SELECT cs.id, name, address_line1, city, state, zip, phone_home, lat, lng, esc.id, type, level, status, product, complaint \
		FROM cis_subscriber cs INNER JOIN cis_subscriber_route csr ON cs.id = csr.cis_subscriber_id LEFT JOIN escalations esc ON cs.id = esc.cis_subscriber_id \
		WHERE route_id = ' + str(route_id))

	q_cursor.execute(query)

	# Loop through the customers and populate each customer
	customers = []

	for (customer_id, name, address, city, state, zip, phone, lat, lng, esc_id, esc_type, level, status, product, complaint) in q_cursor:
		# Populate escalation information first
		escalation = None

		if esc_id is not None:
			escalation = {
				"type": esc_type,
				"level": level,
				"status": status,
				"product": product,
				"complaint": complaint
			}

		# Add customer information and add to customers list
		customer = {
			"id": customer_id,
			"name": name,
			"address": address,
			"city": city,
			"state": state,
			"zip": zip,
			"phone_home": phone,
			"geo": {
				"lat": str(lat),
				"lng": str(lng)
			},
			"escalation": escalation
		}

		customers.append(customer)

	# Cleanup DB stuff
	q_cursor.close()
	cnx.close()

	# Process response and return
	response = {
		"meta": {
			"num_records": len(customers),
			"route_id": route_id
		},
		"data": {
			"customers": customers
		}
	}

	return response
