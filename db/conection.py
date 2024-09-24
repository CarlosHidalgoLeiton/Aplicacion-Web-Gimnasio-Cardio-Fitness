import pymysql

connection = pymysql.connect(host='localhost', user='root', passwd='', db='gimnasio')

cur = connection.cursor()
