from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

from .models import Data

# Create your views here.


def thousands_separated(number):
	"""Separate an integer with thousands commas for presentation."""
	return f"{number:,}"

def isolate_integers(string):
	"""Isolate positive integers from a string, returns as a list of integers."""
	return [int(s) for s in string.split() if s.isdigit()]

def filter_digits(string):
	"""Returns the all digits concatonated sequentially in a string as a single integer value."""
	return ''.join(filter(lambda i: i.isdigit(), string)) 


def scrape_cbc():
	"""Scrapes CBC website to return list of two numbers: total confirmed cases and total deaths in Quebec."""
	url = "https://www.cbc.ca/news/canada/montreal/covid-19-quebec-may-20-1.5576506"
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	#exctract story class
	story = soup.find(class_="story")
	#grab subdivision html/css tags
	story = story.select("ul li")
	#first element in list
	story = story[0]
	#further isolate tagline we require
	story = story.select("strong")
	story = story[0]

	#convert to string
	string = str(story)

	#remove comma separation for int detection
	string = string.replace(',', '')

	count = isolate_integers(string)

	return count



def scrape_gov():
    url = "https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/#c51839"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #get total cases
    table = soup.find(id="c50214")
    row = table.find(class_="contenttable")
    row = row.select("tbody tr td p")[-1]
    row_int = int(filter_digits(str(row)))

    #last update
    last_update = table.find(class_="contenttable")
    last_update = last_update.select("thead tr th p")[-1]
    last_update = last_update.get_text().split()[5:]
    m = last_update[0] + ' '
    d = last_update[1] + ' '
    t = last_update[-2] + ' ' + last_update[-1]
    last_update = m + d + t


    # deaths
    deaths = soup.find(id="c51880")
    deaths = deaths.find(class_="contenttable")
    deaths = deaths.select("tbody tr td p")[-1]
    deaths = int(filter_digits(str(deaths)))
    
    return row_int, deaths, last_update




def quebec_tracker(request):
    """View function for Quebec tracker site."""

    #count_cbc  = scrape_cbc()
    #confirmed_cases_cbc = thousands_separated(count_cbc[0])
    #deaths_cbc = thousands_separated(count_cbc[1])
    confirmed_cases, deaths, last_update = scrape_gov()
    confirmed_cases = thousands_separated(confirmed_cases)
    deaths = thousands_separated(deaths)

    # add to database
    #avoid duplicates
    if Data.objects.filter(confirmed_cases__exact=confirmed_cases, total_deaths__exact=deaths).count()==0:
    	Data(confirmed_cases=confirmed_cases, total_deaths=deaths).save()




    context = {
        #'confirmed_cases_cbc': confirmed_cases_cbc,
        #'deaths_cbc': deaths_cbc
        'confirmed_cases': confirmed_cases,
        'deaths': deaths,
        'last_update': last_update,
        
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'quebec_tracker.html', context=context)
