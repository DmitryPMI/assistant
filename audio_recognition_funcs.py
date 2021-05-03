import numpy as np
import librosa
from tensorflow import keras
import requests
import os


emotion_list = ['Angry', 'Disgusted', 'Domination', 'Happy', 'Neutral', 'Sad', 'Scared', 'Shame', 'Submission', 'Surprised', 'Tiredness']

def features_extractor(audio): 
    mfccs_features = librosa.feature.mfcc(y=audio, sr=22050, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    return mfccs_scaled_features


def get_emotion_from_audio(audio):
	r = requests.get('https://storage.yandexcloud.net/assistant-bot-bucket/saved_models/my_model_1.hdf5', allow_redirects=True)
	with open('test.hdf5', 'wb') as f:
		f.write(r.content)
	model = keras.models.load_model('test.hdf5')
	try:
		audio = np.fromstring(audio, dtype=np.int16)
	except:
		audio = np.fromstring(audio[:-1], dtype=np.int16)
	audio =  audio / np.linalg.norm(audio)
	features = features_extractor(audio)
	os.remove('test.hdf5')
	prediction = model.predict(np.array([features]))[0]
	prediction =  prediction / np.linalg.norm(audio)
	return emotion_list[np.argmax(prediction)]