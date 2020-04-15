#scrap temptalia brands and check if mongodb has it already, if not insert

from html_scraping import Temptalia_Scrapping
from mongodb import Makeup_MongoDB
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
	branddata = Makeup_MongoDB.Get_Makeup_DB_After("Makeup Atelier")
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

def rgb_to_hsv(RGB):
	r, g, b = RGB[0]/255.0, RGB[1]/255.0, RGB[2]/255.0
	mx = max(r, g, b)
	mn = min(r, g, b)
	df = mx-mn
	if mx == mn:
	    h = 0
	elif mx == r:
	    h = (60 * ((g-b)/df) + 360) % 360
	elif mx == g:
	    h = (60 * ((b-r)/df) + 120) % 360
	elif mx == b:
	    h = (60 * ((r-g)/df) + 240) % 360
	if mx == 0:
	    s = 0
	else:
	    s = (df/mx)*100
	v = mx*100
	return int(round(h)), int(round(s)), int(round(v))


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
	print('8. Test Pixel Colors')

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
		 	Eyeshadows = Makeup_MongoDB.Get_All_Eyeshadows("Huda Beauty")
		 	for eyeshadow in Eyeshadows:
		 		brand = eyeshadow["brand"]
		 		if not os.path.isdir(brand):
		 			os.mkdir(brand)
		 		try:
		 			image = Image.open(io.BytesIO(eyeshadow["byte"]))
			 		image.save(brand + "/" + eyeshadow["name"] + ".jpg")
			 		print("Saved " + eyeshadow["name"] + ".jpg")
			 	except:
			 		print("Could not save " + eyeshadow["name"] + ".jpg")
		elif user_input == "8":
			Eyeshadows = Makeup_MongoDB.Get_All_Eyeshadows("LORAC")
			#check four corners and middle
			for i in range(0,10):
				eyeshadow = Eyeshadows[i]
				print(eyeshadow["name"])
				image = Image.open(io.BytesIO(eyeshadow["byte"]))
				
				width, height = image.size

				topleft = x,y = 1,1
				print(image.getpixel(topleft))
				print(rgb_to_hsv(image.getpixel(topleft)))

				topright = 1, width -1 
				print(image.getpixel(topright))

				middle = height/2, width/2
				middlecolor = r,g,b = image.getpixel(middle)
				print(image.getpixel(middle))

				print(rgb_to_hsv(middlecolor))



