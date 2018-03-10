from django.shortcuts import render
from UnmannedStore import models

# Create your views here.
def Purchase(request):   

    # 資料庫function: 擷取產品名稱/價格
    product = models.Products()
    catagories = product.SelectProducts()
    # 資料庫function: 查詢帳戶名稱/姓名/餘額。登入功能尚未完成，所以ID先暫隨便select一筆
    member = models.Member()
    # 結帳前餘額
    balance = member.SelectBalance()
    # 結帳扣款，假設消費後餘額剩5000，update進資料庫
    member.UpdateBalance(5000)

    return render(request,'UnmannedStore/BOT.html',locals())

