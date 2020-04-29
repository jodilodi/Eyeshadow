#scrap temptalia brands and check if mongodb has it already, if not insert

from html_scraping import Temptalia_Scrapping
from mongodb import Makeup_MongoDB
from color_analyse import Color_Class
from color_analyse import Color_Analysis
from write_results import Write_Results_Class
from os import system, name
from subprocess import call
import os
import io
from PIL import Image
from array import array
import sys
import math
import time
#~/.bashrc or ~/.bash_aliases
#alias python=python3
#run source ~/.bashrc or source ~/.bash_aliases

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

def Calculate_RGB(filename):
	Brands = Makeup_MongoDB.Get_All_Brands()
	fieldnames = ["Brand", "FoundIn", "Name", "MiddleRGB", "AvgRGB","ModeCount", "ModeRGB","MinRGB", "MaxRGB", "ColorRGB", "ColorAvgRGB", "ColorModeRGB" ]
	Write_Results_Class.Write_To_XSLX_Title(fieldnames, filename)
	for brand in Brands:
		print(brand)
		Eyeshadows = Makeup_MongoDB.Get_All_Eyeshadows_By_Brand(brand["name"])
		#check four corners and middle
		count = 0
		errorcolors = []
		error = 0
		colorRows = []
		for eyeshadow in Eyeshadows:
			print(eyeshadow["name"])
			try: 
				image = Image.open(io.BytesIO(eyeshadow["byte"]))
			except:
				count+= 1
				errorcolors.append(eyeshadow["name"])
				continue	

			width, height = image.size
			middle = middlex, middley = height/2, width/2
			middlergb = image.getpixel(middle)
			#borderdistance = Calculate_Image_Box(image, middle, middlehsv)
			borderdistance = Color_Analysis.Calculate_Image_Box(image, middle);

			if borderdistance == 0:
				count += 1
				errorcolors.append(eyeshadow["name"])
			else:
			 	results = Color_Analysis.AVG_Image_RGB(image, middle, borderdistance)
			 	MIN, MAX = Color_Analysis.Min_Max_RGB(image, middle, borderdistance)
			 	ModeCount, ModeRGB = Color_Analysis.Calculate_Mode_RGB(image,middle, borderdistance)
			 	RowDict = {}
			 	RowDict["Brand"] = eyeshadow["brand"]
			 	RowDict["FoundIn"] = eyeshadow["foundin"]
			 	RowDict["Name"] = eyeshadow["name"]
			 	RowDict["MiddleRGB"] = middlergb
			 	RowDict["AvgRGB"] = results
			 	RowDict["ModeCount"] = ModeCount
			 	RowDict["ModeRGB"] =  ModeRGB
			 	RowDict["MinRGB"] = MIN
			 	RowDict["MaxRGB"] = MAX
			 	colorRows.append(RowDict)
		print('writing brand to excel')	
		Write_Results_Class.Write_To_XSLX_RGB(colorRows, filename)
	print("Total " + str(count))
	print(errorcolors)
	print("Error " + str(error))
	Write_Results_Class.Write_To_CSV(fieldnames, colorRows)

	#workbook.close()

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
	print('9. Copy Collection')

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
		 	Eyeshadows = Makeup_MongoDB.Get_All_Eyeshadows()
		 	#put everything in brands folder first
		 	if not os.path.isdir("Brands"):
		 		os.mkdir("Brands")

		 	for eyeshadow in Eyeshadows:
		 		brand = eyeshadow["brand"]
		 		filepath = "Brands/{0}".format(brand)
		 		if not os.path.isdir(filepath):
		 			os.mkdir(filepath)
		 		try:
		 			image = Image.open(io.BytesIO(eyeshadow["byte"]))
			 		image.save(filepath + "/" + eyeshadow["name"] + ".jpg")
			 		print("Saved " + eyeshadow["name"] + ".jpg")
			 	except:
			 		print("Could not save " + eyeshadow["name"] + ".jpg")
		elif user_input == "8":
			filename = input("Enter Results File Name (Default is Results):")
			if len(filename) == 0:
				filename = "Results"
			filename = "{0}.xlsx".format(filename)
			
			Calculate_RGB(filename)
		elif user_input == "9":
			from_collection = input('From Collection: ')
			to_collection = input('To Collection: ')
			Makeup_MongoDB.Copy_Collection(from_collection, to_collection)
			print('Complete Copying Collection')
		# elif user_input == "reset":
		# 	os.execl(sys.executable, 'python', "Main.py")
		elif user_input == "reset":
			python = sys.executable
			os.execl(python, python, * sys.argv)