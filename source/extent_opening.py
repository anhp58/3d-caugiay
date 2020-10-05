import arcpy
import os

extra_deg = [0.00013]
extra_met = ["25m"]


def toCSV (lat_long_list, mycsv):
	import csv

	with open(mycsv, 'wb') as myfile:
	    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	    for row in lat_long_list:
	    	wr.writerow(row)

def getExt (filename, extra_deg):

	rows = arcpy.SearchCursor(filename)
	shapeName = arcpy.Describe(filename).shapeFieldName
	lat_long_list = []
	head_row = ['bot_lat', 'top_lat', 'left_long', 'right_long']
	lat_long_list.append(head_row)

	for row in rows:
		feat = row.getValue(shapeName)
		extent = feat.extent 
		bot_lat = extent.YMin - extra_deg
		top_lat = extent.YMax + extra_deg
		left_long = extent.XMin - extra_deg
		right_long = extent.XMax + extra_deg
		# height = row.chieucao

		lat_long_list.append([bot_lat, top_lat, left_long, right_long])

	return lat_long_list

base_dir_shp = r"I:\My Drive\3D-Caugiay\roi\new\corrected_shp"
# base_dir_csv = r"I:\My Drive\3D-Caugiay\small_img_org"
# filename = ["1.1", "1.2", "1.3", "5.1", "6.1", "6.2", "6.3"]

# for deg, met in zip(extra_deg, extra_met):
# 	for index in range (0, len(filename[0])):
# 		print (index)
# 		mycsv = os.path.join(base_dir_csv, "{}_extent_{}.csv".format(filename[0], extra_met))
# 		lat_long_list = getExt(os.path.join(base_dir_shp, "{}.shp".format(filename[0])), deg)
# 		toCSV(lat_long_list, mycsv)

# print ("ok")

rows = arcpy.SearchCursor(os.path.join(base_dir_shp, "1.1.shp"))