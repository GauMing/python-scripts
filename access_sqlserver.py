#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyodbc
import settings

'''
Employees表，正在使用的对外提供查询的表
TmpEmployees表，定期获取的最新数据，用完即删
HistoryRecords表，存放所有历史数据的表，包括最新的数据；
    ModifyDate：修改日期，默认为当前时间；
    ModifyType：修改类型：Initial, Leave, New, Modify
'''


class EnvPreparation(object):
    def __init__(self, db, usr):
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + settings.SERVER + ';DATABASE=' + settings.DATABASE + ';UID=' + settings.UID + ';PWD=' + settings.PWD)
        self.cursor = self.conn.cursor()
        self.db = db
        self.usr = usr

    def __del__(self):
        self.conn.close()

    def create_history_table(self):
        """
        check if HistoryRecords table exists, create if not.

        """
        target_table = "HistoryRecords"
        sql_check_exist = "select object_id('%s')" % target_table

        try:
            self.cursor.execute(sql_check_exist)
            data = self.cursor.fetchone()[0]
            if not data:
                print "Creating table [%s]..." % target_table
                sql_create = "create table %s (ID int IDENTITY PRIMARY KEY, Name nvarchar(max), Phone nvarchar(max), Mobile nvarchar(max), Org nvarchar(max), Office nvarchar(max), EncryptID nvarchar(max), ModifyDate datetime NOT NULL DEFAULT getdate(), ModifyType nvarchar(max))" % target_table
                self.cursor.execute(sql_create)
                self.conn.commit()
                print "Table [ %s ] created." % target_table
            else:
                print "Table [ %s ] already exists" % target_table
        except Exception as e:
            print e

    def update_history(self, modify_type, source, init=None):
        """

        :param modify_type:
        :param source:
        :param init:
        """
        sql_update = "update HistoryRecords set ModifyType = '%s' where Name = ? and Phone = ? and Mobile = ? and Org = ? and Office = ? and EncryptID = ? and ModifyType is null" % modify_type
        if init == 'INIT':
            sql_update = "update HistoryRecords set ModifyType = 'Initial'"
        try:
            if not init:
                self.cursor.executemany(sql_update, source)
            else:
                self.cursor.execute(sql_update)
            self.conn.commit()

        except Exception, e:
            print e

    def insert_employee(self, table, source_type, source):
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
        sql_del = "delete from %s where Name = ? and Phone = ? and Mobile = ? and Org = ? and Office = ? and EncryptID = ?" % table
        # sql_del = "delete from %s where EncryptID = ?" % table
        param = []
        for i in source:
            # param.append(tuple(i[5]))
            param.append(tuple(i))
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
        :param table:
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


ep = EnvPreparation('HakuTest', 'dbo')

ep.create_history_table()

# 准备测试环境，先清空数据表
ep.clean_table('Employees')
ep.clean_table('TmpEmployees')
ep.clean_table('HistoryRecords')

# 初次操作向Employees 和HistoryRecords 插入数据，之后只向TmpEmployees 插入数据，以作差异比较
ep.insert_employee('Employees', 'file', 'test_data.txt')
ep.insert_employee('HistoryRecords', 'file', 'test_data.txt')
ep.insert_employee('TmpEmployees', 'file', 'test_data2.txt')

ep.update_history(None, None, 'INIT')

# print check_change_type(1)
# print check_change_type(2)
# print check_change_type(3)
# print check_change_type(4)

leave_list = check_change_type(4)
new_list = check_change_type(3)
# 修改前的数据，存在于Employees中，待删除
change_list_old = [item for item in check_change_type(1) if item not in leave_list]
# 修改后的数据，待插入Employees 和History Records中
change_list_new = [item for item in check_change_type(2) if item not in new_list]

print new_list
print leave_list
print change_list_old
print change_list_new

ep.insert_employee("Employees", 'list', new_list)
ep.del_data("Employees", 'list', change_list_old)
ep.insert_employee("Employees", 'list', change_list_new)
ep.del_data("Employees", 'list', leave_list)


ep.insert_employee('HistoryRecords', 'list', change_list_new)
ep.insert_employee('HistoryRecords', 'list', new_list)
ep.insert_employee('HistoryRecords', 'list', leave_list)


ep.update_history('New', new_list)
ep.update_history('Leave', leave_list)
ep.update_history('Modify', change_list_new)

ep.clean_table('TmpEmployees')
