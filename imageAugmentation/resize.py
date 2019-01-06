import os
import sys
import numpy as np
import pandas as pd
from PIL import Image, ImageChops

paths     = 'change yours'
threepath = ['mark1\\', 'mark2\\']
width     = 64
height    = 64
mark0     = 'change yours'
mark1     = 'change yours'
mark2     = 'change yours'

for path in threepath:
	for files in os.listdir(paths + path):
		imgpath = paths + path + files
		if path == 'mark0\\':
			im200  = Image.open(imgpath).convert('RGB')
			try:
				newimg = im200.resize((width, height), Image.BILINEAR)
			except:
				pass
			else:
				newimg.save(mark1 + files)
		elif path == 'mark1\\':
			im200  = Image.open(imgpath).convert('RGB')
			try:
				newimg = im200.resize((width, height), Image.BILINEAR)
			except:
				pass
			else:
				newimg.save(mark1 + files)
		elif path == 'mark2\\':
			im200  = Image.open(imgpath).convert('RGB')
			try:
				newimg = im200.resize((width, height), Image.BILINEAR)
			except:
				pass
			else:
				newimg.save(mark2 + files)
	print('%s done' %path)
