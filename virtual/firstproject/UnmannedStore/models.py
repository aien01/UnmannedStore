from django.db import models
from django.db import connection

class Products():
    def SelectProducts(self):
        with connection.cursor() as cursor:
            cursor.execute("select ProductName, price from products")
            datas = cursor.fetchall()
        return datas  
class Member():
    def SelectBalance(self):
        with connection.cursor() as cursor:
            cursor.execute("select account, username, balance from member where id = 1")
            datas = cursor.fetchall()
        return datas
    def UpdateBalance(self,balance):
        with connection.cursor() as cursor:
            sql = "update member set balance=%s where id = 1"
            cursor.execute(sql,(balance,))
            datas = cursor.fetchall()
