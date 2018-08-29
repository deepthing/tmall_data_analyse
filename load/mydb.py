import MySQLdb
import sys
sys.path.append("..")
sys.path.append("../..")
import tmall_data_analyse.settings as settings



def exec_sql(sqlstr):
    db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                            user=settings.DATABASES.get(
                                'default').get('USER'),
                            passwd=settings.DATABASES.get(
                                'default').get('PASSWORD'),
                            db=settings.DATABASES.get('default').get('NAME'),
                            charset="utf8",
                            local_infile=1)
    data = db.cursor(MySQLdb.cursors.DictCursor)
    data.execute(sqlstr)

    db.commit()
    data.close()
    db.close()

def exec_sql_list(sqlstrlist):
    db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                            user=settings.DATABASES.get(
                                'default').get('USER'),
                            passwd=settings.DATABASES.get(
                                'default').get('PASSWORD'),
                            db=settings.DATABASES.get('default').get('NAME'),
                            charset="utf8",
                            local_infile=1)
    data = db.cursor(MySQLdb.cursors.DictCursor)
    for sqlstr in sqlstrlist:
        data.execute(sqlstr)

    db.commit()
    data.close()
    db.close()

def exec_sql_select(sqlstr):
    db = MySQLdb.connect(host=settings.DATABASES.get('default').get('HOST'),
                            user=settings.DATABASES.get(
                                'default').get('USER'),
                            passwd=settings.DATABASES.get(
                                'default').get('PASSWORD'),
                            db=settings.DATABASES.get('default').get('NAME'),
                            charset="utf8",
                            local_infile=1)
    data = db.cursor(MySQLdb.cursors.DictCursor)
    data.execute(sqlstr)
    res = data.fetchall()
    db.commit()
    data.close()
    db.close()
    return res
