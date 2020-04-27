import csv
from openpyxl import Workbook
import openpyxl
from openpyxl.styles import PatternFill
from color_analyse import Color_Class
from color_analyse import Color_Analysis

class Write_Results_Class:
	def Write_To_CSV(fieldnames, data ):
		with open('results.csv', 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
			writer.writeheader()
			for datarow in data:
				writer.writerow(datarow)

	def Write_To_XSLX_Title(fieldnames, filename):
		workbook = Workbook()
		worksheet = workbook.create_sheet('EyeshadowSheet')


		# workbook.remove_sheet(workbook['Sheet'])
		workbook.remove(workbook['Sheet'])
		row = 1
		col = 1
		for name in fieldnames:
			worksheet.cell(row=row, column = col, value = name)
			col += 1
		workbook.save(filename)

	def Write_To_XSLX_RGB(data, filename):
		workbook = openpyxl.load_workbook(filename = filename)
		worksheet = workbook['EyeshadowSheet']
		for datarow in data:
			col = 1
			row = worksheet.max_row + 1
			for datacell in datarow:
				worksheet.cell(row=row, column=col, value=str(datarow[datacell]))
				col += 1

			# MiddleHSV = datarow["MiddleHSV"]
			# rgb = Color_Class.hsv_to_rgb(MiddleHSV[0],MiddleHSV[1], MiddleHSV[2])
			rgb = datarow["MiddleRGB"]
			color = '{0}'.format(Color_Class.rgb_to_hex(rgb))
			a1 = worksheet[row][col-1]
			a1.fill  = PatternFill(start_color=color, fill_type="solid")

			# AvgHSV = datarow["AvgHSV"]
			# rgb = Color_Class.hsv_to_rgb(AvgHSV[0], AvgHSV[1], AvgHSV[2])
			rgb = datarow["AvgRGB"]
			color = '{0}'.format(Color_Class.rgb_to_hex(rgb))
			
			a2 = worksheet[row][col]
			a2.fill = PatternFill(start_color=color, fill_type="solid")
			
		#workbook.close()
		workbook.save('results.xlsx')