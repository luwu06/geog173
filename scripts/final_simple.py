import arcpy
from arcpy import env
from arcpy.sa import *
folder_path = "C:\Users\mr076923\Desktop\Lab6"
arcpy.env.workspace = folder_path
arcpy.env.overwriteOutput = True

dem_raster_object = Raster("DEM.tif")

water_volume = 1000000000

initial_height_change = 30

volume_differential = 50000000000

dem_raster_object = arcpy.sa.Int(dem_raster_object)

cell_width = dem_raster_object.meanCellWidth
cell_height = dem_raster_object.meanCellHeight
cell_area = cell_width * cell_height

dem_minimum = dem_raster_object.minimum
dem_maximum = dem_raster_object.maximum

threshold = dem_minimum + initial_height_change

while volume_differential > 5000 or volume_differential < -5000:
    threshold_reclass = threshold + .0000001
    reclassify_remap = RemapRange([[dem_minimum, threshold, 0],[threshold, dem_maximum, 1],["NODATA","NODATA",1]])
    reclassify_dem = Reclassify(dem_raster_object, "Value", reclassify_remap)
    setnull_dem = SetNull(reclassify_dem, dem_raster_object, "VALUE = 1")
    setnull_dem_mean = setnull_dem.mean
    area_search = arcpy.SearchCursor(reclassify_dem)

    for row in area_search:
        if row.VALUE == 0:
            count = row.COUNT

    area = count*cell_area

    del area_search

    height_change = threshold - setnull_dem_mean

    volume = height_change * area
	
    volume_differential = water_volume - volume
    print volume_differential
    if volume_differential < 0:
        threshold -= .5
    elif volume_differential > 0:
        threshold += .5

print volume
print area
print setnull_dem_mean

arcpy.RasterToPolygon_conversion(reclassify_dem, area_shapefile_path)

area_shapefile = area_shapefile_path

arcpy.SelectLayerByAttribute(area_shapefile, "NEW_SELECTION", ' "GRIDCODE" = 0 ')

arcpy.CopyFeatures_management(area_shapefile, selected_area_shapefile_path)

#APPEND FIELDS & ATTRIBUTE DATA TO EXPORTED SHAPEFILE