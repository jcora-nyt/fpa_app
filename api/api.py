from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

@app.route("/routes/<int:route_id>/", methods=['GET'])
def route_detail(route_id):
    response = {
    	"meta": {
    		"num_records": 0,
    		"route_id": route_id
    	},
    	"data": {
	    	"customers": [
				{
					"name": "",
					"address": "",
					"city": "",
					"state": "",
					"zip": "",
					"geo": {
						"lat": 41.52,
						"lng": -71.61
					},
					"escalation": {
						"type": "STANDARD",
						"level": 2,
						"status": "OPEN",
						"product": "DS",
						"complaint": "WP"
					}
				}
			]
		}
	}

    return response

if __name__ == "__main__":
    app.run('10.51.236.201', debug=True)
