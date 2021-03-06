import requests
import re
import time
import threading
import math
import os

CNT = 0
# 每个线程下载图片数
CAPACITY = 30
# wallpaper 保存目录
SAVE_DIR = 'wallpapers'

class httpThread (threading.Thread):
    def __init__(self, threadID, threadName, httpList):
        threading.Thread.__init__(self)
        self.id = threadID
        self.name = threadName
        self.list = httpList
    
    def run(self):
        for image in self.list:
            downloadImg(image, self.name)
        

def transformPx(url):
    arr = url.split('/')
    return '/'.join(arr[:-1]) + '/1920x1080.jpg'


def getAllImageUrl(): 
    imgArr = []
    for i in range(50):
        homePage = 'https://vlad.studio/wallpapers/?sort=newest&filter=all&page=' + str(i)
        text = requests.get(homePage).text

        pattern = re.compile('src="(https://files.vlad.studio/sequoia/.*?\.jpg)"')
        images = pattern.findall(text)
        images = list(map(transformPx, images))
        imgArr.extend(images)

        # print
        # print(imgArr)
    return imgArr


def downloadImg(image, threadName):
    global CNT
    CNT += 1
    content = requests.get(image).content
    name = image.split('/')[-3] + '.jpg'
    with open('./wallpapers/' + name, 'wb') as f:
        f.write(content)
    print(CNT, ':', threadName, ':', name)


def doneLog():
    print('Done')
    print('Time Cost:')
    print(time.process_time())


def createDir():
    isDirExisted = os.path.exists(SAVE_DIR)
    if not isDirExisted:
        os.makedirs(SAVE_DIR)


def main(): 
    createDir()
    images = getAllImageUrl()
    l = len(images)
    threadNum = math.ceil(l / CAPACITY)
    for i in range(threadNum):
        if (i + 1) * CAPACITY <= l:
            imageList = images[i * CAPACITY : (i + 1) * CAPACITY]
        else:
            imageList = images[i * CAPACITY : l]
        thread = httpThread(i+1, 'thread_' + str(i+1), imageList)
        thread.run()


main()