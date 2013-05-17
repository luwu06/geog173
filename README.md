Geography 173 Final Project
=======
PROGRESS REPORT
Tibet Basin/Watershed:

Requires 3 user inputs:
  DEM of topography
  Threshold elevation
  Volume of water that would flood into topography/area of interest

Clip (spatial analysis) basin shapefile and DEM to surround Basin ID: 84598

The general dimensions of the lake within the basin that would be flooded is
V0 = 5 km x 8km x 0.25 km = 1km3 : this is a guestimate but would be the fixed value of water behind a dam/reservoir

Start do - while loop:

Reclassify (spatial analysis) 
4705 m: an arbitrary elevation threshold that we will base our iterations off 
Elevations above 4705 m not flooded (set value from 4705.0001 – 5692 = 1)
Elevations below are flooded (4646 – 4705 = 0)

Set Null (spatial analysis) – remove pixels with an elevation above threshold value of 4705 
  First input: reclassify dem
  Second input : original dem
  Condition: value = 1

Get statistic for the mean elevation of the newly created raster of elevations below 4705 

Threshold value 4705
A1 = number of pixels that equal 0 * cell size = 8708*0.1km*0.1km= 87.08 km2
Mean elevation of basin after you’ve set null = 4676.39 m
∆H1 ¬= 4705 m –  4676.39 m = 28.61 m = .0286 km 
V1 = 0.0286 km * 87.08 km = 2.4904 km2
Y1 = V0  - V1  = 1 – 2.4904 = -1.49 km2

We want Y as close as possible to zero but cannot change V0
  If Y negative: decrease H: set lower threshold value
  If Y positive: increase H: set higher threshold value

WRONG direction
threshold value 4706.39
∆H2 = 4706.39 (arbitrarily set to check logic) – 4676.89(mean elevation of null) = 29.5
A2 = 8881 * 0.1 * 0.1 = 88.81 km2
V2 = 88.81 * 0.0295 = 2.6198 km3

RIGHT direction
Threshold value 4703.39
∆H2 = 4703.39 – 4675.39 = 28
A2 = 8359 * 0.1*0.1 = 83.59 km2
V2 = 83.59*0.28 = 2.3405
Y2 = 1-2.3405 = -1.34


End while loop

Do raster to polygon conversion using accurate reclassified DEM
  Select by attribute
  Grid code = 0 (means flooded elevations)
  Export as a shapefile

This is the shapefile for the flood extent: 
  Append water volume by polygon part to the shapefile
=======
We are essentially taking the volume of water in a lake and pouring it in to a basin and seeing where it goes. 

The inputs are the water volume, the DEM of the region of interest, and an estimated flood area.
The output is a flood extent shapefile for our region of interest

There are 4 main variables that we will be using 
               V = volume of water
               H = change in the height of the water in the basin
               A = the area or flood extent (this is different(smaller) than the region of interest)
               L = the water level (this is also the threshold value for classifying the DEM)
               E = mean elevation of the within A

From V and our initial A we can calculate H using this equation
                H = V/A

We then need to find L using this equation
               L = H + E
This says that the water level is the mean elevation plus height of the water. This will then be used as a threshold value to classify the DEM 

We classify the DEM so everything less the L is flooded area and everything greater then L is above the flood line. 

We then take the area of flooded area (everything less the L). This should produce a new A value (A_new).

We calculate the mean elevation of A_new (E_new).

We then calculate a new H value (H_new) with is equation
               H_new = L - E_new

From A_new and H_new we can get a new volume of water (V_new)
               V_new = H_new * A_new

We then compare the original volume and the the new volume
              Y = V - V_new
we want Y to be 0 because that means the volume of water leaving the lake and entering the basin are the same. If Y is not zero we run it again using our new H value until we get close to zero.



