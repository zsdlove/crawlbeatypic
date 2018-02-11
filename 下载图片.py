# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:46:44 2018
@author: ocean
E-mail:2998634840@qq.com
TO:Practice makes perfect.

"""
import requests
import os
import hashlib
from lxml import etree
import random
import time
header2={
    #'Host': 'www.mmjpg.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.mmjpg.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}
HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "http://www.mmjpg.com"
}
def downloading(src,dirname):
    print("下载")
    img = requests.get(src,headers=header2)
    print("img="+str(img))
    #print("mm="+str(mm))
    
    filename= random.randint(1,1000)
    #filename = str(GetNowTime())
    print("filename2="+str(filename))
    #filename = mm.hexdigest()
    print("filename3="+str(filename))
    filename=str(filename)+".jpg"
    print("filename="+str(filename))
    basename = "G://img//"
    filedir = basename+dirname+"//"
    print("filedir==="+str(filedir))
    if os.path.exists(filedir)==False:
        print("新建")
        os.mkdir(filedir)
    filepath = filedir+filename
    print("filepath==="+str(filepath))
    f = open(filepath,"ab")
    f.write(img.content)
    f.close()
    print("download successfully.")
def getnexturl(num):
    nexturl = "http://www.mmjpg.com/home/"+str(num)
    return nexturl

def getonepageimg(url):
    print("----"+str(url))
    response = requests.get(url)
    html2 = response.content
    selector = etree.HTML(html2)
    for num in range(1,15):#15
        content = selector.xpath('/html/body/div[2]/div[1]/ul/li['+ str(num)+']/a/img/@src')
        content2=selector.xpath('/html/body/div[2]/div[1]/ul/li['+str(num)+']/a/@href')#dir
        content3=selector.xpath("/html/body/div[2]/div[1]/ul/li["+str(num)+"]/span[1]/a/text()")#dirname
        if content =='':
            return
        print("url is == ",content[0])
        #开始下一级目录下载
        response2 = requests.get(content2[0])
        print("response2 is == ",response2)
        html3 = response2.content
        selector2 = etree.HTML(html3)
        content4 = selector2.xpath('//*[@id="content"]/a/img/@src')
        print("content4 is == ",content4)
        nob = 1
        for nob in range(1,30):#30
            mmurl = os.path.dirname(content4[0])+'/'+str(nob)+".jpg"
            print("mmurl=="+str(mmurl))
            try:
                downloading(mmurl,content3[0])
            except:
                continue
            
def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
if __name__ == "__main__":
        for num in range(2,85):
            urls = getnexturl(num)
            getonepageimg(urls)
            print(urls)
 