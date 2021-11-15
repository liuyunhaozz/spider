import requests

img_url = '//n.sinaimg.cn/sinacn10101/455/w1242h1613/20200115/753b-imztzhn9598423.jpg'
res = requests.get(img_url)

with open('test', "wb") as f:
    f.write(res.content)