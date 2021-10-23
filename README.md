# parser-moemisto
It is parser for moemisto.ua site.

It takes data from the site and put them to posgreSQL DB.

- **parser-request.py** is main module
- **helper.py** procedures for work with database
- **config.py**  reads database.ini file and returns the connection parameters.
- **w2gDB.ini** contains database conection paramenters
- **clear.sql** is SQL query which used by helper.py for clearing database
