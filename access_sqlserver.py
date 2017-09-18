# -*-coding:utf-8-*-

import pyodbc
import settings

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + settings.SERVER + ';DATABASE=' + settings.DATABASE + ';UID=' + settings.UID + ';PWD=' + settings.PWD)
cursor = conn.cursor()


def create_table(db, usr, table):
    """
    check if table exists, create table if not.
    :param db: database that table belongs to
    :param usr: user that create the table
    :param table: table to be created
    """
    target_table = "%s.%s.%s" % (db, usr, table)
    sql_check_exist = "select object_id('%s')" % target_table

    try:
        cursor.execute(sql_check_exist)
        data = cursor.fetchone()[0]
        if not data:
            print "Creating table..."
            sql_create = "create table %s (ID int IDENTITY PRIMARY KEY, Name nvarchar)" % table
            cursor.execute(sql_create)
            conn.commit()
            print "Table %s created." % target_table
        else:
            print "Table %s already exists" % target_table
    except Exception as e:
        print e
    finally:
        conn.close()


create_table('HakuTest', 'dbo', 'people22')
