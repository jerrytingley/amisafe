from __future__ import division

import math
import datetime
from django.db import models

# AIzaSyAddPpyvjA4e-et6awgS1heNX9C6zC-6V4
class Crime(models.Model):
	crime_type = models.CharField(max_length=56)
	address = models.CharField(max_length=256)
	city = models.CharField(max_length=128)
	department = models.CharField(max_length=128)
	date_time = models.DateTimeField()
	latitude = models.FloatField(null=True, blank=True)
	longitude = models.FloatField(null=True, blank=True)

	def haversine(self, other_crime):
		R = 3961

		lat1 = math.radians(self.latitude)
		lat2 = math.radians(other_crime.latitude)
		lng1 = math.radians(self.longitude)
		lng2 = math.radians(other_crime.longitude)
		
		d_lng = lng2 - lng1 
		d_lat = lat2 - lat1 
		a = (math.sin(d_lat / 2)**2) + math.cos(lat1) * math.cos(lat2) * (math.sin(d_lng / 2)**2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
		d = R * c

		return d


	def haversine(self, lat2, lng2):
		R = 3961

		lat1 = math.radians(self.latitude)
		lat2 = math.radians(lat2)
		lng1 = math.radians(self.longitude)
		lng2 = math.radians(lng2)
		
		d_lng = lng2 - lng1 
		d_lat = lat2 - lat1 
		a = (math.sin(d_lat / 2)**2) + math.cos(lat1) * math.cos(lat2) * (math.sin(d_lng / 2)**2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
		d = R * c

		return d
