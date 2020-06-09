from django.shortcuts import render

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import urllib.request
from PIL import Image

from .models import CurrentAlbum
# Create your views here.

def top(request):


	client_credentials_manager = SpotifyClientCredentials(client_id='af04cdfc9d6648f892f7d8c0bc8c9121', client_secret='2421f982963b4f628eae9c06f1e610a9')
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	playlists = sp.user_playlists('bilalyousuf')

	# collect my 3 most recently created playlists
	three_playlists = playlists['items'][:3]

	#cycling through 3 album data models to update
	for i in range(3):
		# specify the model
		model = CurrentAlbum.objects.get(id=i+1)
		#get the first track from this playlist
		track = sp.playlist_tracks(three_playlists[i]['uri'], offset=0, limit=1)
		#album title
		model.title = track['items'][0]['track']['album']['name']
		#album artist
		model.artist = track['items'][0]['track']['album']['artists'][0]['name']
		#img url
		model.img_url = track['items'][0]['track']['album']['images'][0]['url']
		#external url
		model.external_url = track['items'][0]['track']['album']['external_urls']['spotify']

		#save changes
		model.save()
	queryset = CurrentAlbum.objects.all()


	context = {
		'queryset': queryset
		        
	}

    # Render the HTML template index.html with the data in the context variable
	return render(request, 'top-albums.html', context=context)
