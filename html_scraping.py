#HTML Scraping
# from lxml import html
# import requests

# page = requests.get('https://www.temptalia.com/p/_brands/')
# tree = html.fromstring(page.content)

# #brands = tree.xpath('//select[@id="filter_brand"]')
# brands = tree.xpath('//option/text()')
# print(brands)
# print(len(brands))

from bs4 import BeautifulSoup
import requests
import re

import sys

#error handling

#image stuff
from PIL import Image
from io import BytesIO

class Brand:
	def __init__(self, name, id):
		self.name = name
		self.id = id

class Eyeshadow:
	def __init__(self, name, imgsrc, src, foundin, grade, brand, finish):
		self.name = name
		self.imgsrc = imgsrc
		response = requests.get(imgsrc, timeout=5)
		self.byte = BytesIO(response.content).getvalue()
		self.src = src
		self.foundin = foundin
		self.temptaliagrade = grade
		self.brand = brand
		self.finish = finish

class Temptalia_Scrapping:

	def Get_Brands():
		url = "https://www.temptalia.com/p/_brands/"
		r = requests.get(url, timeout=5)
		html_doc = r.text
		soup = BeautifulSoup(html_doc, 'html.parser')

		#will print out all of the brands that temptalia has reviewed or mentioned
		# for option in soup.find(id='filter_brand'):
		# 	try:
		# 		if "Select" not in option.get_text() and "All Brands" not in option.get_text(): 
		# 			print(option.get_text())
		# 	except:
		# 		continue

		brands = []
		for option in soup.find(id = 'filter_brand'):
			try:
				if "Select" not in option.get_text() and "All Brands" not in option.get_text(): 
					#brands.append(option.get_text())
					brands.append(Brand(option.get_text(), option['value']))
			except:
				continue

		return brands

	def Brand_Contains_Eyeshadow(id):
		url = r"https://www.temptalia.com/product/page/1/?f_formula_search&f_formula=0&t%%5B0%%5D=12674&brand=%s&time=all&sorting=date_desc&archive=rated" % (id)
		try:
			r = requests.get(url, timeout=10)
		except:
			return True #dunno, false positive is better than false negative

		html_doc = r.text
		soup = BeautifulSoup(html_doc, 'html.parser')

		elements = soup.find_all("div", class_="alert alert-danger my-5 f-4 sans-serif text-center")
		if len(elements) == 0:
			#there is not warning for not eyeshadows 
			return True
		else:
			return False


	def Print_Brands():
		url = "https://www.temptalia.com/p/_brands/"
		r = requests.get(url, timeout=5)
		html_doc = r.text
		soup = BeautifulSoup(html_doc, 'html.parser')

		for option in soup.find(id = 'filter_brand'):
			print(option)
			print(option.get_text())
			print(option['value'])
	
	def Get_Available_In_Palette(url):
		try:
			r = requests.get(url, timeout=5)
			html_doc = r.text
			soup = BeautifulSoup(html_doc, 'html.parser')

			section = soup.find(id="sectionAvailable")

			#section 
			if section is None:
				return "Single"
			else:
				title = section.find("h4", class_="f-2 mb-0 regular text-uppercase").text
				return str.rstrip(title)
		except:
			return "Unknown"
		
	def Get_Eyeshadow_Rank(url):
		try:
			r = requests.get(url, timeout=5)
			html_doc = r.text
			soup = BeautifulSoup(html_doc, 'html.parser')
			# grade = soup.find("div", class_="glossover-grade large py-4").text
			gradebox = soup.find("div", class_="glossover-grade large py-4")
			if gradebox is None:
				return ""
			else:
				return gradebox.text
		except:
			return ""
	def Get_Eyeshadow_Finish(url):
		try:
			print(url)
			r = requests.get(url, timeout = 5)
			html_doc = r.text
			soup = BeautifulSoup(html_doc, 'html.parser')

			description = "none"
			for tag in soup.find_all("meta"):
				if tag.get("name", None) == "twitter:description":
					description = tag["content"]

			desSplit = description.split(" ")
			findex = 0
			try:
				findex = desSplit.index('finish')
			except:
				findex = desSplit.index('finish.')
			print(desSplit[findex-1])
			return desSplit[findex - 1]
		except:
			print(sys.exc_info()[0])
			return -1

	def Get_Eyeshadow(brand, id, pageindex):
		#brand, type is eyeshadow, date rangeis set to all time
		#https://www.temptalia.com/product/page/1/?f_formula_search&f_formula=0&t%%5B0%%5D=12674&brand=%s&time=all&sorting=date_desc&archive=rated
		url = r"https://www.temptalia.com/product/page/%s/?f_formula_search&f_formula=0&t%%5B0%%5D=12674&brand=%s&time=all&sorting=date_desc&archive=rated" % (pageindex, id)
		try:
			r = requests.get(url, timeout=10)
		except:
			print("Get Eyeshadow Page Error")
			return []
		html_doc = r.text
		soup = BeautifulSoup(html_doc, 'html.parser')
		
		eyeshadowcolors = []
		for element in soup.find_all("div", class_="display-badge"):#, class_="display-badge product product-archive"):
			try:
				#get the biggest image for the color
				allimg = element.find("img", class_="img-fluid").get('data-lazy-srcset')
				img_array = allimg.split(",")
				img = img_array[len(img_array)-1].strip()
				img = img[0:img.find(' ')]
				colorName = element.find("h5", class_="f-3 text-base text-ellipsis m-0").text
				src = element.find("h5", class_="f-3 text-base text-ellipsis m-0").find("a").get("href")
				foundin = Temptalia_Scrapping.Get_Available_In_Palette(src)
				grade = Temptalia_Scrapping.Get_Eyeshadow_Rank(src)
				finish = Temptalia_Scrapping.Get_Eyeshadow_Finish(src)
				eyeshadowcolors.append(Eyeshadow(colorName, img, src, foundin, grade, brand, finish))
				print(colorName)
			except:
				print("Error in adding eyeshadow")
				print(sys.exc_info()[0])
				continue
		return eyeshadowcolors

	
	def Get_Nav_Pages(id):
		url = r"https://www.temptalia.com/product/page/1/?f_formula_search&f_formula=0&t%%5B0%%5D=12674&brand=%s&time=all&sorting=date_desc&archive=rated" % id
		try:
			r = requests.get(url, timeout=5)
			html_doc = r.text
			soup = BeautifulSoup(html_doc, 'html.parser')


			maxpage = 1
			for pages in soup.find_all(True, class_="page-link" ):
				try:
					maxpage = max(maxpage, int(pages.text))
				except ValueError:
					continue

			return maxpage
		except:
			return 1

	







