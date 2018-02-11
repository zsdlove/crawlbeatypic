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
import io
reload(sys)
sys.setdefaultencoding('utf-8')
header2={
   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
   'Accept-Encoding':'gzip, deflate',
   'Accept-Language':'zh-CN,zh;q=0.8',
   'Cache-Control':'max-age=0',
   'Connection':'keep-alive',
   'Host':'images.zhaofulipic.com:8818',
   'If-Modified-Since':'Sat, 10 Feb 2018 08:04:08 GMT',
   'If-None-Match':"08cf2b945a2d31:0",
   'Upgrade-Insecure-Requests':'1',
   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
}
#lock=threading.Lock()
lock=multiprocessing.Lock()
def downloadimg(src,dirname):
    img = requests.get(src,headers=header2,timeout=10)
    mm = hashlib.md5()
    filename = mm.update(src)
    filename=mm.hexdigest()
    filename=filename+".jpg"
    basename="G://img8//"
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
    # 获取一页的imgurl
    response=requests.get(url)
    html2=response.content
    selector=etree.HTML(html2)
    with lock:
     for cc in range(1,9):
      try:
        content2=selector.xpath('/html/body/section/div/div/article['+str(cc)+']/header/h2/a/@href')#dir套图地址
        ttname=selector.xpath('/html/body/section/div/div/article['+str(cc)+']/header/h2/a/text()')#套图名称
        if content2=='':
            return
        ttadr="http://yxpjwnet1.com"+str(content2[0])
        print ttname[0].decode('gb2312','ignore')
		#get http://yxpjwnet1.com/youmihui/2018/0210/4659.html   to 4659_30.html
        #开始下一级目录下载
        for everytt in range(2,30):#套图下载开始...
         try:
           sp=ttadr.split('.h')
           newttadr=sp[0]+'_'+str(everytt)+'.html'
           response2=requests.get(newttadr)
           print newttadr
           html3=response2.content
           selector2=etree.HTML(html3)
           for ii in range(1,5):
            try:
              content3=selector2.xpath('/html/body/section/div/div/article/p['+str(ii)+']/img/@src')
              if len(content3)==0:
                 return
              print content3[0]
              downloadimg(content3[0],ttname[0].decode('gb2312','ignore'))
            except:
              continue
         except:
            continue
      except:
         continue
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