# -*- coding:utf-8 -*-

import requests
import re
import os
import datetime

CATEGORIES = [
    '短视频', '国产精品', '女优专辑', '中文字幕', '亚洲无码', '欧美精品', '成人动漫'
]
BASEURL = 'https://www.dpz62.com/shipin/'
PAGENUM = 2


# 获取要下载的类型
def getCates():
    for i in range(len(CATEGORIES)):
        print(str(i+1) + '.', CATEGORIES[i])
    cates = input('\n输入下载类型：')
    if cates == '':
        cates = [1, 2]
    else:
        cates = list(map(lambda x: int(x), cates.split()))
    return list(map(lambda i: CATEGORIES[i-1], cates))


def getPageNum():
    num = input('\n输入要下载的页数（默认' + str(PAGENUM) + '页）：')
    if num == '':
        num = PAGENUM
    else:
        num = int(num)
    return num


def getVideoLinkByUrl(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    
    # # debug
    # print(url)
    pattern = re.compile('<input type="text" data-clipboard-text="(https://s1\.maomibf1\.com/.*?)"')

    link = pattern.findall(res.text)[0]
    print('下载链接：', link)
    return link


def getAllVideosByCategory(cate, pageNum):
    videos = []
    for i in range(pageNum):
        pageUrl = BASEURL + 'list-' + cate
        if i != 0:
            pageUrl += str(i+1)
        pageUrl += '.html'

        print('\n类型 ' + cate + ': 第' + str(i+1) + '页，' + '加载中...')
        
        res = requests.get(pageUrl)
        res.encoding = 'utf-8'

        print(pageUrl + ' 页面加载完毕')
        print('解析视频链接中...')

        pattern = re.compile('<a href="/shipin/(\d+?\.html)" title="(.*?)" target="_blank">')
        matches = pattern.findall(res.text)
        for match in matches:
            url = BASEURL + match[0]
            link = getVideoLinkByUrl(url)
            video = {
                "link": link,
                "title": match[1]
            }
            videos.append(video)

            print('视频 ' + video["title"] + ' 添加到视频池')
    return videos


def downLoadVideos(videos, cate):
    dirName = './videos/' + cate
    if not os.path.exists(dirName):
        print('创建文件夹：' + dirName)
        os.mkdir(dirName)
    for video in videos:
        title = video.title + '.' + video.link.split('.')[-1]
        if os.path.isfile(dirName + '/' + title):
            print('视频 ' + title + ' 已存在，跳过')
            continue
        else:
            print('视频 ' + title + ' 下载中...')
            start = datetime.datetime.now()
            content = requests.get(video.link).content

            with open(dirName + '/' + title, 'wb') as file:
                file.write(content)
            end = datetime.datetime.now()
            cost = (end - start).total_seconds() 
            print('Done. Costs: ' + int(cost) + 's')


def makeBaseDir():
    if not os.path.exists('./videos'):
        print('创建 ./videos 文件夹')
        os.mkdir('./videos')


def main():
    cates = getCates()
    print('下载类型：' + str(cates))
    pageNum = getPageNum()
    makeBaseDir()
    for cate in cates:
        videos = getAllVideosByCategory(cate, pageNum)
        downLoadVideos(videos, cate)


main()