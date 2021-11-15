## 爬取 https://yande.re 上的二刺螈图片



![image-20211115171036823](https://github.com/liuyunhaozz/image/blob/main/img/20211115171026.png?raw=true)



- 采用各级 `url` 分别获取的策略，可以实现批量获取
- 采用 `soup.select` 中的 `css` 选择器进行筛选

---

新建 `tag.py` 用于获取指定标签的所有图片

```sh
$ python tag.py -h                                  
usage: tag.py [-h] --tag TAG --save SAVE      

optional arguments:
  -h, --help   show this help message and exit
  --tag TAG    Enter the tag name
  --save SAVE  Enter the name of your file-dir
```

> Demo

```sh
# 下载 tag 名为 yukinoshita_yukino 所有图片，合成后放入 demo 文件夹中
$ python tag.py --tag yukinoshita_yukino --save demo
```

