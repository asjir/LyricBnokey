import sys
from sklearn.externals.joblib import load
import numpy as np
from back.artistname_to_lyricsid import find
from back.elmoise import elmoiser
import warnings
import requests
warnings.filterwarnings("ignore")
args = sys.argv
nbrs = load('./back/nbrs.joblib')
# With a larger dataset annoy might be necessary but seems like an overkill here. Not that ELMo doesn't. 
svd = load('./back/svd.joblib')
url = 'https://api.musixmatch.com/ws/1.1/'
apikey = 'd8eaef84c24b7217a5ec54158eacd213'.encode('utf-8') 


if(len(args)<3):
	print('Usage: recommend.py \'artist 1\' \'song 1\' [\'artist 2\' \'song 2\' ...]\nwhere artist1 song1 is the last track listened to\nAnd the remaining ones are recommendations to choose from.\nIf only first pair is given it matches against songs already in the database.')
assert(len(args)>2)
if len(args)==3:
	listened_to = args[1], args[2]
	lyr, trid = find(listened_to[0], listened_to[1])
	lyr=' '.join(lyr.replace('\n', ' ').split(' ')[:-12])
	elmoisedlyr = elmoiser([lyr])
	elmoisedlyr = elmoisedlyr.reshape((1,1024))
	lyrArr = elmoisedlyr
	distances, indices = nbrs.kneighbors(lyrArr)
	# two cases either its just in the set and:
	if distances[0,0]<0.01:
		resindex = indices[1]
	else:
		resindex = indices[0]
	print(distances[0,0])
	#Only lookup left:
	lookup = np.load('./back/allyrics.npy')
	resid = lookup[resindex, 1]
	restrack = requests.get(url+'track.get', {'apikey':apikey, 'track_id':resid}).json()['message']['body']['track']
	print(lyrArr)
	print(restrack['track_name'], ' by ', restrack['artist_name'])

if len(args)>4:
	lyrs=[]
	l = []
	for i in range(len(args)//2):
		try:
			lyr, trid = find(args[i*2+1],args[i*2+2])
		except:
			continue
		
		lyr=' '.join(lyr.replace('\n', ' ').split(' ')[:-12])
		
		l+=[(args[i*2+1],args[i*2+2])]
		lyrs+=[lyr]
	elmoisedlyrs = elmoiser(lyrs)
	elmoisedlyrs = elmoisedlyrs.reshape((-1,1024))
	lyrs = elmoisedlyrs
	# Pick the closes one:
	listened_to = lyrs[0]
	candidates = lyrs[1:]
	# I'll just do it explicitely:
	from sklearn.metrics import mean_squared_error as mse # l2 distance
	d_min = 1000000 # since data is scaled it's safe
	for candidate in candidates:
		d_new = mse(listened_to, candidate)
		if d_new<d_min:
			d_min=d_new
	j=0
	print("Found data for: ", l)
	for candidate in candidates:
		j+=1
		print(mse(listened_to, candidate))
		if mse(listened_to, candidate)==d_min:
			print('Recommendation ', l[j])
	
		