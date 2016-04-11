import datetime
import requests
import pytz
from django.core.management.base import BaseCommand, CommandError

from ...models import *

from pprint import pprint as pp

KEY = "AIzaSyAddPpyvjA4e-et6awgS1heNX9C6zC-6V4"
BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key=" + KEY
def geocode(address, city):
	address = address.replace(" ", "+")
	city = city.replace(" ", "+")
	q = "{0},{1},New York".format(address, city)
	r = requests.get(BASE_URL.format(q))
	
	return r.json()

# Returns one datatime object from a time and date string.
# If there's two times in the time string, it retrieves the first one
# and uses that as the time in the datetime.
def get_date_time(date, time):
	time = time.replace("p.m.", "PM")
	time = time.replace("a.m.", "AM")
	if "-" in time:
		time = time.split("-")[0]
	time = datetime.datetime.strptime(time, "%I:%M %p")
	date = datetime.datetime.strptime(date, "%m/%d/%Y")
	combined = datetime.datetime.combine(date.date(), time.time())

	return combined.replace(tzinfo=pytz.UTC)
	
csv_file = "crime_data.csv"
class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		csv_data = []
		with open(csv_file, 'r') as csv:
			csv_data = csv.read().split("\n")

		# crime,address,city,department,date,time
		csv_data = csv_data[1:]
		for line in csv_data:
			csv_line = line.split(",")
			print csv_line

			crime_type = csv_line[0]
			address = csv_line[1]
			city = csv_line[2]
			department = csv_line[-3]
			date = csv_line[-2]
			time = csv_line[-1]
			date_time = get_date_time(date, time)

			if not Crime.objects.filter(crime_type=crime_type, address=address, date_time=date_time).exists():
				coords = geocode(address, city)
				#pp(coords)
				if coords['status'] != 'ZERO_RESULTS':
					if len(coords['results']) > 1:
						coords = coords['results'][1]
					else:
						coords = coords['results'][0]
			
					latitude = coords['geometry']['location']['lat']
					longitude = coords['geometry']['location']['lng']

					crime = Crime.objects.create(crime_type=crime_type,
												 address=address,
												 city=city,
												 department=department,
												 date_time=date_time,
												 latitude=latitude,
												 longitude=longitude)
			else:
				print "Exists"
