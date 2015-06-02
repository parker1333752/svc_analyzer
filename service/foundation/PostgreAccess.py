import psycopg2
from psycopg2 import extras
from datetime import datetime

class TxPostgreAccess(object):
    '''
    code examples:
        # pac is a instance of TxPostgreAccess.

        code example: (count)
            a = pac.count('vehicle')

        code example: (select)
            a = pac.select('vehicle',columns=['code','id'])
            # or get all columns default : a = pac.select('vehicle')

            # print all data to console
            for i in a:
                s = []
                for j in i.iteritems():
                    s.append('%s=%r'%j)
                s = ','.join(s)
                print s

        code example: (insert)
            a = pac.insert('vehicle',{'code':'1314','note':'python'})

        code example: (update)
            a = pac.update('vehicle',{'code':131},'where id=16')

        code example: (delete)
            a = pac.delete('vehicle','where id = 11')
    '''
    default_user = 1314

    def __init__(self, config):
        self.conn = psycopg2.connect(database=config['database'],user=config['user'],
                password=config['password'],host=config['host'],port=config['port']
                ,cursor_factory=extras.DictCursor)

    def count(self, table, query=''):
        '''get count of records (rows) of one table
        - table: table name (string)
        - query: a query string to indicate which rows of data to update, like 'where id = 1'
        ->return_value: a long type date indicate count of row in this table
        '''
        if not table:
            raise AssertionError, 'table can\'t be None'

        sql = 'select count(*) from ' + table + ' ' + query

        # with statement: if no exception, transaction is committed.
        # In case of exception the transaction is rolled back.
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                data = cur.fetchone()
                if data:
                    return data['count']

    def select(self, table, columns = [], query = ''):
        '''select a list of data match the query condition
        - table: table name (string)
        - columns: a list of column's names, indicate return data's content.
            columns=[] means return all columns data.
        - query: a query string to indicate which rows of data to update, like 'where id = 1'
        ->return_value: list of RowMap.
            RowMap is a dict-like object, use rowMap.iteritems()
        '''
        if not table:
            raise AssertionError, 'table can\'t be None'

        column_string = ','.join(columns)
        if not column_string:
            column_string = '*'
        sql = 'select ' + column_string + ' from ' + table + ' ' + query

        with self.conn:
            with self.conn.cursor() as cur:
                cur = self.conn.cursor()
                cur.execute(sql)
                return cur.fetchall()

    def insert(self, table, data):
        '''insert a record (one row) into database.
        - table: table name (string)
        - data: a python-dict has structure of {'column1':value}, represent a row data in database
        ->return_value: return True if update success, else return None
        notice that: 
            If crtdate and upddate is not given, curren datetime will be used.
            If crtuser and upduser is not given, default user code will be used. (check default_user_code by 'print TxPostgreAccess.default_user')
        '''
        if not table:
            raise AssertionError, 'table can\'t be None'

        columnNames = self.getColumns(table)
        if 'crtuser' in columnNames and data.get('crtuser') == None:
            data['crtuser'] = self.__class__.default_user
            if 'upduser' in columnNames and data.get('upduser') == None:
                data['upduser'] = self.__class__.default_user

        if 'crtdate' in columnNames and data.get('crtdate') == None:
            data['crtdate'] = datetime.now()
            if 'upddate' in columnNames and data.get('upddate') == None:
                data['upddate'] = data['crtdate']

        columns = '(' + ','.join(data.iterkeys()) + ')'
        values = '(' + ','.join(len(data)*['%s']) + ')'
        sql = 'insert into ' + table + ' ' + columns + ' values ' + values

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql, tuple(data.itervalues()))
                return True

    def update(self, table, data = {}, query = ''):
        '''update a record (one row) in database.
        - table: table name (string)
        - data: a python-dict has structure of {'column1':value}, represent a row data in database
        - query: a query string to indicate which rows of data to update, like 'where id = 1'
        ->return_value: return True if update success, else return None
        notice that: 
            If upddate is not given, curren datetime will be used.
            If upduser is not given, default user code will be used. (check default_user_code by 'print TxPostgreAccess.default_user')
            Query can't be null for prevent mass change.
        '''
        if not table:
            raise AssertionError, 'table can\'t be None'

        if not query:
            raise AssertionError, '\n\tUpdate all data is forbiden, set query condition first.'

        columnNames = self.getColumns(table)
        if 'upduser' in columnNames and data.get('upduser') == None:
            data['upduser'] = self.__class__.default_user

        if 'upddate' in columnNames and data.get('upddate') == None:
            data['upddate'] = datetime.now()

        with self.conn:
            with self.conn.cursor() as cur:
                lst_data = []
                for i in data.iterkeys():
                    s = i + '=%s'
                    lst_data.append(s)

                sql = 'update ' + table + ' set ' + ','.join(lst_data) + ' ' + query
                cur.execute(sql,tuple(data.itervalues()))
                return True

    def delete(self, table, query):
        '''delete records (rows) which match query condition.
        - table: table name (string)
        - query: a query string to indicate which rows of data to update, like 'where id = 1'
        ->return_value: return True if update success, else return None
        notice that: 
            If upddate is not given, curren datetime will be used.
            If upduser is not given, default user code will be used. (check default_user_code by 'print TxPostgreAccess.default_user')
            Query can't be null for prevent mass change.
        '''
        if not query:
            raise AssertionError, '\n\tUpdate all data is forbiden, set query condition first.'

        sql = 'delete from ' + table + ' ' + query
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                return True

    def __del__(self):
        self.conn.close()

    def getColumns(self, table):
        '''-> return a list of column name
        '''
        rs = self.select('information_schema.columns',query='where table_schema=\'public\' and table_name=\'%s\''%(table,))
        return [ i['column_name'] for i in rs]

if __name__ == '__main__':
    config = {
        "database": "site",
        "user": "siteadmin",
        "password": "siteadmin",
        "host": "192.168.1.153",
        "port": "5432"
    }
    # pac is a instance of TxPostgreAccess.
    pac = TxPostgreAccess(config)

    del pac

