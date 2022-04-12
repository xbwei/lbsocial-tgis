# A GIS representation framework for location‐based social media activities

To cite the paper:
> Wei, X., & Yao,X.(2022). A GIS representation framework for location‐based social media activities. Transactions in GIS, 00, 1-22.https://doi.org/10.1111/tgis.12929


A [demo video](https://youtu.be/TSARYxwWcCE) is provided illustrating how to load the data and run the tool in ArcGIS.

The SQL codes to create the demo data tables is in the [demo_data_sql](https://github.com/xbwei/lbsocial-tgis/tree/main/demo_data_sql) folder. The demo data is in the [demo_data](https://github.com/xbwei/lbsocial-tgis/tree/main/demo_data) folder. The demo output is in the [demo_output](https://github.com/xbwei/lbsocial-tgis/tree/main/demo_output) folder. 

To load the data into Postgresql, install the [Postgresql](https://www.postgresql.org/) with the [GIS plugin](https://postgis.net/), and create the following tables. Those tables should have the same columns as in the [demo_data](https://github.com/xbwei/lbsocial-tgis/tree/main/demo_data) CSV files.
- activity_demo,
- people_demo,
- peoplesocial_demo,
- place_demo,
- placesocial_demo.

Load the demo data to the database:

`COPY demo_data`

`FROM 'C:\demo_data.csv' DELIMITER ',' CSV HEADER;`

Connect Postgresql to ArcGIS:
- Add a database connection to Postgresql in ArcGIS. A video tutorial is avaiable [here](https://youtu.be/wZj9f8eh8Xw).

Please install the required python packages before running the tool:
- pysal
- psycopg2
- networkx
- numpy
- pyproj
- matplotlib
- arcpy

