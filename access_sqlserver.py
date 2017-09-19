# -*-coding:utf-8-*-

import pyodbc
import settings


class AAA(object):
    def __init__(self, db, usr, table):
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + settings.SERVER + ';DATABASE=' + settings.DATABASE + ';UID=' + settings.UID + ';PWD=' + settings.PWD)
        self.cursor = self.conn.cursor()
        self.db = db
        self.usr = usr
        self.table = table

    def __del__(self):
        self.conn.close()

    def create_table(self):
        """
        check if table exists, create table if not.
        :param db: database that table belongs to
        :param usr: user that create the table
        :param table: table to be created
        """
        target_table = "%s.%s.%s" % (self.db, self.usr, self.table)
        sql_check_exist = "select object_id('%s')" % target_table

        try:
            self.cursor.execute(sql_check_exist)
            data = self.cursor.fetchone()[0]
            if not data:
                print "Creating table..."
                sql_create = "create table %s (ID int IDENTITY PRIMARY KEY, Name nvarchar(max), Phone nvarchar(max), Mobile nvarchar(max), Org nvarchar(max), EncryptID nvarchar(max))" % self.table
                self.cursor.execute(sql_create)
                self.conn.commit()
                print "Table %s created." % target_table
            else:
                print "Table %s already exists" % target_table
        except Exception as e:
            print e

    def insert_data(self, source_file):
        """
        write file data to db
        :param source_file:
        """
        sql_insert = "insert into %s VALUES (?, ?, ?, ?, ?)" % self.table
        param = []
        with open(source_file, 'r') as f:
            for line in f.readlines():
                line = line.replace('\n', '')
                # print line.split('##')
                param.append(tuple(line.split('##')))

        try:
            self.cursor.executemany(sql_insert, param)
            self.conn.commit()
        except Exception, e:
            print str(e).decode('GB2312')

    def clean_table(self):
        """
        delete all data in the table
        """
        sql_del = "delete from %s" % self.table
        try:
            self.cursor.execute(sql_del)
            self.conn.commit()
        except Exception as e:
            print e


inst = AAA('HakuTest', 'dbo', 'EmployeeUpToDate')
inst.create_table()
inst.insert_data('test_data.txt')
# inst.clean_table()
