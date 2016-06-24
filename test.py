#encoding:utf-8
import re
import urllib
import urllib2
import sys
page=2
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
url='http://www.qiushibaike.com/hot/page/'+str(page)
f=file('a.txt','w')
try:
	request=urllib2.Request(url,headers=headers)
	response=urllib2.urlopen(request)
	content=response.read()
	pattern=re.compile('<div.*?class="author.*?>.*?<a.*?>.*?<h2>(.*?)</h2>.*?</a>.*?<div.*?class="content">(.*?)</div>.*?<div.*?class="stats">.*?<i.*?class="number">(.*?)</i>',re.S)
	items=re.findall(pattern,content)
	string=[]
	for item in items:
		print item[0],item[1],item[2]
		f.write(str(item[0])+str(item[1])+str(item[2]))
		
	 	
except urllib2.URLError,e:
	if hasattr(e,"code"):
		print e.code
	if hasattr(e,"reason"):
		print e.reason