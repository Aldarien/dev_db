import pymysql

class DB:
    host=''
    username=''
    password=''
    name=''
    connection=None
    
    def __init__(self, host='', username='', password='', name=''):
        self.host = host
        self.username = username
        self.password = password
        self.name = name
    def connect(self):
        self.connection = pymysql.connect(host=self.host, user=self.username, password=self.password, db=self.name, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    
    def tables(self):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                sql = "SHOW TABLES"
                cursor.execute(sql)
                results = cursor.fetchall()
                for r in results:
                    for k, t in r.items():
                        yield t
        except Exception as e:
            print(e)
        finally:
            try:
                self.connection.close()
            except:
                ''
    
    def schema(self, table):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                sql = "DESCRIBE " + table
                cursor.execute(sql)
                results = cursor.fetchall()
                for r in results:
                    yield r
        except Exception as e:
            print(e)
        finally:
            try:
                self.connection.close()
            except:
                ''
                
    def hasTable(self, table):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                sql = "SHOW TABLES LIKE '" + table + "'"
                r = cursor.execute(sql)
                if r > 0:
                    return True
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            try:
                self.connection.close()
            except:
                ''
    
    def tableHasColumn(self, table, column):
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                sql = "SHOW COLUMNS FROM `" + table + "` LIKE %s"
                r = cursor.execute(sql, (column))
                if r > 0:
                    return True
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            try:
                self.connection.close()
            except:
                ''
                
    def createTable(self, table, source_gen):
        output = "CREATE TABLE " + table + '('
        for column in source_gen:
            output += column['Field'] + ' ' + column['Type']
            if column['Null'] == 'NO':
                output += ' NOT NULL'
            if column['Key'] == ''