
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib
import urllib2
import os
import requests
from bs4 import BeautifulSoup
import argparse

def getHtml(url_address):
	 """
    通过url_address得到网页内容
    :param url_address: 请求的网页地址
    :return: html
    """
	headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
	request=urllib2.Request(url_address,headers=headers)
	response=urllib2.urlopen(request)
	return response

def get_soup(html):
	"""
    把网页内容封装到BeautifulSoup中并返回BeautifulSoup
    :param html: 网页内容
    :return:BeautifulSoup
    """
	if None==html:
		return
	return BeautifulSoup(html.read(),"html.parser")

def get_img_dirs(soup):
	 """
    获取所有相册标题及链接
    :param soup: BeautifulSoup实例
    :return: 字典（ key:标题， value:内容）
    """
	if None==soup:
		return
	lis=soup.find(id="pins").find_all(name="li")
	if None!=lis:
		img_dirs={};
		for li in lis:
			links=li.find('a')
			k=links.find('img').attrs['alt']
			t=links.attrs['href']
			img_dirs[k]=t;
		# print img_dirs
		return img_dirs
def download_imgs(info):
	if None==info:
		return
	t=info[0]
	l=info[1]
	if None==t or None==l:
		return
	print "创建相册："+t+""+l
	try:
		os.mkdir(t)
	except Exception as e:
		print "文件夹："+t+",已经存在"
	print "开始获取相册《"+t+"》，图片数量为..."
	dir_html=getHtml(l)
	dir_soup=get_soup(dir_html)
	img_page_url=get_dir_img_page_url(l,dir_soup)

	#得到当前相册的封面
	main_image=dir_soup.find_all(name="div",attrs={'class':'main-image'})
	if None!=main_image:
		for image_parent in main_image:
			imgs=image_parent.find_all(name='img')
			if None!=imgs:
				img_url=str(imgs[0].attrs['src'])
				filename=img_url.split('/')[-1]
				print "开始下载："+img_url+",保存为："+filename
				save_file(t,filename,img_url)

	#获取相册下的图片
	for photo_web_url in img_page_url:
		download_img_from_page(t,photo_web_url)

def download_img_from_page(t,page_url):
	dir_html=getHtml(page_url)
	dir_soup=get_soup(dir_html)

	#得到当前页面的图片
	main_image=dir_soup.find_all(name='div',attrs={'class':'main-image'})
	if None!=main_image:
		for image_parent in main_image:
			imgs=image_parent.find_all(name='img')
			if None!=imgs:
				img_url=str(imgs[0].attrs['src'])
				filename=img_url.split('/')[-1]
				print "开始下载："+img_url+",保存为："+filename
				save_file(t,filename,img_url)

def save_file(d,filename,img_url):

	print(img_url+"=======")
	img=requests.get(img_url)
	name=str(d+"/"+filename)
	with open(name.decode('utf-8'),"wb") as code:
		code.write(img.content)

def get_dir_img_page_url(l,dir_soup):#得到l路径下所有的链接地址
	divs=dir_soup.find_all(name="div",attrs={'class':'pagenavi'})
	navi=divs[0]
	links=navi.find_all(name='a')
	if None==links:
		return
	a=[]
	url_list=[]
	for link in links:
		h=str(link['href'])
		if len(h.split('/'))!=len(l.split('/')):
			n=h.replace(l+"/","")  #n表示第n张照片
			try:
				a.append(int(n))
			except Exception as e:
				print "错误",e
	_max=max(a)     #一个文件夹中得到照片总数
	for i in range(1,_max):
		u=str(l+"/"+str(i))
		url_list.append(u)
	return url_list

if __name__=='__main__':
	# parser=argparse.ArgumentParser()
	# parser.add_argument("echo")
	# args=parser.parse_args()
	# url=str(args.echo)
	# print "开始解析"+url

	html=getHtml("http://www.mzitu.com/xinggan")
	soup=get_soup(html)
	img_dirs=get_img_dirs(soup)
	for key in img_dirs:
		# print img_dirs[key]
		# dir_html=getHtml(img_dirs[key])
		# dir_soup=get_soup(dir_html)
		# a=get_dir_img_page_url(img_dirs[key],dir_soup)

	
		if None==img_dirs:
	 		print "无法获取该网页下的相册内容"
		else:
	 		for key in img_dirs.items():
	 			download_imgs(key)

		



