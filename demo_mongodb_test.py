import pymongo

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

	def Insert_Brand(brand_name, brand_id):
		mydict = {"name": brand_name, "temptalia_id": brand_id}
		x = Makeup_MongoDB.mybrands.insert_one(mydict)
		return x.inserted_id

	def Get_Makeup_DB():
		return Makeup_MongoDB.mybrands.find({})

	def Get_Makeup_DB_After(brand_name):
		return Makeup_MongoDB.mybrands.find({"name": { "$gte": brand_name}}).sort("name")

	def Delete_Makeup_DB():
		Makeup_MongoDB.mybrands.delete_many({})

	def Get_Makeup_Brand(brand_name):
		myquery = {"name": brand_name}
		mydoc = Makeup_MongoDB.mybrands.find(myquery)
		return mydoc

	def Contain_Eyeshadow(brand_name, eyeshadow):
		myquery = {"name": eyeshadow, "brand": brand_name}
		mydoc = Makeup_MongoDB.myeyeshadow.find(myquery)

		if mydoc.count() > 0 :
			return True
		else:
			return False

	def Insert_Eyeshadow(eyeshadow_class):
		eyeshadowvalues = {key:value for key, value in eyeshadow_class.__dict__.items() if not key.startswith('__') and not callable(key)}
		x = Makeup_MongoDB.myeyeshadow.insert_one(eyeshadowvalues)
		return x.inserted_id



