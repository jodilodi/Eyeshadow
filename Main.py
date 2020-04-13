#scrap temptalia brands and check if mongodb has it already, if not insert

from html_scraping import Temptalia_Scrapping
from demo_mongodb_test import Makeup_MongoDB
from os import system, name
from subprocess import call
import os
import io
from PIL import Image
from array import array

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

def Insert_New_Eyeshadows():
	branddata = Makeup_MongoDB.Get_Makeup_DB_After("Kevyn Aucoin")
	for brand in branddata:
		print(brand)
		totalpages = Temptalia_Scrapping.Get_Nav_Pages(brand["temptalia_id"])
		alleyeshadows = []
		for pageindex in range(1, totalpages + 1):
		#for pageindex in range(1,2):
			alleyeshadows = alleyeshadows + Temptalia_Scrapping.Get_Eyeshadow(brand["name"], brand["temptalia_id"], pageindex)

		for eyeshadow in alleyeshadows:
			exist = Makeup_MongoDB.Contain_Eyeshadow(eyeshadow.brand, eyeshadow.name)
			if not exist:
				insertid = Makeup_MongoDB.Insert_Eyeshadow(eyeshadow)
				print(insertid)
			else:
				print("Added")

def Welcome_Screen():
	print('###########################################')
	print('##   Welcome to Temptalia Eyeshadow DB   ##')
	print('###########################################')

def Print_Menu():
	print('Menu')
	print('1. Exit')
	print('2. Delete Brands Collection')
	print('3. Screen Scrap Brands')
	print('4. Delete Eyeshadows Colelction')
	print('5. Screen Scrap Eyeshadows')
	print('6. Print All Eyeshadows')
	print('7. Convert Eyeshadow Byte To Img')
	print('8. Test')

if __name__ == "__main__":
	clear()
	Welcome_Screen()
	Print_Menu()
	while True:
		user_input = input('What would you like to do? ')
		if user_input == "Menu" or user_input=="menu":
			Print_Menu()
		elif user_input == "1" or user_input == "Exit" or user_input == "exit" or user_input == "quit":
			print('Goodbye!')
			break
		elif user_input == "2":
			Makeup_MongoDB.Delete_Brands_Collection()
			print('Deleted all brands from MongoDB')
		elif user_input == "3":
			print('Inserting Brands')
			Insert_New_Brands()
		elif user_input == "4":
			Makeup_MongoDB.Delete_Eyeshadow_Collection()
		elif user_input == "5":
			Insert_New_Eyeshadows()
		elif user_input == "6":
			Eyeshadows = Makeup_MongoDB.Get_All_Eyeshadows()
			for es in Eyeshadows:
				print(es)
		elif user_input == "7":
		 	Eyeshadows = Makeup_MongoDB.Get_All_Eyeshadows("BH Cosmetics")
		 	for i in range(0,10):
		 		eyeshadow = Eyeshadows[i]
		 		#print(eyeshadow["byte"])
		 		image = Image.open(io.BytesIO(eyeshadow["byte"]))
		 		#print(image.size)
		 		image.save(str(i) + ".jpg")
		

