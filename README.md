Geography 173 Final Project
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