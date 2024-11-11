# sqlalchemy-challenge

With an upcoming long holiday vacation in Honolulu, Hawaii, our assignment was to do a climate analysis about the area. The dataset, stored in an SQLite database, contains precipitation and temperature data across various weather stations. The goal was to retrieve meaningful insights about weather patterns in Hawaii and to build an API for easy data access.
The initial data exploration involved connecting to the database and using SQLAlchemy to reflect the tables into ORM classes. Two tables were identified: measurement (containing temperature and precipitation data) and station (containing weather station information). A query was designed to retrieve the last 12 months of precipitation data, showing seasonal precipitation patterns as shown below.

![precipitation.png](https://github.com/otybaasandorj/sqlalchemy-challenge/blob/main/SurfsUp/images/precipitation.png)

Using a query to count observations per station, the station USC00519281 was identified as the most active station, with the highest number of observations. For USC00519281, the most active station, a histogram of temperature observations over the last 12 months revealed that most temperatures fell between 70°F and 80°F as shown below. 

![histogram.png](https://github.com/otybaasandorj/sqlalchemy-challenge/blob/main/SurfsUp/images/histogram.png)

The analysis highlighted Hawaii's generally moderate temperatures, with noticeable precipitation patterns that may be tied to seasonal changes. The API provides a useful tool for retrieving climate data by date and station, potentially aiding researchers, tourists, or residents in understanding weather trends.
