import sys
sys.path.append(r"D:\Python_Excercise\cx_ORCL\tutorials\python-cx_Oracle-main\samples\tutorial")
import cx_Oracle
import db_config

con = cx_Oracle.connect(db_config.user, db_config.pw, db_config.dsn)
print("Database version:", con.version)