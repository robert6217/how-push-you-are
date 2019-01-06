import os
import sys
import cv2
import dlib
import imutils
import numpy as np
import pandas as pd
from PIL import Image, ImageChops
from imutils.face_utils import rect_to_bb
from imutils.face_utils import FaceAligner

SOURCE_PATHS         = ['hotgirl/', 'other/']
STORE_PATHS          = 'E:/face/'
EXCEL_PATH           = 'beautyFinal.xlsx'
EXCELDATA            = pd.read_excel(EXCEL_PATH)
SHAPE_PREDICTOR_PATH = 'cv2/shape_predictor_68_face_landmarks.dat'
MARK                 = ['mark0/', 'mark1/', 'mark2/']
DETECTOR             = dlib.get_frontal_face_detector()
PREDICTOR            = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
FACE_PRE             = FaceAligner(PREDICTOR, desiredFaceWidth=200)

count0 = 0
count1 = 0
count2 = 0

if __name__ == '__main__':
	path = 'other/'
	for dirs in os.listdir(path):
		mark = ''
		#print(path + dirs)
		try:
			mark = int(EXCELDATA[EXCELDATA.title == dirs].mark3.tolist()[0])
		except:
			pass
		else:
			for files in os.listdir(path + dirs):
				full_path = path + dirs + '/' + files
				print('mark%s %s' %(mark, full_path))
				try:
					img = Image.open(full_path).convert('RGB')
				except:
					os.remove(full_path)
					print('cant open image heve be removed: ', full_path)
				else:
					errorimg  = Image.open(STORE_PATHS + 'error/error.jpg').convert('RGB')
					diff      = ImageChops.difference(img, errorimg)
					if diff.getbbox() == None:
						os.remove(full_path)
						print('error image heve be removed: ', full_path)
					else:
						imgary = np.array(img)
						imgary = imutils.resize(imgary, width=1280)
						gray = cv2.cvtColor(imgary, cv2.COLOR_BGR2GRAY)
						faces = DETECTOR(gray, 2)
						if len(faces) > 0:
							for face in faces:
								(x, y, w, h) = rect_to_bb(face)
								try:
									faceOrig = imutils.resize(imgary[y : y+h, x : x+w], width=400)
								except:
									with open(STORE_PATHS + 'error/imgLog.txt','a', encoding='utf-8') as imgNoFace:
										noface = full_path + '\n'
										imgNoFace.write(noface)
								else:
									faceAligned_bgr = FACE_PRE.align(imgary, gray, face)
									faceAligned_rgb = faceAligned_bgr[:,:,::-1] #imgshow 三原色順序是bgr 要換成 rgb才會正常顯示圖片顏色
									if mark == 0:
										cv2.imwrite(STORE_PATHS + MARK[0] + str(count0) + '_other.jpg', faceAligned_rgb)
										count0 += 1
									elif mark == 1:
										cv2.imwrite(STORE_PATHS + MARK[1] + str(count1) + '_other.jpg', faceAligned_rgb)
										count1 += 1
									elif mark == 2:
										cv2.imwrite(STORE_PATHS + MARK[2] + str(count2) + '_other.jpg', faceAligned_rgb)
										count2 += 1
						else:
							with open(STORE_PATHS + 'error/imgLog.txt','a', encoding='utf-8') as imgNoFace:
								noface = full_path + '\n'
								imgNoFace.write(noface)
