import math

class Color_Class:
	def rgb_to_hex(rgb):
	 	return '%02x%02x%02x' % rgb

class Color_Analysis:
	def Calculate_Mode_Count_RGB(image, middle, borderdistance):
		start = x,y = middle[0] - borderdistance, middle[1] - borderdistance
		RGBDic = {}
		for i in range(int(start[0]), int(start[0] + borderdistance*2)):
			for j in range(int(start[1]), int(start[1] + borderdistance*2)):
				pixel = i,j 
				RGB = r,g,b =image.getpixel(pixel)
				
				if RGB in RGBDic:
					RGBDic[RGB]+= 1
				else:
					RGBDic[RGB] = 1
		# return len(HSVDic)
		return len(RGBDic)	

	def within_rgb_frame(middle, topleft, topright, bottomleft, bottomright):
		#format r,g,b from each passed variable
		threshold = 15

		if abs(middle[0] - topleft[0]) <= threshold \
		and abs(middle[1] - topleft[1]) <= threshold \
		and abs(middle[2] - topleft[2]) <= threshold \
		and abs(middle[0] - topright[0]) <= threshold \
		and abs(middle[1] - topright[1]) <= threshold \
		and abs(middle[2] - topright[2]) <= threshold \
		and abs(middle[0] - bottomleft[0]) <= threshold \
		and abs(middle[1] - bottomleft[1]) <= threshold \
		and abs(middle[2] - bottomleft[2]) <= threshold \
		and abs(middle[0] - bottomright[0]) <= threshold \
		and abs(middle[1] - bottomright[1]) <= threshold \
		and abs(middle[2] - bottomright[2]) <= threshold :
			return True
		else:
			return False
	def AVG_Image_RGB(image, middle, borderdistance):
		start = x,y = middle[0] - borderdistance, middle[1] - borderdistance

		tot_r,tot_g,tot_b = 0,0,0

		for i in range(int(start[0]), int(start[0] + borderdistance*2)):
			for j in range(int(start[1]), int(start[1] + borderdistance*2)):
				pixel = i,j
				RGB = r,g,b = image.getpixel(pixel)
				tot_r += r
				tot_g += g
				tot_b += b
		surfacearea = borderdistance * borderdistance * 4
		RGBAvg = R,G,B = math.floor(tot_r/surfacearea), math.floor(tot_g/surfacearea), math.floor(tot_b/surfacearea)
		return RGBAvg

	def Calculate_Image_Box(image, middle):
		borderdistance = 100
		middlex, middley = middle[0],middle[1]
		width, height = image.size

		middlergb = image.getpixel((middlex,middley))
		topleftrgb =image.getpixel((max(1, middlex-borderdistance), max(1, middley - borderdistance)))
		toprightrgb = image.getpixel((min(width, middlex+borderdistance),max(1, middley-borderdistance)))
		bottomleftrgb = image.getpixel((max(1,middlex-borderdistance), min(height, middley+borderdistance)))
		bottomrightrgb = image.getpixel((min(width, middlex + borderdistance), min(height, middley + borderdistance)))
		
		if len(middlergb) != 3 or \
		len(topleftrgb) != 3 or \
		len(toprightrgb) != 3 or \
		len(bottomleftrgb) != 3 or \
		len(bottomrightrgb) != 3:
			print("Error")
			return 0

		#do middle and try for 150 up/down and 150 right/left
		#check if the hue is within 60 degrees if not then go down by 50 all direction
		while not Color_Analysis.within_rgb_frame(middlergb, topleftrgb, toprightrgb, bottomleftrgb, bottomrightrgb) \
			and borderdistance > 0:
			borderdistance -= 5
			topleftrgb =image.getpixel((max(1, middlex-borderdistance), max(1, middley - borderdistance)))
			toprightrgb = image.getpixel((min(width, middlex+borderdistance),max(1, middley-borderdistance)))
			bottomleftrgb = image.getpixel((max(1,middlex-borderdistance), min(height, middley+borderdistance)))
			bottomrightrgb = image.getpixel((min(width, middlex + borderdistance), min(height, middley + borderdistance)))
			
		return borderdistance
