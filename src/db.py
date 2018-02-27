import pymysql, time, logging, json

from aconfig import config

'''
Gets all tables from source with the data and copies everything to destination after clearing it

1. Get all tables from source
2. Get all data for each table
3. Clear destination
4. Create tables and insert data
'''

logger = logging.getLogger('DevDB.db.connect')

def connect(database):
    logger.debug('Connecting to {}'.format(config('databases.' + database + '.name')))
    connection = pymysql.connect(host=config('databases.' + database + '.host'),
                             user=config('databases.' + database + '.username'),
                             password=config('databases.' + database + '.password'),
                             db=config('databases.' + database + '.name'),
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

def getTables(connection):
    logger.debug('Getting tables')
    query = "SHOW TABLES"
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            yield row

def getCreation(connection, table):
    logger.debug('Getting creation of {}'.format(table))
    query = "SHOW CREATE TABLE " + table
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()
    
def getData(connection, table):
    logger.debug('Getting data from {}'.format(table))
    query = "SELECT * FROM " + table
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            yield row
    
def emptyDatabase(connection, database):
    logger.debug('Emptying database {}'.format(config('databases.' + database + '.name')))
    for table in getTables(connection):
        query = "DROP TABLE " + table['Tables_in_' + config('databases.' + database + '.name')]
    
        cursor = connection.cursor()
        cursor.execute(query)
    
def createTable(connection, table, creation):
    logger.debug('Creating table {}'.format(table))
    query = creation.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
    
    cursor = connection.cursor()
    cursor.execute(creation)
        
def insertData(connection, table, data):
    logger.debug('Inserting data into {}'.format(table))
    query = "INSERT INTO " + table + " VALUES ("
    for item, value in data.items():
        query += '%(' + item + ')s, '
        logger.debug('({}: {})'.format(item, value))
    query = query[:-2]
    query += ')'
    
    cursor = connection.cursor()
    cursor.execute(query, data)
    
def db():
    start = time.time()
    in_database = 'source'
    out_database = 'destination'
    in_connection = connect(in_database)
    out_connection = connect(out_database)
        
    try:
        query = "SET FOREIGN_KEY_CHECKS=0"
        with out_connection.cursor() as cursor:
            cursor.execute(query)
        
        emptyDatabase(out_connection, out_database)
        
        for table in getTables(in_connection):
            table = table['Tables_in_' + config('databases.' + in_database + '.name')]
            creation = getCreation(in_connection, table)['Create Table']
            createTable(out_connection, table, creation)
            for data in getData(in_connection, table):
                insertData(out_connection, table, data)
        
        out_connection.commit()
        
        query = "SET FOREIGN_KEY_CHECKS=1"
        with out_connection.cursor() as cursor:
            cursor.execute(query)
    finally:
        in_connection.close()
        out_connection.close()

    end = time.time()
    return end - start