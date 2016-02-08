import shapefile 
import datetime
import os

#open zoning districts shape file
sf = shapefile.Reader("/Users/Taha/Downloads/Zoning/Zoning_Districts.shp") 

#get all the records
records = sf.records()

#get all the attribute names
field = sf.fields 

n=0
file_attr = []
#iterate over attributes to print out the index number and attribute name for user to select
for f in field:
	print str(n) + ')', f[0]
	n = n + 1
	#save attriubutes to be used later in org2org command via index number (user's input)
	file_attr.append(f[0])

#once the attributes are listed above, the user has an option to enter which attriubute will be used for filtering
attr = raw_input("Please enter number of the attribute to be filtered: ")
if attr:
	attr_index = int(attr)
	if 0 <= attr_index <= 5:
		#asking user to enter the value for filtering
		user_value = raw_input("Please enter attribute value for filtering (e.g Community Business or Commercial or Public: ")
		if user_value:
			#get the attribute name from user's input
			attribute_filter = file_attr[attr_index]
			
			#creating a string for where command for filtering
			filter_command_string = attribute_filter + ' like "%'+user_value+'%" ' 
			
			#get timestamp to save a unique geojson file
			now = datetime.datetime.now()
			file_name = str(now.strftime("%Y-%m-%d %H:%M:%S").replace(" ","-")).replace(":","-")
			
			#run ogr2ogr command line to save shapefile as geojson projected as EPSG:4326 and filter out user's query
			command_string = "ogr2ogr -f GeoJSON -t_srs EPSG:4326 sf-"+file_name+".geojson -where '" + filter_command_string +"' Zoning_Districts.shp"
			# print command_string
			os.system(command_string)




