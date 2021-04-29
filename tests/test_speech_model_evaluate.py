import requests
import numpy as np
import io
from tensorflow import keras
import os


def test_evaluate():
	''' If we inly save weights of the model, we dont need to save and delete file directly '''
	r = requests.get('https://storage.yandexcloud.net/assistant-bot-bucket/saved_models/x_test.npy', allow_redirects=True)
	X = np.load(io.BytesIO(r.content))
	r = requests.get('https://storage.yandexcloud.net/assistant-bot-bucket/saved_models/y_test.npy', allow_redirects=True)
	y = np.load(io.BytesIO(r.content))
	r = requests.get('https://storage.yandexcloud.net/assistant-bot-bucket/saved_models/my_model_1.hdf5', allow_redirects=True)
	with open('test.hdf5', 'wb') as f:
		f.write(r.content)
	model = keras.models.load_model('test.hdf5')
	result = model.evaluate(X, y)
	os.remove('test.hdf5')
	assert result[1] > 0.5 # accuracy score
	assert result[2] > 0.8 # AUC score

# test_evaluate()