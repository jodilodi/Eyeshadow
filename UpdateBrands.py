from html_scraping import Temptalia_Scrapping
from demo_mongodb_test import Makeup_MongoDB
from os import system, name
from subprocess import call
import os

if __name__ == "__main__":
	#update brands and see if each brand has eyeshadows, if they do then set the 
	#mongodb row

	# branddata = Makeup_MongoDB.Get_Makeup_DB()
	# for brand in branddata:
	# 	print(brand)
	# 	update = {"HasEyeshadows": False}
	# 	if Temptalia_Scrapping.Brand_Contains_Eyeshadow(brand["temptalia_id"]):
	# 		#set update query to say brand contains eyeshadows
	# 		update = {"HasEyeshadows": True}
	# 	Makeup_MongoDB.Update_Brand(brand["temptalia_id"], update)


	# branddata = Makeup_MongoDB.Get_Makeup_DB()
	# for brand in branddata:
	# 	print(brand)