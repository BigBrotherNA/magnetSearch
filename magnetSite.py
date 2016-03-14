# -*- coding: utf-8 -*-

import gzip
import json
import re
import sys
import urllib
import urllib2
from StringIO import StringIO
from bs4 import BeautifulSoup

__author__ = 'jingqiwang'

reload(sys)
sys.setdefaultencoding('utf-8')
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11'}


class FanHao:
	def __init__(self, title, size, popularity, file_number, magnet_link, source, source_url):
		self.title = title
		self.size = size
		self.popularity = popularity
		self.file_number = file_number
		self.magnet_link = magnet_link
		self.source = source
		self.source_url = source_url


class magnetSite:
	def __init__(self):
		self.result = []

	def icili(self, fanhao):
		result = []
		try:
			url = 'http://www.icili.tv/search/%s_ctime_1.html' % fanhao
			request = urllib2.Request(url, headers=headers)
			response = urllib2.urlopen(request)
			if response.info().get('Content-Encoding') == 'gzip':
				buf = StringIO(response.read())
				f = gzip.GzipFile(fileobj=buf)
				page = f.read()
			else:
				page = response.read()
		except Exception, e:
			print e
			sys.exit(1)

		soup = BeautifulSoup(page, 'html.parser')
		for item in soup.find_all('div', class_='item'):
			title = item.a.text.strip()
			info = item.find('div', class_='info')
			span = info.find_all('span')
			size = span[1].b.text
			popularity = int(span[2].b.text)
			file_number = None
			magnet_link = 'magnet:?xt=urn:btih:' + item.find('a')['href'][1:-5]
			source = 'icili'
			source_url = 'http://www.icili.tv/'
			result.append(FanHao(title, size, popularity, file_number, magnet_link, source, source_url))

		self.result += result
		# return result

	def btdao(self, fanhao):
		result = []
		try:
			url = 'http://www.btdao.org/list/%s-s1d-1.html' % fanhao
			request = urllib2.Request(url, headers=headers)
			response = urllib2.urlopen(request)
			if response.info().get('Content-Encoding') == 'gzip':
				buf = StringIO(response.read())
				f = gzip.GzipFile(fileobj=buf)
				page = f.read()
			else:
				page = response.read()
		except Exception, e:
			print e
			sys.exit(1)

		soup = BeautifulSoup(page, 'html.parser')
		for item in soup.find_all('li'):
			title = item.a.text.strip()
			span = item.find('dt').find_all('span')
			size = span[0].text
			popularity = int(span[3].text)
			file_number = span[1].text
			magnet_link = 'magnet:?xt=urn:btih:' + item.find('a')['href'][8:]
			source = 'btdao'
			source_url = 'http://www.btdao.org/'
			result.append(FanHao(title, size, popularity, file_number, magnet_link, source, source_url))

		# return result
		self.result += result

	def cilisou(self, fanhao):
		def filter_tag(tag):
			return tag.name == 'td' and tag.has_attr('class') and tag.parent.name == 'tr' and tag.get('class')[0] == 'idx'

		result = []
		try:
			url = 'http://www.cilisou.cn/s.php?q=%s' % fanhao
			request = urllib2.Request(url, headers=headers)
			response = urllib2.urlopen(request)
			if response.info().get('Content-Encoding') == 'gzip':
				buf = StringIO(response.read())
				f = gzip.GzipFile(fileobj=buf)
				page = f.read()
			else:
				page = response.read()
		except Exception, e:
			print e
			sys.exit(1)

		soup = BeautifulSoup(page, 'html.parser')

		for item in soup.find_all(filter_tag):
			a = item.parent.find_all('a')
			title = a[0].text
			span = item.parent.find_all('span')
			size = span[1].text
			popularity = int(span[5].text)
			file_number = span[3].text
			if a[1].has_attr('onclick'):
				magnet_link = a[1]['onclick'][7:-2]
			else:
				magnet_link = a[1]['href']
			source = 'cilisou'
			source_url = 'http://www.cilisou.cn/'
			result.append(FanHao(title, size, popularity, file_number, magnet_link, source, source_url))

		self.result += result

	def kickass(self, fanhao):
		def filter_tag(tag):
			return tag.name == 'tr' and tag.has_attr('class') and (tag.get('class')[0] == 'odd' or tag.get('class')[0] == 'even')

		result = []
		try:
			'''
			import requests
			url = 'https://kat.cr/usearch/%s' % fanhao
			page = requests.get(url).text
			soup = BeautifulSoup(page, 'html.parser')

			works the same
			'''
			url = 'https://kat.cr/usearch/%s' % fanhao
			request = urllib2.Request(url, headers=headers)
			response = urllib2.urlopen(request)
			if response.info().get('Content-Encoding') == 'gzip':
				buf = StringIO(response.read())
				f = gzip.GzipFile(fileobj=buf)
				page = f.read()
			else:
				page = response.read()
		except Exception, e:
			print e
			sys.exit(1)

		soup = BeautifulSoup(page, 'html.parser')
		for item in soup.find_all(filter_tag):
			info = json.loads(item.find('div', class_='none')['data-sc-params'].replace('\'', '"'))
			title = urllib.unquote(info['name'])
			magnet_link = urllib.unquote(info['magnet'])
			size = item.find('td', class_='nobr center').text
			popularity = int(item.find('td', class_='green center').text)
			file_number = item.find_all('td', class_='center')[1].text
			source = 'kickass'
			source_url = 'https://kat.cr/'
			result.append(FanHao(title, size, popularity, file_number, magnet_link, source, source_url))

		self.result += result

	def kitty(self, fanhao):
		def filter_tag(tag):
			return tag.name == 'td' and tag.has_attr('class') and tag.get('class')[0] == 'name'

		result = []
		try:
			url = 'http://www.torrentkitty.net/search/%s' % fanhao
			request = urllib2.Request(url, headers=headers)
			response = urllib2.urlopen(request)
			if response.info().get('Content-Encoding') == 'gzip':
				buf = StringIO(response.read())
				f = gzip.GzipFile(fileobj=buf)
				page = f.read()
			else:
				page = response.read()
		except Exception, e:
			print e
			sys.exit(1)

		soup = BeautifulSoup(page, 'html.parser')
		for item in soup.find_all(filter_tag):
			title = item.text
			size = None
			popularity = None
			file_number = None
			magnet_link = item.parent.find(href=re.compile('magnet'))['href']
			source = 'torrentkitty'
			source_url = 'http://www.torrentkitty.net/'
			result.append(FanHao(title, size, popularity, file_number, magnet_link, source, source_url))

		self.result += result

	def generate_html(self, result):
		fanhao_html = open("Template.html", "r").read()
		soup = BeautifulSoup(fanhao_html, 'html.parser')
		fanhao_tbody_html = soup.find("tbody")
		for index, fanhao in enumerate(result):
			tr_tag = soup.new_tag('tr')
			fanhao_tbody_html.insert(0, tr_tag)

			fanhao_tbody_tr = fanhao_tbody_html.find('tr')
			th_tag = soup.new_tag('th')
			th_tag.string = str(len(result) - index)
			fanhao_tbody_tr.insert(0, th_tag)

			title_tag = soup.new_tag('td')
			title_tag.string = fanhao.title
			fanhao_tbody_tr.insert(1, title_tag)

			size_tag = soup.new_tag('td')
			if fanhao.size:
				size_tag.string = fanhao.size
			else:
				size_tag.string = '--'
			fanhao_tbody_tr.insert(2, size_tag)

			popularity_tag = soup.new_tag('td')
			if fanhao.popularity:
				popularity_tag.string = str(fanhao.popularity)
			else:
				popularity_tag.string = '--'
			fanhao_tbody_tr.insert(3, popularity_tag)

			file_number_tag = soup.new_tag('td')
			if fanhao.file_number:
				file_number_tag.string = str(fanhao.file_number)
			else:
				file_number_tag.string = '--'
			fanhao_tbody_tr.insert(4, file_number_tag)

			magnet_link_tag = soup.new_tag('td')
			magnet_link_tag['class'] = 'magnet'
			fanhao_tbody_tr.insert(5, magnet_link_tag)
			fanhao_magnet_td = fanhao_tbody_tr.find('td', attrs={'class': 'magnet'})
			magnet_link_a = soup.new_tag('a', href=fanhao.magnet_link)

			magnet_link_a.string = 'Download'
			magnet_link_a['class'] = 'btn btn-success'
			fanhao_magnet_td.insert(0, magnet_link_a)

			resource_tag = soup.new_tag('td')
			resource_tag.string = fanhao.source
			fanhao_tbody_tr.insert(6, resource_tag)

		return soup
