# -*-coding:utf-8-*-

import pyodbc
import settings


class EnvTest(object):
    def __init__(self, db, usr):
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + settings.SERVER + ';DATABASE=' + settings.DATABASE + ';UID=' + settings.UID + ';PWD=' + settings.PWD)
        self.cursor = self.conn.cursor()
        self.db = db
        self.usr = usr

    def __del__(self):
        self.conn.close()

    def insert_data(self, table, source_type, source):
        """
        write file data to db
        :param source_type: file or list
        :param source:
        :param table: table to insert into
        """
        sql_insert = "insert into %s (Name, Phone, Mobile, Org, Office, EncryptID) VALUES (?, ?, ?, ?, ?, ?)" % table
        param = []

        if source_type == 'file':
            print "Inserting from file into %s ..." % table
            source_file = source
            with open(source_file, 'r') as f:
                for line in f.readlines():
                    line = line.replace('\n', '')
                    # print line.split('##')
                    param.append(line.split('##'))
        elif source_type == 'list':
            print 'Inserting from list into %s ...' % table
            param = source

        else:
            print 'func [insert_data] Wrong parameters.'
            return
        try:
            self.cursor.executemany(sql_insert, param)
            print "%s lines inserted." % len(param)
            self.conn.commit()

        except Exception, e:
            print e

    def del_data(self, table, source_type, source):
        # sql_del = "delete from %s where Name = ? and Phone = ? and Mobile = ? and Org = ? and Office = ? and EncryptID = ?" % table
        sql_del = "delete from %s where EncryptID = ?" % table
        param = []
        for i in source:
            param.append(tuple(i[5]))
        try:
            self.cursor.executemany(sql_del, param)
            print "Source: %s " % source
            # ret = self.cursor.fetchall()
            # print 'RET: %s' % ret
            self.conn.commit()
            print "%s lines deleted from table %s." % (self.cursor.rowcount, table)
        except Exception, e:
            print e

    def clean_table(self, table):
        """
        delete all data in the table
        """
        sql_del = "delete from %s" % table
        try:
            self.cursor.execute(sql_del)
            print "Cleared. %s rows deleted from table %s" % (self.cursor.rowcount, table)
            self.conn.commit()

        except Exception as e:
            print e


def check_change_type(change_type):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + settings.SERVER + ';DATABASE=' + settings.DATABASE + ';UID=' + settings.UID + ';PWD=' + settings.PWD)
    cursor = conn.cursor()
    sql_statement = ""
    if change_type == 1:
        # 原表中有而新获取的数据中没有（信息修改和新人加入）
        sql_statement = "select Name, Phone, Mobile, Org, Office, EncryptID from Employees except select Name, Phone, Mobile, Org, Office, EncryptID from TmpEmployees"
    elif change_type == 2:
        # 原表中没有，新获取的数据中有的（离职和信息修改）
        sql_statement = "select Name, Phone, Mobile, Org, Office, EncryptID from TmpEmployees except select Name, Phone, Mobile, Org, Office, EncryptID from Employees"
    elif change_type == 3:
        # 原表中没有的EncryptID，新表中有，表示新加入
        sql_statement = "select Name, Phone, Mobile, Org, Office, EncryptID from TmpEmployees where EncryptID in ( select EncryptID from TmpEmployees except select EncryptID from Employees)"
    elif change_type == 4:
        # 原表中有的EncryptID，新表中没有，表示离职
        sql_statement = "select Name, Phone, Mobile, Org, Office, EncryptID from Employees where EncryptID in ( select EncryptID from Employees except select EncryptID from TmpEmployees)"

    try:
        cursor.execute(sql_statement)
        data = cursor.fetchall()
        return data

    except Exception, e:
        print e

    finally:
        conn.close()




# print leave_list
# print new_list
# print change_list
#
# print '-------------'
#
# print check_change_type(1)
# print check_change_type(2)
# print check_change_type(3)
# print check_change_type(4)


et = EnvTest('HakuTest', 'dbo')

et.insert_data('Employees', 'file', 'test_data.txt')
et.insert_data('TmpEmployees', 'file', 'test_data2.txt')

leave_list = check_change_type(4)
new_list = check_change_type(3)
change_list = [item for item in check_change_type(1) if item not in leave_list]

print new_list
print leave_list

et.insert_data("Employees", 'list', new_list)
et.del_data("Employees", 'asdf', leave_list)




# et.clean_table('Employees')
# et.clean_table('TmpEmployees')
