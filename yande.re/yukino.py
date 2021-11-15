import requests
from bs4 import BeautifulSoup
import time
import os

class Yokino(object):
    def __init__(self, url, path):
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",

        }
        self.title = ""
        self.path = path
        self.url = url
        self.url_list = []
        self.img_list = []

    def get_soup(self, url):
        res = requests.get(url, headers=self.header, timeout=50)
        res_html = res.content.decode("utf-8")
        soup = BeautifulSoup(res_html, "lxml")
        return soup

    def get_url_list(self):
        
        soup = self.get_soup(self.url)
        # 利用 css 选择器语法 
        links = soup.select("li div a")   
        for j in links:
            # 获取 href 属性所对应的值
            one_link = j.get("href")  
            # print(one_link)
            
            self.url_list.append('https://yande.re' + one_link)


    def get_img(self):
        for url in self.url_list:
            soup = self.get_soup(url)
            img_link = soup.select("div div img[id='image']")
            # print(img_link)
            for img in img_link:
                link = img.get('src')
                print(f"开始获取图片链接{link}")
                print("----------------------------------------------")
                self.img_list.append(link)

    def down_img(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        # 开始下载图片
        for index, img_url in enumerate(self.img_list):
            name = str(index + 1) + '.jpg'

            print(f"开始下载图片{name}-------->")
            res = requests.get(img_url, headers=self.header)
            if res.status_code == 404:
                print(f"图片{img_url}下载出错------->")
            img_name = os.path.join(self.path, name)
            # print(img_name)
            with open(img_name, "wb") as f:
                f.write(res.content)
                # print(res.content)   编码的图片
            print(f"图片{name}下载完成--------->")
            



if __name__ == '__main__':
    yokino = Yokino('https://yande.re/pool/show/97980', 'yokino')
    yokino.get_url_list()
    yokino.get_img()
    yokino.down_img()
