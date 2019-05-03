import requests
url = 'https://api.musixmatch.com/ws/1.1/'
apikey = 'd8eaef84c24b7217a5ec54158eacd213'.encode('utf-8')
def find(artist, song):
	trid = requests.get(url+'track.search', {'apikey':apikey, 'q_artist':artist.encode('utf-8'), 'q_track':song.encode('utf-8')}).json()['message']['body']['track_list'][0]['track']['track_id']
	debugging = requests.get(url+'track.lyrics.get', {'apikey':apikey, 'track_id':trid}).json()['message']['body']
#	print(debugging)
	lyrics = debugging['lyrics']
	lyrics = lyrics['lyrics_body']
#	print(lyrics) # I think I got a completely missed error here
	return(lyrics,trid)
