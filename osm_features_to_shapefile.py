#-------------------------------------------------------------------------------
# Name:        Penn State Geog 485 Project 3: Extracting amenities from OpenStreetMap data
# Purpose:     Creates seperate shapefiles of selected features(Schools, Hospitals, Places of Worship) in El Salvador from Open Street Map data
#              Example Data can be found at:
#              https://www.e-education.psu.edu/geog485/node/145
#
# Author:      Jacob Potterf
#-------------------------------------------------------------------------------



import arcpy
from arcpy.da import UpdateCursor

# Setting the workspace
env.workspace = "C:\\pennState485\\data\\project3" #change the directory to where your data resides

# Input the names of geographic data
centralAmericaBoundaries = "CentralAmerica.shp"
osmPoints = "OSMpoints.shp"

# The name field of geographic data of points by Open Street Map
nameFieldAmenity = "Amenity"
nameFieldCountry = "NAME"

# Input the names of amenities and the name of country
amenities = ["school","hospital","place_of_worship"]
country = "El Salvador"

try:
    # Select only the country in Central America Boundaries
    nameCountryLayer = country + "lyr"
    queryStringCountry = '"' + nameFieldCountry + '" = ' + "'"  + country + "'"
    MakeFeatureLayer_management(centralAmericaBoundaries, nameCountryLayer, queryStringCountry)

    for typeAmenities in amenities:
        # SQL pick up the type amenities
        queryStringAmenities = '"' + nameFieldAmenity + '" = ' + "'"  + typeAmenities + "'"
        # The name of new feature layer
        nameAmenitiesLayer = typeAmenities + "lyr"
        # Mame a feature layer of type amenities
        MakeFeatureLayer_management(osmPoints, nameAmenitiesLayer, queryStringAmenities)
        # Select only amanities into the country El Salvador
        SelectLayerByLocation_management(nameAmenitiesLayer, "CONTAINED_BY", nameCountryLayer)
        # Makes a separate shapefile for each types of amenities
        CopyFeatures_management(nameAmenitiesLayer, typeAmenities)
        # Get the new separete shapefile
        amenitiesTable = typeAmenities + '.dbf'
        # Name of new field for amenities
        newField = "source"
        # Add new field called 'source'
        AddField_management(amenitiesTable, newField, "TEXT", 100)
        with UpdateCursor(typeAmenities + ".shp", newField) as amenitiesRows:
            for row in amenitiesRows:
                # Update the value for each row in typeAmenities
                row[0] = "OpenStreetMap"
                amenitiesRows.updateRow(row)
except:
print ' An error occured and it was not possible makes a separete shapefile for each feature'