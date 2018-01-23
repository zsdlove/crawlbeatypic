# -*- coding:utf-8 -*-
from lxml import etree
import requests
import random
import hashlib
import sys
import os
import time
header2={
    'Host': 'www.mmjpg.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.mmjpg.com/mm/1193/5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
headers = {
    'Host': 'www.mmjpg.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}
header={
     'Host': 'img.mmjpg.com',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
     'Accept': '*/*',
     'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
     'Accept-Encoding': 'gzip, deflate',
     'Referer': 'http://www.mmjpg.com/',
     'Connection': 'keep-alive'
}
HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "http://www.mmjpg.com"
}
def downloadimg(src,dirname):
    img = requests.get(src, headers=HEADERS, timeout=10)
    mm = hashlib.md5()
    filename = mm.update(src)
    filename=mm.hexdigest()
    filename=filename+".jpg"
    basename="G://img3//"
    filedir=basename+dirname+"//"
    if os.path.exists(filedir)==False:
       os.mkdir(filedir)
    filepath=filedir+filename
    f = open(filepath,"ab")
    f.write(img.content)
    f.close()
    print "download successfully"
def getnexturl(num):
    # 获取下一页
    #selector=etree.HTML(html)
    #nexturl=selector.xpath("/html/body/div[2]/div[1]/div/div/a["+str(num)+"]/@href")
    nexturl="http://www.mmjpg.com/home/" +str(num)
    return nexturl
def getonepageimg(url):
    zsdlove=1
    # 获取一页的imgurl
    response=requests.get(url)
    html2=response.content
    selector=etree.HTML(html2)
    for num in range(1, 15):
        content=selector.xpath('/html/body/div[2]/div[1]/ul/li[' + str(num) + ']/a/img/@src')#jpg
        content2=selector.xpath('/html/body/div[2]/div[1]/ul/li['+str(num)+']/a/@href')#dir
        content4=selector.xpath("/html/body/div[2]/div[1]/ul/li["+str(num)+"]/span[1]/a/text()")#dirname
        content5=selector.xpath("/html/body/div[2]/div[1]/ul/li["+str(num)+"]/span[3]/text()")#浏览量
        print content5[0]
        print content4[0]
        print  str(content2[0])
        if content=='':
            return 
        print "url is====>",content[0]
        #downloadimg(content[0])
        #开始下一级目录下载
        response2=requests.get(content2[0])
        html3=response2.content
        selector2=etree.HTML(html3)
        content3=selector2.xpath('//*[@id="content"]/a/img/@src')
        nob=1
        for nob in range(1,30):
            mmurl=os.path.dirname(content3[0])+'/'+str(nob)+".jpg"
            try:
              downloadimg(mmurl,content4[0])
            except:
              continue
def main():
    print "sssss"
    #response=requests.get("http://www.mmjpg.com")
    #html=response.content
    for num in range(2, 83):
        url=getnexturl(num)
        print url
        getonepageimg(url)
timestart=time.time()
main()
timedf=time.time()-timestart
print "共花费了：".decode('utf-8')+timedf+'s'
