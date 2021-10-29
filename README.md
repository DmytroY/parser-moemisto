# parser-moemisto
It is parser for moemisto.ua site.

It takes data from the site and put them to posgreSQL DB.
2 improvements used for speedup process:
1) Eevery INSERT to PostgreSQL takes about 0.5sec. To avoid such time lose I put all data to temporary files first, then COPY data from file to the PostgreSQL tables.
2) The site responds in 0.5 ~ 1.2 sec. So I use threading for wait and prosess site responce in paralel way.
Processing time before those modification was 1h, after is 70 sec.

- **parser-file.py** is main module
- **helper.py** procedures for work with database
- **config.py**  reads database.ini file and returns the connection parameters.
- **w2gDB.ini** contains database conection paramenters
- **clear.sql** is SQL query which used by helper.py for clearing database
- **w2g_backup 29-10-2021** database backup with parsed results made with pgAdmin in custom format
