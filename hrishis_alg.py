import requests, json
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty
import imp

##Global Variables and Constants##
api_key = "AIzaSyB2INeLjmXDX54ePAm__6mwOU96R2UsUvw"

##Initialization Code##
geolocator = GoogleV3()

##Function Body##

def call_api(url):
	"""
	Internal function for making API Calls.

	Args:
		url (String) - valid http post request.

	Returns:
		Results of the request. No exception handling. No direct calls.
	"""
	return json.loads(requests.get(url).content)

def add2latlon(address):
	"""
	Geocoding function.

	Args:
		address (String): lookup address.

	Returns:
		Location: Contains latitude and longitude of the address.
		Location.raw: Contains JSON data about the place, including place_id which can be used for other lookups.
	"""
	return geolocator.geocode(address)

def lookupAdd(address):
	"""
	Wrapper for add2latlon.

	Args:
		address (String): lookup address;

	Returns:
		String: place_id for the address from Google API.
	"""
	return add2latlon(address).raw['place_id']

def lookupLatLon(lat, lon):
	"""
	Wrapper for latlon2add.

	Args:
		lat (int): latitude
		lon (int): longitude

	Returns:
		String: place_id for the coordinates specified.
	"""
	return latlon2add(lat,lon)[0].raw['place_id']

def latlon2add(lat, lon):
	"""
	Reverse Geocoding function.

	Args:
		lat (double): latitude
		lon (double): longitude

	Returns:
		Location[]: Contains all locations that match the reverse geocoding request.
	"""	
	latlon = str(lat)+","+str(lon)
	return geolocator.reverse(latlon)

def routePlanner(locations, start, end):
	
	s = ""
	e = ""
	if isinstance(start, str):
		tmp = add2latlon(start)
		s = "lat:%f,lon:%f" % (tmp[1][0],tmp[1][1])
	else:
		s = "lat:%f,lon:%f" % (start[0],start[1])
	if isinstance(end, str):
		tmp = add2latlon(end)
		e = "lat:%f,lon:%f" % (tmp[1][0],tmp[1][1])
	else:
		e = "lat:%f,lon:%f" % (end[0],end[1])

	api_string = "https://maps.googleapis.com/maps/api/directions/json?key=%s&origin=%s&destination=%s" % (api_key,s,e)

	if len(locations) <= 0:
		return call_api(api_string)

	api_string += "&waypoints=optimize:true"	

	for location in locations:
		if isinstance(location, str):
			tmp = add2latlon(location)
			api_string += "|lat:%f,lon:%f" % (tmp[1][0],tmp[1][1])
		else:
			api_string += "|lat:%f,lon:%f" % (location[0],location[1])

	return call_api(api_string)


##Testing Code##
if __name__ == '__main__':
	print(add2latlon("Toronto,Canada")[1][1])