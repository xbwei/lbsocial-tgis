# A GIS representation framework for location‐based social media activities

To cite the paper:
> 

A demo video is provided illustrating how to load the data and run the tool in ArcGIS.

The SQL codes to create the demo data tables is in the demo_data_sql folder. The demo data is in the demo_data folder. The demo output is in the demo_output folder. 

To load the data into Postgresql, install the Postgresql with GIS plugin, and create the following tables. Those tables should have the same columns as in the demo_data CSV files.
- activity_demo,
- people_demo,
- peoplesocial_demo,
- place_demo,
- placesocial_demo.

Load the demo data to the database:

`COPY demo_data`
`FROM 'C:\demo_data.csv' DELIMITER ',' CSV HEADER;`

Connect Postgresql to ArcGIS:
Add a database connection to Postgresql in ArcGIS

Please install the required python packages before run the tool:
- pysal
- psycopg2
- networkx
- numpy
- pyproj
- matplotlib
- arcpy

