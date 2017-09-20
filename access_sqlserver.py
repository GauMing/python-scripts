# -*-coding:utf-8-*-

import pyodbc
import settings


class AAA(object):
    def __init__(self, db, usr, table):
        """

        :param db: database that table belongs to
        :param usr: user that create the table
        :param table: table to be created
        """
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

        """
        target_table = "%s.%s.%s" % (self.db, self.usr, self.table)
        sql_check_exist = "select object_id('%s')" % target_table

        try:
            self.cursor.execute(sql_check_exist)
            data = self.cursor.fetchone()[0]
            if not data:
                print "Creating table [%s]..." % target_table
                sql_create = "create table %s (ID int IDENTITY PRIMARY KEY, Name nvarchar(max), Phone nvarchar(max), Mobile nvarchar(max), Org nvarchar(max), EncryptID nvarchar(max))" % self.table
                self.cursor.execute(sql_create)
                self.conn.commit()
                print "Table [ %s ] created." % target_table
            else:
                print "Table [ %s ] already exists" % target_table
        except Exception as e:
            print e

    def insert_data(self, source_file, table=None):
        """
        write file data to db
        :param table:
        :param source_file:
        """
        table = self.table if not table else table
        sql_insert = "insert into %s (Name, Phone, Mobile, Org, EncryptID) VALUES (?, ?, ?, ?, ?)" % table
        param = []
        with open(source_file, 'r') as f:
            for line in f.readlines():
                line = line.replace('\n', '')
                # print line.split('##')
                param.append(line.split('##'))
        try:
            self.cursor.executemany(sql_insert, param)
            self.conn.commit()
            print "%s lines inserted." % len(param)
        except Exception, e:
            # 中文系统的编码问题
            print str(e).encode('utf-8').decode('GB2312')

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


# inst = AAA('HakuTest', 'dbo', 'EmployeeInit')
# inst.create_table()
# inst.insert_data('test_data.txt')
# # inst.clean_table()
#
# inst2 = AAA('HakuTest', 'dbo', 'EmployeeUpToDate')
# inst2.create_table()
# inst2.insert_data('test_data2.txt')

def check_change():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + settings.SERVER + ';DATABASE=' + settings.DATABASE + ';UID=' + settings.UID + ';PWD=' + settings.PWD)
    cursor = conn.cursor()

    # 原表中有而新获取的数据中没有（信息修改和新人加入）
    sql_modify_add = 'select * from EmployeeInit except select * from EmployeeUpToDate'
    cursor.execute(sql_modify_add)
    print cursor.fetchall()

    # 原表中没有，新获取的数据中有的（离职和信息修改）
    sql_modify_lose = "select * from EmployeeUpToDate except select * from EmployeeInit"
    cursor.execute(sql_modify_lose)
    print cursor.fetchall()

    # 原表中没有的EncryptID，新表中有，表示新加入
    sql_new = "select Name from EmployeeUpToDate except select Name from EmployeeInit"
    cursor.execute(sql_new)
    print cursor.fetchall()

    # 原表中有的EncryptID，新表中没有，表示离职
    sql_leave = "select Name from EmployeeInit except select Name from EmployeeUpToDate"
    cursor.execute(sql_leave)
    print cursor.fetchall()


check_change()
