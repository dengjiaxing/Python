__author__ = 'CQC'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time

class QSBK:

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.stories = []
        self.enable = False
    
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print "connected failed,the reason is",e.reason
                return None

    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "load failed..."
            return None
        pattern=re.compile('<div.*?class="author.*?>.*?<a.*?>.*?<h2>(.*?)</h2>.*?</a>.*?<div.*?class="content">(.*?)</div>.*?<div.*?class="stats">.*?<i.*?class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        pageStories = []
        for item in items:
            #print item[0],item[1],item[2]
            pageStories.append([''+str(item[0]).strip()
                ,''+str(item[1]).strip(),''+str(item[2]).strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1
    
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print "page:%d\tpublisher:%s\n%s\npraise:%s\n" %(page,story[0],story[1],story[2])

    def start(self):
        print "Reading with Enter,Exit with Q"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()