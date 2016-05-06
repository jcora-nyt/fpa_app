import mysql.connector
import geocoder

cnx = mysql.connector.connect(user='root', password='root', host='localhost', database='cis_delivery')

q_cursor = cnx.cursor(buffered=True)
u_cursor = cnx.cursor(buffered=True)

query = ('SELECT id, name, address_line1, zip FROM cis_subscriber WHERE lat IS NULL')

q_cursor.execute(query)

for (rec_id, name, address_line1, zip) in q_cursor:
	print(name + '|' + address_line1 + '|' + zip)

	g = geocoder.google(address_line1 + ', ' + zip)

	if 'geometry' in g.geojson:
		geometry = g.geojson['geometry']

		if geometry['type'] == 'Point':
			update = ('UPDATE cis_subscriber SET lat = ' + str(geometry['coordinates'][0]) + ', lng = ' + str(geometry['coordinates'][1]) + ' WHERE id = ' + str(rec_id))
			
			u_cursor.execute(update)

q_cursor.close()
u_cursor.close()

cnx.commit()

cnx.close()