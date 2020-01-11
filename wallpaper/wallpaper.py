import requests
import re
import time


def main(): 
    cnt = 0

    for i in range(20):
        homePage = 'https://vlad.studio/wallpapers/?sort=newest&filter=all&page=' + str(i)
        text = requests.get(homePage).text

        pattern = re.compile('src="(https://files.vlad.studio/sequoia/.*?\.jpg)"')
        images = pattern.findall(text)
        images = list(map(transformPx, images))

        for image in images:
            content = requests.get(image).content
            with open('./wallpapers/' + str(cnt) + '.jpg', 'wb') as f:
                f.write(content)
            print(cnt+1)
            cnt += 1


def transformPx(url):
    arr = url.split('/')
    return '/'.join(arr[:-1]) + '/1920x1080.jpg'


main()
print('Done')
print('Time Cost:')
print(time.process_time())