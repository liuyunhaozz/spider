import requests
from bs4 import BeautifulSoup
import time
import os
import argparse


class Yokino(object):
    def __init__(self, url, path):
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",

        }
        self.title = ""
        self.path = path
        self.url = url
        self.page_list = []
        self.url_list = []
        self.img_list = []

    def get_soup(self, url):
        res = requests.get(url, headers=self.header, timeout=50)
        res_html = res.content.decode("utf-8")
        soup = BeautifulSoup(res_html, "lxml")
        return soup

    """获取每一页的 url"""
    def get_page_list(self):
        soup = self.get_soup(self.url)
        links = soup.select('a[aria-label]')
        num = int(links[-1].get_text())
        for i in range(num):
            self.page_list.append(self.url + f'&page={i + 1}')

    """获取一页中所有图片的高清页面 url"""
    def get_url_list(self):
        
        for url in self.page_list:
            soup = self.get_soup(url)
            # 利用 css 选择器语法 
            links = soup.select("li div a")   
            for j in links:
                # 获取 href 属性所对应的值
                one_link = j.get("href")  
                # print(one_link)
                
                self.url_list.append('https://yande.re' + one_link)
    
    """获取每一张图片的存储地址 url"""
    def get_img(self):
        amount = len(self.url_list)
        for index, url in enumerate(self.url_list):
            soup = self.get_soup(url)
            # css 选择器语法
            img_link = soup.select("div div img[id='image']")
            # print(img_link)
            for img in img_link:
                link = img.get('src')
                print(f"开始获取图片链接 {index + 1} / {amount}")
                print(f'{link}')
                print("----------------------------------------------------")
                self.img_list.append(link)

    """下载图片"""
    def down_img(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        amount = len(self.img_list)
        # 开始下载图片
        for index, img_url in enumerate(self.img_list):
            name = str(index + 1) + '.jpg'

            print(f"开始下载图片 {index + 1} / {amount}")
            res = requests.get(img_url, headers=self.header)
            if res.status_code == 404:
                print(f"图片{img_url}下载出错------->")
            img_name = os.path.join(self.path, name)
            # print(img_name)
            with open(img_name, "wb") as f:
                f.write(res.content)
                # print(res.content)   编码的图片
            print(f"图片{name}下载完成")
            print("-----------------------------------------------------")
            



def handle(args):
    yokino = Yokino(f'https://yande.re/post?tags=' + args.tag, args.save)
    yokino.get_page_list()
    yokino.get_url_list()
    yokino.get_img()
    yokino.down_img()




def main():
    parser = argparse.ArgumentParser()
   
    parser.add_argument('--tag', required=True, help="Enter the tag name")
    parser.add_argument('--save', required=True, help="Enter the name of your file-dir")
    
    parser.set_defaults(func=handle)	# 绑定处理函数
    # 将函数参数设置为命令行的值
    args = parser.parse_args()
    # 执行函数功能
    args.func(args)


if __name__ == '__main__':
    main()
