# parser-moemisto
It is parser for moemisto.ua site.
It takes data from the site and put them to posgreSQL DB.
Contains files:
*** parser-request.py*** - main module
*** helper.py*** - procedures for work with database
*** config.py*** - reads database.ini file and returns the connection parameters.
*** database.ini*** - database conection paramenters
*** clear.sql*** - SQL query which used by helper.py for clearing database
