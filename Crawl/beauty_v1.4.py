# -*- coding: utf-8 -*-
import threading
import requests
import time
import json
import sys
import csv
import re
import os
from bs4 import BeautifulSoup

HTML_PARSER = "html.parser"
USER_AGENT  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
HEADERS     = {'User-Agent': USER_AGENT}
CSVFILE     = 'beautycsv.csv'
BASE_URL    = 'https://www.ptt.cc'
TARGET_URL  = 'https://www.ptt.cc/bbs/Beauty/index'

def reqRes(url, option):
	#option 0 means to download the picture
	#option 1 means to select tags by BeautifulSoup
	try:
		res = requests.get(url, headers=HEADERS)
	except:
		return 'url error'
	else:
		res.encoding = 'utf-8'
		if res.status_code == 200 and option == 1:
			return BeautifulSoup(res.text, HTML_PARSER)
		elif res.status_code == 200 and option == 0:
			return res.content
		else:
			return 'url error'

def getIndexNumber(url):
	soup = reqRes(url, 1)
	indexnumber = soup.select('a.wide')[1].get('href')
	indexnumber = int(re.findall(r"\d+", indexnumber)[0])+1
	return indexnumber

def getFeature(pages): #main
	print(pages)
	url = 'https://www.ptt.cc/bbs/Beauty/index'
	featureDict = {}
	for page in pages:
		time.sleep(0.5)
		soup = reqRes(url+str(page) + '.html', 1)
		eachrow = soup.select('div.r-ent')
		eachrow_number = len(eachrow)
		for row in range(0, eachrow_number):
			try:
				title_with_a = eachrow[row].select('div.title > a')[0].text.strip()
			except: #文章被刪除
				title_without_a = eachrow[row].select('div.title')[0].text.strip()
				print(title_without_a)
			else:
				if '公告' in title_with_a:
					continue
				else:
					postLink = eachrow[row].select('div.title > a')[0].get('href')
					stopword = ['/', '／', '\\', ':', '*', '?', '"', '<', '>', '|', '.', '　', '。']
					for symbol in stopword:
						if symbol in title_with_a:
							title_with_a = title_with_a.replace(symbol, ' ').strip()
					print(page)
					print(title_with_a)
					featureDict['title']  = title_with_a
					print(postLink)
					#featureDict['post_link'] = postLink
					getPictureAndPushTagAndContent(title_with_a, postLink, featureDict)

def getPictureAndPushTagAndContent(folderName, postlink, featureDict):
	imgLinkList = []
	downList    = []
	mark        = 0
	push        = 0
	booo        = 0
	none        = 0
	numberOfImg = 0
	soup = reqRes(BASE_URL+postlink, 1)
	if soup == 'url error':
		with open('urlLog.txt', 'a') as urllog:
			log = 'url error: ' + postlink + '\n'
			urllog.write(log)
		print(log)
	else:
		imgLink_tag = soup.select('div#main-content > a')
		if len(imgLink_tag) == 0: #沒圖片就跳出
			return
		for i in range(0, len(imgLink_tag)):
			imgLink = imgLink_tag[i].get('href')
			re_imgLink = re.match(r'^https?://(i.)?(m.)?imgur.com', imgLink)
			if re_imgLink != None:
				if not imgLink.endswith('.jpg') and not imgLink.endswith('.gif') and not imgLink.endswith('.png'):
					imgLink += '.jpg'
				imgLinkList.append(imgLink)
				numberOfImg = len(imgLinkList)
				if numberOfImg == 0:
					return
				else:
					featureDict['number_of_img'] = numberOfImg
					#return downList.append([folderName, str(i), imgLink])
					downloadPicture(folderName, str(i), imgLink)
		pushTag_tag     = soup.select('span.push-tag') #推文符號
		pushContent_tag = soup.select('span.push-content') #留言
		for i in range(0, len(pushTag_tag)):
			pushTag = pushTag_tag[i].text.strip()
			if pushTag == '→':
				none += 1
			elif pushTag == '推':
				push += 1
			elif pushTag == '噓':
				booo += 1
			else:
				print('pushtag error')
		total = push-booo
		featureDict['number_of_push'] = push
		featureDict['number_of_booo'] = booo
		featureDict['number_of_none'] = none
		featureDict['total_push']     = total
		if total > 50:
			mark = 1
			featureDict['mark2'] = mark
		else:
			mark = 0
			featureDict['mark2'] = mark
		if total <= 35:
			mark = 0
			featureDict['mark3'] = mark
		elif 70 >= total > 35:
			mark = 1
			featureDict['mark3'] = mark
		elif total > 70:
			mark = 2
			featureDict['mark3'] = mark
		else:
			featureDict['mark3'] = 'mark error'
		print("總推文: {total}, 推文數: {push}, 噓文數: {booo}, 箭頭數: {none}, 圖片數量: {img}\n".format(total = total, push = push, booo = booo, none = none, img = numberOfImg))
		data2csv(featureDict)


def downloadPicture(folderName, filename, imglink):
	error = ''
	imgPath = folderName + '/' + filename + '.jpg'
	content = reqRes(imglink, 0)
	if content != 'url error':
		try:
			if not os.path.isdir(folderName):
				os.makedirs(folderName)
				open(imgPath, 'wb').write(content)
				print('%s %s 下載完成' %(imglink, filename))
			else:
				open(imgPath, 'wb').write(content)
				print('%s %s 下載完成' %(imglink, filename))
		except Exception as e:
			with open(folderName + '/' + 'imgLog.txt','a') as imgError:
				error = e + ': ' + imglink + '\n'
				imgError.write(error)
			with open('log.txt', 'a') as log:
				logtag = folderName + '\n'
				log.write(logtag)
			print('something wrong', e)
	else:
		print('%s url error' %imglink)
		if not os.path.isdir(folderName):
			os.makedirs(folderName)
			with open(folderName + '/' + 'imgLog.txt','a') as imgError:
				error = 'url error: ' + imglink + '\n'
				imgError.write(error)
		else:
			with open(folderName + '/' + 'imgLog.txt','a') as imgError:
				error = 'url error: ' + imglink + '\n'
				imgError.write(error)

def data2csv(featureDict):
	fileName = 'beautycsv.csv'
	path = 'C:\\Users\\Robert\\Desktop\\big_data_mining\\finalVersion\\beautycsv.csv'
	fieldnames = ['title', 'total_push', 'mark2', 'mark3', 'number_of_push', 'number_of_booo', 'number_of_none', 'number_of_img'] #define fieldnames
	if os.path.exists(path):
		with open(fileName, 'a', newline='', encoding='utf8', errors="replace") as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writerow(featureDict)
	else:
		with open(fileName, 'a', newline='', encoding='utf8', errors="replace") as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			writer.writerow(featureDict)

def splitPages(platform, pages, last, url):
	pageList = []
	indexnumber = getIndexNumber(url + '.html') - last
	howManyPage = indexnumber - pages
	print("從{howManyPage}到{indexnumber}".format(indexnumber = indexnumber, howManyPage = howManyPage))
	peace = pages//platform
	for i in range(0, platform):
		if i == platform - 1:
			pageList.append(range((howManyPage+peace*i)+1, indexnumber))
		else:
			pageList.append(range(howManyPage+peace*i, howManyPage+peace*(i+1)))
	return pageList


if __name__ == '__main__':
	threads = []
	start = time.time()
	platform = int(sys.argv[1])
	pages    = int(sys.argv[2])
	last     = int(sys.argv[3])
	rangeList = splitPages(platform, pages, last, TARGET_URL)
	for i in rangeList:
		mission = threading.Thread(target=getFeature, args=([i]))
		mission.start()
		threads.append(mission)
	[mission.join() for mission in threads]
	end = time.time()
	runtime = end-start
	print(runtime)


	data:{
		'picture':'xxx.jpg',
		'push':50
	}