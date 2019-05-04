import tensorflow as tf
import tensorflow_hub as hub
from tqdm import tqdm
import numpy as np
import warnings
warnings.filterwarnings("ignore")
def elmoise(string):
	elmo = hub.Module("https://tfhub.dev/google/elmo/2")
	embeddings = elmo([string], signature = 'default', as_dict = True)['default']
	sess = tf.Session()
	sess.run(tf.global_variables_initializer())
	E = sess.run(embeddings) # I could have put a placeholder for X and feed dict
	return(E[0])

def elmoiser(strArray):
	E = []
	elmo = hub.Module("https://tfhub.dev/google/elmo/2")
	x = tf.placeholder(dtype=tf.string, shape = (1,))
	embeddings = elmo(x, signature = 'default', as_dict = True)['default']
	sess = tf.Session()
	sess.run(tf.global_variables_initializer())
	for string in tqdm(strArray):
		E += [sess.run(embeddings, feed_dict={x: [string]})] # I could have put a placeholder for X and feed dict
	return(np.array(E))