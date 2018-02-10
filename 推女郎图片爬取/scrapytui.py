# -*- coding:utf-8 -*-
from lxml import etree
import requests
import random
import hashlib
import sys
import os
import time
import threading
from multiprocessing import Pool, cpu_count
import multiprocessing
header2={
}
#lock=threading.Lock()
lock=multiprocessing.Lock()
def downloadimg(src,dirname):
    img = requests.get(src, headers=header2, timeout=10)
    mm = hashlib.md5()
    filename = mm.update(src)
    filename=mm.hexdigest()
    filename=filename+".jpg"
    basename="G://img5//"
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
    nexturl="http://yxpjwnet1.com/page/" +str(num)+".html"
    return nexturl
def getonepageimg(url):
    zsdlove=1
    # 获取一页的imgurl
    response=requests.get(url)
    html2=response.content
    selector=etree.HTML(html2)
    with lock:
      for num in range(1, 15):
        content2=selector.xpath('/html/body/section/div/div/article[1]/header/h2/a/@href')#dir
        print  str(content2[0])
        if content=='':
            return 
        print "url is====>",content[0]
        #开始下一级目录下载
        #response2=requests.get(content2[0])
        #html3=response2.content
        #selector2=etree.HTML(html3)
        #content3=selector2.xpath('/html/body/section/div/div/article/p[2]/img/@src')
		#content3=http://yxpjwnet1.com/luyilu/2018/0210/4661_21.html
if __name__ == "__main__":
    print "sssss"
    urls=[getnexturl(num)
        for num in range(1,61)]
    print urls
    pool = Pool(processes=cpu_count())
    try:
       pool.map(getonepageimg,urls)
    except Exception as e:
      print e
      pool.map(getonepageimg,urls)
      getonepageimg(url)
#timestart=time.time()
#main()
#timedf=time.time()-timestart
#print "共花费了:".decode('utf-8')+str(timedf)+'s'