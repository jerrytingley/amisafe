from __future__ import division

import datetime
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView

from django.core.management.base import BaseCommand, CommandError
from ...models import Crime

from pprint import pprint as pp

# http://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
def dict_max(d):
	k = list(d.keys())
	v = list(d.values())

	if len(v) <= 0:
		return 0
	return k[v.index(max(v))]

def crimes_freq(crimes):
	crime_type_freq = {}
	crime_address_freq = {}
	crime_hours_freq = {}
	crime_days_freq = {}

	for crime in crimes.all():
		crime_type = crime.crime_type
		address = crime.address
		crime_type_freq[crime_type] = crime_type_freq.get(crime_type, 0) + 1
		crime_address_freq[address] = crime_address_freq.get(address, 0) + 1
		crime_hours_freq[crime.date_time.hour] = crime_hours_freq.get(crime.date_time.hour, 0) + 1
		crime_days_freq[crime.date_time.day] = crime_days_freq.get(crime.date_time.day, 0) + 1

	crime_type_freq["max"] = dict_max(crime_type_freq)
	crime_address_freq["max"] = dict_max(crime_address_freq)
	crime_hours_freq["max"] = dict_max(crime_hours_freq)
	crime_days_freq["max"] = dict_max(crime_days_freq)

	return (crime_type_freq, crime_address_freq, crime_hours_freq, crime_days_freq)

radius = 0.5
def crimes_near_me(crimes, lat, lng):
	local_crimes = []
	for crime in crimes.all():
		if crime.haversine(lat, lng) <= radius:
			local_crimes.append(crime)
	return local_crimes

def safety_score(lat, lng, hour):
	crimes = Crime.objects.filter(date_time__hour=hour) #| Crime.objects.filter(date_time__hour=(hour-1)) | Crime.objects.filter(date_time__hour=(hour+1))
	
	overall_crime_count = crimes.count()
	local_crime_count = len(crimes_near_me(crimes, lat, lng))

	return local_crime_count/overall_crime_count

def likely_crime(lat, lng, hour):
	crime_freq = {}
	crimes = Crime.objects.filter(date_time__hour=hour) #| Crime.objects.filter(date_time__hour=(hour-1))
	for crime in crimes_near_me(crimes, lat, lng):
		crime_type = crime.crime_type
		crime_freq[crime_type] = crime_freq.get(crime_type, 0) + 1
	print crime_freq	
	return crime_freq

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		freqs = crimes_freq(Crime.objects.all())
		pp(freqs[0])
		pp(freqs[1])
		pp(freqs[2])
		pp(freqs[3])
