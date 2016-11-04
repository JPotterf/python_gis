#-------------------------------------------------------------------------------
# Name:        Penn State Geog 485: Park and Rides
# Purpose:     Determines which cities have at least two park and rides.
#              Then prints percentage of cities.
#              Source data availabe at:
#              https://www.e-education.psu.edu/geog485/node/59
# Author:      Jacob Potterf
#-------------------------------------------------------------------------------

import arcpy
arcpy.env.overwriteOutput = True

cityBoundaries = "C:\\pennstate485\\data\\lesson3\\practice_exercise_b\\Washington.gdb\\CityBoundaries" #set directory where your data is stored
parkAndRide = "C:\\pennstate485\\data\\lesson3\\practice_exercise_b\\Washington.gdb\\ParkAndRide"       #set directory where your data is stored
parkAndRideField = "Has_Two_Park_And_Rides"   # Name of column for storing the Park & Ride information
cityIDStringField = "CI_FIPS"                 # Name of column with city IDs
citiesWithTwoParkAndRides = 0                 # Used for counting cities with at least two P & R facilities
numCities = 0                                 # Used for counting cities in total

#feature layer of all the park and ride facilities
arcpy.MakeFeatureLayer_management(parkAndRide, "ParkAndRideLayer")

# update cursor loops through each city
with arcpy.da.UpdateCursor(cityBoundaries, (cityIDStringField, parkAndRideField)) as cityRows:
    for city in cityRows:
        # Create a query string for the current city
        cityIDString = city[0]
        queryString = '"' + cityIDStringField + '" = ' + "'" + cityIDString + "'"

        # Make a feature layer of just the current city polygon
        arcpy.MakeFeatureLayer_management(cityBoundaries, "CurrentCityLayer", queryString)

        try:
            # selecting only the park and rides in the current city
            arcpy.SelectLayerByLocation_management("ParkAndRideLayer", "CONTAINED_BY", "CurrentCityLayer")

            # Count the number of park and ride facilities selected
            selectedParkAndRideCount = arcpy.GetCount_management("ParkAndRideLayer")
            numSelectedParkAndRide = int(selectedParkAndRideCount.getOutput(0))

            # If more than two park and ride facilities found, update the row to TRUE
            if numSelectedParkAndRide >= 2:
                city[1] = "TRUE"

                # updateRow
                cityRows.updateRow(city)

                # increment P&R counter
                citiesWithTwoParkAndRides += 1

        finally:
            # Deletes current cities layer increments numCities
            arcpy.Delete_management("CurrentCityLayer")
            numCities +=1

# Clean up park and ride feature layer
arcpy.Delete_management("ParkAndRideLayer")

# Calculate and report the number of cities with two park and rides
if numCities != 0:
    percentCitiesWithParkAndRide = ((1.0 * citiesWithTwoParkAndRides) / numCities) * 100
else:
    print "Error with input dataset. No cities found."

print str(percentCitiesWithParkAndRide) + " percent of cities have two park and rides."