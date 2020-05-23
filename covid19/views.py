from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.


def thousands_separated(number):
	"""Separate an integer with thousands commas for presentation."""
	return f"{number:,}"

def isolate_integers(string):
	"""Isolate positive integers from a string, returns as a list of integers."""
	return [int(s) for s in string.split() if s.isdigit()]


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


def quebec_tracker(request):
    """View function for Quebec tracker site."""

    count_cbc  = scrape_cbc()
    confirmed_cases_cbc = thousands_separated(count_cbc[0])
    deaths_cbc = thousands_separated(count_cbc[1])


    context = {
        'confirmed_cases_cbc': confirmed_cases_cbc,
        'deaths_cbc': deaths_cbc
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'quebec_tracker.html', context=context)
