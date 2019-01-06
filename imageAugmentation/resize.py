import os
import sys
import numpy as np
import pandas as pd
from PIL import Image, ImageChops

paths     = 'C:\\Users\\Robert\\Google 雲端硬碟\\Colab Notebooks\\how-push-you-are\\face\\'
threepath = ['mark1\\', 'mark2\\']
width     = 64
height    = 64
mark0     = 'C:\\Users\\Robert\\Google 雲端硬碟\\Colab Notebooks\\how-push-you-are\\face\\32by32\\mark0\\'
mark1     = 'C:\\Users\\Robert\\Google 雲端硬碟\\Colab Notebooks\\how-push-you-are\\face\\32by32\\mark1\\'
mark2     = 'C:\\Users\\Robert\\Google 雲端硬碟\\Colab Notebooks\\how-push-you-are\\face\\32by32\\mark2\\'

for path in threepath:
	for files in os.listdir(paths + path):
		imgpath = paths + path + files
		if path == 'mark1\\':
			im200  = Image.open(imgpath).convert('RGB')
			try:
				newimg = im200.resize((width, height), Image.BILINEAR)
			except:
				pass
			else:
				newimg.save(mark1 + files)
			print('1 start')
		elif path == 'mark2\\':
			im200  = Image.open(imgpath).convert('RGB')
			try:
				newimg = im200.resize((width, height), Image.BILINEAR)
			except:
				pass
			else:
				newimg.save(mark2 + files)
			print('1 start')
	print('%s done' %path)