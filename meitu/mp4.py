# coding:utf-8

import re
import os
import time
import threading
from multiprocessing import Pool, cpu_count

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'http://www.mzitu.com'
}

DIR_PATH = r"/Users/qiuhong/Desktop/mzitu"      # 下载图片保存路径


def save_to_file(pic_str):
    filename = 'mp4_urls.txt'
    outfile = open(filename, 'a')
    outfile.write(pic_str)
    outfile.close


def get_urls():
    """ 获取 13lulu 网站下所有套图的 url
    """

    url_pre = 'http://13lulu.com/list/index57'
    url_x = '.html'
    page_urls = []
    page_urls.append(url_pre + url_x)
    for cnt in range(2, 8):
        page_urls.append(url_pre + '_{cnt}'.format(cnt=cnt) + url_x)
    print("Please wait for second ...")

    video_urls = []
    for page_url in page_urls:
        try:
            bs = BeautifulSoup(
                requests.get(page_url, headers=HEADERS, timeout=10).text,
                'lxml').find('ul', {"class": "m_Box1"})
            result = re.findall(r"(?<=href=)\S+", str(bs))      # 匹配所有 urls
            video_url = [url.replace('"', "") for url in result]
            video_urls.extend(video_url)
        except Exception as e:
            print(e)

    urls =[]
    for url in set(video_urls):
        index_pre = url.replace('/view/index', '')
        index = index_pre.replace('.html', '')
        final_url = 'http://13lulu.com/player/index{index}.html?{index}-0-0'.format(index=index)
        urls.append(final_url)

    count = len(urls)
    i = 0

    final_video_urls = []
    for url in urls:
        try:
            bs = BeautifulSoup(
                requests.get(url, headers=HEADERS, timeout=10).text,
                'lxml')
            a1 = bs.find('div', id='a1')
            script = a1.find('script')
            mp4_url = str(a1)[(str(a1).find('f:') + 3):(str(a1).find('c:0,') - 10)].replace("',", "").replace('\r', '')
            final_video_urls.append(mp4_url)
            i += 1
            print "{i} / {count}".format(i=i, count=count)
            print mp4_url
        except Exception as e:
            print(e)

    return set(final_video_urls)    # 利用 set 去重 urls


lock = threading.Lock()     # 全局资源锁



def urls_crawler(url):
    """ 爬虫入口，主要爬取操作
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=10).text
        folder_name = BeautifulSoup(r, 'lxml').find(
            'div', class_="main-image").find('img')['alt'].replace("?", " ")
        with lock:
            if make_dir(folder_name):
                # 套图里图片张数
                max_count = BeautifulSoup(r, 'lxml').find(
                    'div', class_='pagenavi').find_all('span')[-2].get_text()
                page_urls = [url + "/" + str(i) for i in range(1, int(max_count) + 1)]
                img_urls = []

                for _, page_url in enumerate(page_urls):
                    time.sleep(0.6)
                    result = requests.get(page_url, headers=HEADERS, timeout=10).text
                    img_url = BeautifulSoup(result, 'lxml').find(
                        'div', class_="main-image").find(
                        'p').find('a').find('img')['src']
                    img_urls.append(img_url)
                for cnt, url in enumerate(img_urls):
                    save_pic(url, cnt)
    except Exception as e:
        print(e)


def save_pic(pic_src, pic_cnt):
    """ 保存图片到本地
    """
    try:
        img = requests.get(pic_src, headers=HEADERS, timeout=10)
        imgname = "pic_cnt_{}.jpg".format(pic_cnt + 1)
        with open(imgname, 'ab') as f:
            f.write(img.content)
            print(imgname)
    except Exception as e:
        print(e)


def save_video(video_src):
    """ 保存video到本地
    """
    print "save video"


    try:
        img = requests.get(video_src, headers=HEADERS, timeout=10)
        # imgname = "pic_cnt_{}.jpg".format(pic_cnt + 1)
        video_name = 'video'
        print video_name
        with open(video_name, 'ab') as f:
            f.write(img.content)
            print(video_name)
    except Exception as e:
        print(e)


def make_dir(folder_name):
    """ 新建文件夹并切换到该目录下
    """
    path = os.path.join(DIR_PATH, folder_name)
    # 如果目录已经存在就不用再次爬取了，去重，提高效率。存在返回 False，否则反之
    if not os.path.exists(path):
        os.makedirs(path)
        print(path)
        os.chdir(path)
        return True
    print("Folder has existed!")
    return False


def delete_empty_dir(dir):
    """ 如果程序半路中断的话，可能存在已经新建好文件夹但是仍没有下载的图片的情况
    但此时文件夹已经存在所以会忽略该套图的下载，此时要删除空文件夹
    """
    if os.path.exists(dir):
        if os.path.isdir(dir):
            for d in os.listdir(dir):
                path = os.path.join(dir, d)     # 组装下一级地址
                if os.path.isdir(path):
                    delete_empty_dir(path)      # 递归删除空文件夹
        if not os.listdir(dir):
            os.rmdir(dir)
            print("remove the empty dir: {}".format(dir))
    else:
        print("Please start your performance!")     # 请开始你的表演


if __name__ == "__main__":
    urls = get_urls()
    # print urls
    save_to_file(str(urls))

    for url in urls:
        save_to_file(url + '\r')
    # save_video('https://201712mp4.89soso.com/20171230/18/1/xml/91_5a2f1084b4184af6f71ca2b0453a1e52.mp4')
    #
    # pool = Pool(processes=cpu_count())
    # try:
    #     # delete_empty_dir(DIR_PATH)
    #     pool.map(save_video, urls)
    # except Exception as e:
    #     time.sleep(30)
    #     # delete_empty_dir(DIR_PATH)
    #     pool.map(save_video, urls)
