###################################################################################################################
## flood_test.py
## GEOG 173 Final Project: Flood Modeling
## Script Description: Takes input volume and projects affected flood area
#################################################################################################################

import arcpy
from arcpy import env
from arcpy.sa import *
folder_path = "~/Developer/geog173/data/"
arcpy.env.workspace = folder_path
arcpy.env.overwriteOutput = True

#####CHECK FOR LICENSES AND PROMPT TO ENABLE IF UNAVAILABLE############


########################## User Inputs ################################

#1: DEM (RASTER)
dem_raster_object = "dempath.tif"

#2: Water Volume (m^3) (DOUBLE)
water_volume = NUMBER

#3: Initital Threshold Value (m) (DOUBLE)
initial_height_change = NUMBER

#4: {Area of Interest (Extent/Polygon)}
interest_polygon = "shapfile.shp"
extent = Extent({XMin}, {YMin}, {XMax}, {YMax}, {ZMin}, {ZMax}, {MMin}, {MMax})

#5: Projection Selection With UTM Zone Selection
dem_project = "demproject.tif"
project_in_raster = dem
project_out_raster = dem_project
coordinate_system_project = "string"
arcpy.ProjectRaster_management(project_in_raster, project_out_raster, coordinate_system_project)

#6: Clipped DEM Output Location
clipped_dem_path = "demclip.tif"

#7: Reclassified Raster Output Location
reclassify_dem_path = "demreclass.tif"

################### STEP 1: DEM Data Management #############################
#Fill DEM???
#demfill = Fill(dem, z-value)

#Clip DEM To Basin / User Defined Extent (Either Shapefile or Extent Values)
#clipped_DEM = ExtractByMask(dem, interest_polygon)
#clipped_DEM.save(clipped_dem_path)

#Ensure Raster is Integer Format to Create Attribute Table
dem_raster_object = arcpy.sa.Int(dem_raster_object)

#Get Cell Width & Height
cell_width = dem_raster_object.meanCellWidth
cell_height = dem_raster_object.meanCellHeight

#Cell Area in m^2
cell_area = cell_width*cell_height

#Minimum and Maximum of Raster
dem_minimum = dem_raster_object.minimum
dem_maximum = dem_raster_object.maximum
threshold = dem_minimum + initial_height_change

################## BEGIN MAJOR LOOP ##############################

""" While (-5 < Y < 5) DO:
	1) 
	2)
	3)
"""
#Volume Differential (Y) [m^3] [Global Variable]
volume_differential = 20
while volume_differential > 5 or volume_differential < -5:
	threshold_reclass = threshold + .0000001
	reclassify_remap = RemapRange([[dem_minimum, threshold, 0],[threshold, dem_maximum, 1], ["NODATA", "NODATA", 1]])
	reclassify_dem = Reclassify(dem_raster_object, "Value", reclassify_remap)
	setnull_dem = SetNull(reclassify_dem, dem_raster_object, "Value = 1")
	setnull_dem_mean = setnull_dem.mean
	area_search = arcpy.SearchCursor(reclassify_dem)
	for row in area_search:
		if row.VALUE == 0:
			count = row.COUNT

	#Area in m^2
	area = count*cell_area

	#Delete Search Cursor
	del area_search

	#Get Delta H
	height_change = threshold - setnull_dem_mean

	volume = height_change * area

	volume_differential = water_volume - volume

	if volume_differential < 0:
		threshold -= 1
	elif volume_differential > 0:
		threshold += 1

print volume
print area
print setnull_dem_mean

arcpy.RasterToPolygon_conversion(reclassify_dem, area_shapefile_path)

area_shapefile = area_shapefile_path

arcpy.SelectLayerByAttribute(area_shapefile, "NEW_SELECTION", ' "GRIDCODE" = 0 ')

arcpy.CopyFeatures_management(area_shapefile, selected_area_shapefile_path)

#APPEND FIELDS & ATTRIBUTE DATA TO EXPORTED SHAPEFILE

#PRODUCE A MAP BOOK

import os

mxd = arcpy.mapping.MapDocument(folder_path + "file_name.mxd")
data_frame = arcpy.mapping.ListDataFrames(mxd)[0]
list_layers = arcpy.mapping.ListLayers(mxd,"", data_frame)

#Final and temporary pdf set up

finalPDF_filename = folder_path + "/file_name.pdf"

if os.path.exists(finalPDF_filename):
    os.remove(finalPDF_filename)

finalPDF = arcpy.mapping.PDFDocumentCreate(finalPDF_filename)

tempPDF = folder_path+"/temp.pdf"

#Title page with names
#We can save the mxd orginally with all of the layers turned off and the title we'd like. OR:

for lyr in list_layers:
	lyr.visible = False
	arcpy.RefreshActiveView()

element = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[0]
element.text = "Title and our names here"

mxd.save()

if os.path.exists(tempPDF):
    os.remove(tempPDF)
    
arcpy.mapping.ExportToPDF(mxd,tempPDF)
finalPDF.appendPages(tempPDF)

if os.path.exists(tempPDF):
    os.remove(tempPDF)

#Reclassified DEM

#Turn on the reclassified DEM

data_frame = arcpy.mapping.ListDataFrames(mxd)[0]

for lyr in list_layers:
	if lyr.isRasterLayer = True:
		lyr.visible = True
	arcpy.RefreshActiveView()

element = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[0]
element.text = "Title of this page"

mxd.save()

if os.path.exists(tempPDF):
    os.remove(tempPDF)
    
arcpy.mapping.ExportToPDF(mxd,tempPDF)
finalPDF.appendPages(tempPDF)

#Polygon shapefile

data_frame = arcpy.mapping.ListDataFrames(mxd)[0]

for lyr in list_layers:
	if lyr.isFeatureLayer = True:
		lyr.visible = True
	arcpy.RefreshActiveView()

element = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[0]
element.text = "Title of this page"

#Repeat for any additional pages we want. We can also index layers if we want to do more than one shapefile or raster.
