# Springer-quarantine-books-python

a python script to download open-access books from Springer

the news "Springer open access resources to assist with the COVID-19 pandemic" see [link](https://www.springernature.com/gp/librarians/landing/covid19-library-resources)

灵感来自于代码仓库[github-danielw2904/SpringerQuarantineBooks.jl](https://github.com/danielw2904/SpringerQuarantineBooks.jl)，我想借助Python丰富的生态环境，应该也可以实现这一功能

## quickstart

1. requirements
   * `tqdm`: draw progress bar
   * `click`: command line tools
   * `requests`: download http/https content
   * `pandas`: read xlsx
   * `xlrd`: read xlsx
   * `lxml`: parse html
2. install requirements (select one of below)
   * `conda install -c conda-forge tqdm click requrests pandas xlrd lxml`
   * `pip install tqdm click requrests pandas xlrd lxml`

更新ebook列表

```bash
$ python springerbook.py update
```

展示ebook列表

```bash
$ python springerbook.py show all #list all ebooks
$ python springerbook.py show downloaded #list downloaded ebooks
$ python springerbook.py show not-downloaded #list not-downloaded ebooks
```

下载ebook

```bash
$ python springerbook.py download 5 #download the first 5 ebooks from not-downloaded list
$ python springerbook.py download-E-ISBN 978-0-387-22592-0
```

下载的ebook保存在`./download`目录，ebook列表文件(xlsx)保存在`./cache`目录

## LICENSE以及权责声明

所有下载内容的所有权归Springer所有，与当前代码仓库无关。下载链接通过该[网页链接](https://www.springernature.com/gp/librarians/news-events/all-news-articles/ebooks/free-access-to-textbooks-for-institutions-affected-by-coronaviru/17855960)获得，我想Springer的LICENSE声明应该会在相关的网页中。

当前代码仓库仅提供下载工具，如果该工具损害了您的权益，望告知。

## Q & A

Why README.md not all in English?

> My English is poor

为什么下载速度很慢？

> 也许需要使用代理

下载抛错该如何处理？

> 大多数情况下重新运行即可，实在不能解决可以提个issue，虽然大概率我也不懂（个人的计算机网络知识依旧非常贫瘠┑(￣Д ￣)┍

为什么不提供python2支持？

> 已经2020年了。。。
