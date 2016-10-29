# coding: utf-8
import httplib2 # http client library
import json # converting in-memory python objects into json
import sys
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stdout)


client_id = "AYK0HLOF0SGPJGKMDWJDXBWN2VE55DY2UIH1UV4CF0TXRJC4"
client_secret = "Y31ZKBXCOICMWNY1LCRT4G5DS2TTY14TII0P4HR3PMEGH3PN"
google_api_key = "AIzaSyANbOmmApPNwoUOJ_u1q4MnohifOsMAO9A"


def get_geocode_location(inputString):
	global google_api_key
	google_api_key = "AIzaSyANbOmmApPNwoUOJ_u1q4MnohifOsMAO9A"
	locationString = inputString.replace(" ", "+")
	url = ("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (locationString, google_api_key))
	h = httplib2.Http()
	response, content = h.request(url, 'GET')
	result_data = json.loads(content)
	lat, lng = result_data['results'][0]['geometry']['location'].values()

	return (lat, lng)


def findARestaurant(mealType, location):
	global client_id
	global client_secret
	print get_geocode_location(location)
	lat, lng = get_geocode_location(location)

	"""
	lat, lng = get_geocode_location(location)
  File "/Users/JMHong/Documents/Python/REST_APIs/restaurant_features/restaurant_image_finder.py", line 24, in get_geocode_location
    lat, lng = result_data['results'][0]['geometry']['location'].values()
IndexError: list index out of range
	"""

	foursquare_url = "https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s" % (client_id, client_secret, lat, lng, mealType)
	h = httplib2.Http()
	response, content = h.request(foursquare_url, 'GET')
	api_data = json.loads(content)

	if api_data['response']['venues']:
		restaurant = api_data['response']['venues'][0]
		venue_id = restaurant['id']
		restaurant_name = restaurant['name']
		restaurant_address = restaurant['location']['formattedAddress']
		address = ""
		for i in restaurant_address:
			address += i + " "
		restaurant_address = address

		url = 'https://api.foursquare.com/v2/venues/{}/photos?client_id={}&v=20150603&client_secret={}'.format(
			  venue_id, client_id, client_secret)

		content_str = h.request(url, 'GET')[1]
		content = json.loads(content_str)

		if content['response']['photos']['items']:
			content = content['response']['photos']['items'][0]
			prefix = content['prefix']
			suffix = content['suffix']
			image_url = prefix + '300x300' + suffix
		else:
			# else input random image of burger
			image_url = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"

		restaurant_info = {'name': restaurant_name, 'address': restaurant_address, 'image': image_url}
		print "Restaurant Name: %s" % restaurant_info['name']
		print "Restaurant Address: %s" % restaurant_info['address']
		print "Image: %s" % restaurant_info['image']
		return restaurant_info

	else:
		return "No Restaurants Found"


restaurants = {"Pizza": "Tokyo, Japan",
			   "Tacos": "Jakarta, Indonesia",
			   "Tapas": "Maputo, Mozambique",
			   "Falafel": "Cairo, Egypt",
			   "Spaghetti": "New Delhi, India",
			   "Cappuccino": "Geneva, Switzerland",
			   "Sushi": "Los Angeles, California",
			   "Steak": "La Paz, Bolivia",
			   "Gyros": "Sydney, Australia"}

if __name__ == "__main__":
	for k, v in restaurants.iteritems():
		print findARestaurant(k, v)