from __future__ import division

import datetime
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView

from models import Crime

# http://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
def dict_max(d):
	k = list(d.keys())
	v = list(d.values())

	if len(v) <= 0:
		return 0
	return k[v.index(max(v))]

radius = 1
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

class Home(View):
	template_name = "home.html"

	def get(self, *args, **kwargs):
		lat = 43.044689399999996
		lng = -76.1495647
		hour = 11#datetime.datetime.now().hour #1
		context = {
			"safety_score" : 100 - round(safety_score(lat, lng, hour) * 100, 1),
			"likely_crime" : dict_max(likely_crime(lat, lng, hour)),
		}

		return render(self.request, self.template_name, context)

class HeatMap(View):
	def get(self, *args, **kwargs):
		context = {
			"crimes" : Crime.objects.all()
		}

		#return render(self.request, "heat_map.html", context)
		return render(self.request, "map.html", context)

class Stats(TemplateView):
	template_name = "stats.html"

class About(TemplateView):
	template_name = "about.html"

class FAQ(TemplateView):
	template_name = "faq.html"
