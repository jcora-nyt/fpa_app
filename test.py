from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


# Setup Flask API and use custom JSON encoder for decimal issue
app = FlaskAPI(__name__)
app.config['DEBUG'] = True

print "Here I am, world!"