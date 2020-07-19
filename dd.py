import requests
import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
import time
#
# reload(sys)
# sys.setdefaultencoding('utf-8')

client = MongoClient('127.0.0.1', 27017)
db = client.spider
collection = db.search_words_dtk

def test1():
    print(1)
    for i in collection.find():
        print(i)


def test():
    link = "http://www.dataoke.com/ddq?tempforqq=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    r = requests.get(link, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")

    tags = soup.select('.new_gjz')
    key_words = []
    for tag in tags:
        print('888', tag.get_text())
        key_words.append(tag.get_text().strip())

    print('key_words', key_words)
    for i in range(len(key_words)):
        conent = key_words[i]
        print(conent)
        post = {
            "id": i,
            "content": conent,
            "date": datetime.datetime.utcnow()  # 获取当前时间
        }
        print('post',post)
        collection.insert(post)
        # print('collection',1)

if __name__ == '__main__':
    test1()