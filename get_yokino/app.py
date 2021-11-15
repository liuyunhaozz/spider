import requests
from bs4 import BeautifulSoup
import time
import os

class Yokino(object):
    def __init__(self, path):
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",

        }
        self.title = ""
        self.soup = ""
        self.path = path

    def get_soup(self, url):
        res = requests.get(url, headers=self.header, timeout=50)
        res_html = res.content.decode("utf-8")
        self.soup = BeautifulSoup(res_html, "lxml")
        return self.soup


    def down_jpg(self, nameint, img_url):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        # 开始下载图片
        name = str(nameint) + ".jpg"  # name = 1 2 3 4 ....
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



    def run(self):
        input("hit Enter to start downloading")
        # 生产每一页url地址
        for i in range(1, 2):
            templete = f'https://yande.re/pool/show/97980'
            # 提取地址中的图文链接
            soup = self.get_soup(templete)
            # 利用 css 选择器语法 选择具有值为'image'的itemprop属性的meta标签
            zipai_links = soup.select("li div a img")   

            # print(zipai_links)
            # print(zipai_links[0].get('src'))
            for index, j in enumerate(zipai_links):
                # 获取 content 属性所对应的值
                one_link = j.get("src")  
                # print(one_link)
                print(f"Start downloading {one_link}")
            
                # 将链接发给zipai类，执行run函数
                try:
                    self.down_jpg(index, one_link)
                    time.sleep(2)
                except Exception as e:
                    print(f'Get Error in {j}')
                    continue


        print("All Completed")


if __name__ == '__main__':
    yokino = Yokino('downloads')
    yokino.run()
