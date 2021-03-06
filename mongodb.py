import pymongo
from html_scraping import Temptalia_Scrapping

#to view mongo db running in the background ps aux | grep -v grep | grep mongod

class Makeup_MongoDB:
	myclient = pymongo.MongoClient('mongodb://localhost:27017/')
	#create db / call it out
	mydb = myclient["Makeup_DB"]
	mybrands = mydb["Brands"]

	myeyeshadow = mydb["Eyeshadow"]

	#does mongodb in brands contain this particular brand
	def Contain_Brand(brand_name, brand_id):
		myquery = {"name": brand_name, "id": brand_id}
		mydoc = Makeup_MongoDB.mybrands.find(myquery)

		#if there is an a record that means that the db has the brand already
		if mydoc.count() > 0 :
			return True
		else:
			return False

	#insert name, temptalia_id, has_eyeshadow (flag) to mongodb Brands
	def Insert_Brand(brand_name, brand_id):
		mydict = {"name": brand_name, "temptalia_id": brand_id}
		if Temptalia_Scrapping.Brand_Contains_Eyeshadow(brand_id):
			mydict["has_eyeshadow"] = True
		else:
			mydict["has_eyeshadow"] = False
		x = Makeup_MongoDB.mybrands.insert_one(mydict)
		return x.inserted_id

	#return all brands in mongodb Brands
	#def Get_Makeup_DB():
	#	return Makeup_MongoDB.mybrands.find({"has_eyeshadow": True}).limit(10)

	def Get_Makeup_DB_One(brand_name):
		return Makeup_MongoDB.mybrands.find({"name": brand_name})

	#return all brands in mongodb Brands >= passed value
	#has_eyeshadow flag not working! need to fix
	def Get_Makeup_DB_After(brand_name):
		return Makeup_MongoDB.mybrands.find({"name": { "$gte": brand_name}, "has_eyeshadow": True}).sort("name")

	#delete Brands mongodb
	def Delete_Brands_Collection():
		Makeup_MongoDB.mybrands.delete_many({})

	#delete Eyeshadow mongodb
	def Delete_Eyeshadow_Collection():
		Makeup_MongoDB.myeyeshadow.delete_many({})

	#return specific object
	def Get_Makeup_Brand(brand_name):
		myquery = {"name": brand_name}
		mydoc = Makeup_MongoDB.mybrands.find(myquery)
		return mydoc

	#check if the eyeshadow is already in the collection
	def Contain_Eyeshadow(brand_name, eyeshadow):
		myquery = {"name": eyeshadow, "brand": brand_name}
		mydoc = Makeup_MongoDB.myeyeshadow.find(myquery)

		if mydoc.count() > 0 :
			return True
		else:
			return False

	#add eyeshadow
	def Insert_Eyeshadow(eyeshadow_class):
		eyeshadowvalues = {key:value for key, value in eyeshadow_class.__dict__.items() if not key.startswith('__') and not callable(key)}
		x = Makeup_MongoDB.myeyeshadow.insert_one(eyeshadowvalues)
		return x.inserted_id

	def Get_All_Eyeshadows():
		return Makeup_MongoDB.myeyeshadow.find({})

	def Get_All_Eyeshadows_By_Brand(brand):
		return Makeup_MongoDB.myeyeshadow.find({"brand": brand})#.sort("name")

	def Get_Eyeshadow(id):
		return Makeup_MongoDB.myeyeshadow.find({"_id": id})

	def Copy_Collection(from_collection, to_collection):
		fromcollection = Makeup_MongoDB.mydb[from_collection].find({})
		tocollection = Makeup_MongoDB.mydb[to_collection]
		for item in fromcollection:
			myid = tocollection.insert_one(item)
			print(myid)
		#myid = tocollection.insertMany(fromcollection)

	def Get_All_Brands():
		return Makeup_MongoDB.mybrands.find({"has_eyeshadow": True})#.limit(5)

	def Update_Eyeshadow_Finish(brand_name, eyeshadow_name, finish_value):
		# test find and modify from mongodb
		query = {"brand" : brand_name, "name": eyeshadow_name }
		update = {"$set": {"finish" : finish_value}}
		Makeup_MongoDB.myeyeshadow.find_one_and_update(
			query,
			update
			)
