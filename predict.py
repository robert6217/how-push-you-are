import random
import requests
import numpy as np
from PIL import Image
from keras.models import load_model
SIZE = 32
label_dict = {
	0: '0to35',
	1: '36to70',
	2: '71to100'
}

def howPush(pictureURL, userID):
	
	model = load_model('hdf5/ptt_buaty.h5')
	res = requests.get(pictureURL)
	open(userID + '.jpg', 'wb').write(res.content)
	img       = Image.open(userID + '.jpg')
	img32by32 = img.resize((SIZE, SIZE), Image.BILINEAR)
	imgary    = np.array(img32by32, dtype=np.float)
	imgary    = imgary.reshape(1, SIZE, SIZE, 3).astype('float32')/255
	Predicted_Peobability = model.predict(imgary)
	prediction            = model.predict_classes(imgary)
	
	if prediction[0] == 0:
		push = random.randint(0, 35)
	elif prediction[0] == 1:
		push = random.randint(36, 70)
	else:
		push = random.randint(71, 150)
		if push > 100:
			push = '爆'
	data = {
		'push': push,
		'prediction': prediction[0],
		'Predicted_Peobability': Predicted_Peobability
	}
	return data