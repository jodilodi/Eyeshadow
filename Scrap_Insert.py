#scrap temptalia brands and check if mongodb has it already, if not insert

from html_scraping import Temptalia_Scrapping
from demo_mongodb_test import Makeup_MongoDB
from os import system, name
from subprocess import call
import os
def Insert_New_Brands():

	print("Get all brands from Temptalia")
	AllBrands = Temptalia_Scrapping.Get_Brands()
	#print(AllBrands)
	#print(Makeup_MongoDB.Contain_Brand(AllBrands[0]))

	print("Check if brand is already in db and insert")
	for brand in AllBrands:
		print(brand.name)
		brand_exist = Makeup_MongoDB.Contain_Brand(brand.name, brand.id)
		if not brand_exist:
			insertid = Makeup_MongoDB.Insert_Brand(brand.name, brand.id)
			print(insertid)
		else:
			print("exists")

def clear():
	_ = call('clear' if os.name == 'posix' else 'cls')

if __name__ == "__main__":
	clear()

	#For Testing
	# print(Makeup_MongoDB.Contain_Brand("Wet 'n' Wild",'1'))

	# rows = Makeup_MongoDB.Get_Makeup_DB()

	# for x in rows:
	# 	print(x)


	#For Reset
	#Makeup_MongoDB.Delete_Makeup_DB()

	#Insert new brand names
	#Insert_New_Brands()

	#insert all eyeshadows
	branddata = Makeup_MongoDB.Get_Makeup_DB_After("Ole Henriksen")
	for x in branddata:
		print(x)
		totalpages = Temptalia_Scrapping.Get_Nav_Pages(x["temptalia_id"])
		alleyeshadows = []
		for pageindex in range(1, totalpages + 1):
		#for pageindex in range(1,2):
			alleyeshadows = alleyeshadows + Temptalia_Scrapping.Get_Eyeshadow(x["name"], x["temptalia_id"], pageindex)

		# for eyeshadow in alleyeshadows:
		# 	print(eyeshadow.name)
		# 	print(eyeshadow.src)
		# for i in range(0,10):
		# 	eyeshadow = alleyeshadows[i]
		for eyeshadow in alleyeshadows:
			exist = Makeup_MongoDB.Contain_Eyeshadow(eyeshadow.brand, eyeshadow.name)
			if not exist:
				insertid = Makeup_MongoDB.Insert_Eyeshadow(eyeshadow)
				print(insertid)
			else:
				print("exists")



