from django.shortcuts import render,redirect
from UnmannedStore import models
from django.http import HttpResponse,JsonResponse
from chatterbot import ChatBot
from chatterbot.comparisons import levenshtein_distance
from chatterbot.comparisons import jaccard_similarity
from chatterbot.comparisons import sentiment_comparison
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import requests
import speech_recognition as sr 
import time
from gtts import gTTS
import os
import tempfile
from pygame import mixer
from playsound import playsound
from bs4 import BeautifulSoup
import webbrowser
import re
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
    
    RobotOutput = 'Hello'

    return render(request,'UnmannedStore/BOT.html',locals())

def BOT(request):
    You = request.GET['You']
    response = TextEnBot(You)
    print(response)
    Speech(response)

    return JsonResponse(response,safe=False)

def Checkout(request):
    product1 = int(request.GET['雪碧'])
    product2 = int(request.GET['茶裏王'])
    product3 = int(request.GET['衛生紙'])
    product4 = int(request.GET['刮鬍刀'])
    product5 = int(request.GET['阿Q桶麵'])
    product6 = int(request.GET['維力炸醬麵'])
    product7 = int(request.GET['可樂'])
    product8 = int(request.GET['伯朗咖啡'])
    product9 = int(request.GET['樂事原味洋芋片'])
    product10 = int(request.GET['義美泡芙'])
    # test = request.GET['test']
    # print(product1,product2,product10)
    # print(test)

    product = models.Products()
    catagories = product.SelectProducts()

    total_cost = product1*int(catagories[0][1]) + product2*int(catagories[1][1]) + product3*int(catagories[2][1]) + product4*int(catagories[3][1]) + product5*int(catagories[4][1]) + product6*int(catagories[5][1]) + product7*int(catagories[6][1]) + product8*int(catagories[7][1]) + product9*int(catagories[8][1]) + product10*int(catagories[9][1])

    print(catagories)


    member = models.Member()
    balance = member.SelectBalance()

    UpdateBalance = balance[0][2] - total_cost
    price = {'雪碧':int(catagories[0][1]),'茶裏王':int(catagories[1][1]),'衛生紙':int(catagories[2][1]),'刮鬍刀':int(catagories[3][1]),'阿Q桶麵':int(catagories[4][1]),'維力炸醬麵':int(catagories[5][1]),'可樂':int(catagories[6][1]),'伯朗咖啡':int(catagories[7][1]),'樂事原味洋芋片':int(catagories[8][1]),'義美泡芙':int(catagories[9][1])}
    
    print(price)

    localtime = time.asctime( time.localtime(time.time()) )
    receipt = {'name':balance[0][1],'total_cost':total_cost,'balance': UpdateBalance,'time':localtime,'price':price}
    print(receipt)
    Speech('Thank you for this purchase, hope you will be having a nice experience in Franklin Medium Store')
    
    return JsonResponse(receipt,safe=False)

def SpeechBot(request):
    # Speech('Good morning')
    # Speech('hello what can i do for you')
    request1 = Recognizer()
    output1 = EnBot(request1)
    if output1 == 'What can i do for you, sir?':
        Speech(output1)

        request2 = Recognizer()
        output2 = EnBot(request2)
        
        Speech(output2)
        if output2 == 'OK,Please wait a second':
            triger = 'CheckOut'
            return JsonResponse(triger,safe=False)
        if output2 == 'what keyword you would like to google':
            request3 = Recognizer()
            Speech('ok, you are being directed to google search as requested')
            google_search(request3)
            
        if output2 == 'what subject do you want to know':
            request3 = Recognizer()
            Speech('ok, here is the result you requested')
            data = wiki_key(request3)
            print(data)
            return JsonResponse(data,safe=False)
        if output2 == 'could you please provide the name of the video':
            request3 = Recognizer()
            output3 = EnBot(request3)
            Speech('Ok, here is the video you want')
            youtube_serach(request3)
        if output2 == 'Ok sir, here are some news for you':
            yahoo_news()
        if output2 == 'no problem sir, here is exchange rate for you':
  
            rate = exchange()
            data = {'triger':'exchange','data':rate}
            return JsonResponse(data,safe=False)
    else:
        pass


def Speech(text):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text= text, lang='en-us', slow=False)
        tts.save("{}.mp3".format(fp.name))
        # os.system("{}.mp3".format(fp.name))
        playsound("{}.mp3".format(fp.name))

def Recognizer():
    print('Please speak')
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        UserSpeech = r.recognize_google(audio)
        print(UserSpeech)
        return UserSpeech


def EnBot(input):
    bot = ChatBot('Norman', 
        logic_adapters=[    
       {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_random_response"
        },
        {
            "import_path": "chatterbot.logic.MathematicalEvaluation"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'Sorry sir, I do not understand what you mean'
        },
        ],
        preprocessors=[
                'chatterbot.preprocessors.clean_whitespace'
            ],
        input_adapter="chatterbot.input.VariableInputTypeAdapter",
        output_adapter="chatterbot.output.OutputAdapter",
        statement_comparison_function=levenshtein_distance)

    # bot.set_trainer(ChatterBotCorpusTrainer)
    bot.set_trainer(ListTrainer)
    # bot.train(['Lisa','What can i do for you, sir?'])

    # bot.train(['sinisa','What can i do for you, sir?'])
    # bot.train(['Vanessa','What can i do for you, sir?'])
    # bot.train(['Anissa','What can i do for you, sir?'])
    # bot.train(['Check, Please','OK,Please wait a second'])
    # bot.train('chatterbot.corpus.english')
    # bot.train(['Google something','what keyword you would like to google'])
    # bot.train(['give me some news','Ok sir, here are some news for you'])
    # bot.train(['show me some news','Ok sir, here are some news for you'])
    # bot.train(['what is new','Ok sir, here are some news for you'])
    # bot.train(['what is new','Ok sir, here are some news for you'])
    # bot.train(['i am ready to go','OK,Please wait a second'])
    # bot.train(['that is all i want','OK,Please wait a second'])
    # bot.train(['search something on wiki','what subject do you want to know'])

    # bot.train(['search on wiki','what subject do you want to know'])
    # bot.train(['Denisa','What can i do for you, sir?'])
    # bot.train(['Play video on Youtube','could you please provide the name of the video','hello','ok, here you are'])
    # bot.train(['check exchange rate','no problem sir, here is exchange rate for you'])

    response = str(bot.get_response(input))

    return response

def TextEnBot(input):
    TextBot = ChatBot('Elsa', 
        logic_adapters=[    
       {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_random_response"
        },
        {
            "import_path": "chatterbot.logic.MathematicalEvaluation"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'Sorry sir, I do not understand what you mean'
        },
        ],
        preprocessors=[
                'chatterbot.preprocessors.clean_whitespace'
            ],
        input_adapter="chatterbot.input.VariableInputTypeAdapter",
        output_adapter="chatterbot.output.OutputAdapter",
        statement_comparison_function=levenshtein_distance)

    TextBot.set_trainer(ChatterBotCorpusTrainer)
    # TextBot.train("chatterbot.corpus.english")


    response = str(TextBot.get_response(input))

    return response









def youtube_serach(input):
    keyword = input
    url = "https://www.youtube.com/results?search_query="
    res = requests.get(url+keyword)
    soup = BeautifulSoup(res.text,'html.parser')
    y_info = {}
    gi = 1
    
    for i in range(0,gi):
        a_title_1 = soup.select(".yt-uix-tile-link")[i].text
        a_link = soup.select(".yt-uix-tile-link")[i]
        ylink = a_link.get('href')
        youlink = 'https://www.youtube.com' + ylink 
        youtube_i = {i+1:{"title":a_title_1,"link":youlink}}
        print(youtube_i) #列出選項
        y_info[i+1] = {"title":a_title_1,"link":youlink}
        choice = 1
        user_choice = y_info[choice]
        u_link = user_choice['link']
        webbrowser.open(u_link, new=0, autoraise=True) #new=0, url會在同一個 瀏覽器視窗中開啟 ; new=1，新的瀏覽器視窗會被開啟 ; new=2  新的瀏覽器tab會被開啟



def google_search(key):
    keyword = key
    url = "https://www.google.com.tw/search?q="
    res = requests.get(url+keyword)
    soup = BeautifulSoup(res.text,'lxml')
    g_info = {}
    gs = 1
    for i in range(0,gs):
        a_title = soup.select(".r a")[i].text
        o_link = soup.select('.r a')[i]
        a_link0 = o_link.get('href')
        a_link = re.search (r'([https].*?:\/\/\w.*\/)',a_link0)
        if a_link:
            a_link = a_link.group(0)
            google_i = {i+1:{a_title:a_link}}
            print(google_i) #列出選項
        g_info[i+1] = {"title":a_title,"link":a_link}
        choice = 1
        user_choice = g_info[choice]
        u_link = user_choice['link']
        webbrowser.open(u_link, new=0, autoraise=True)

def wiki_key(keyword):
    # keyword = request.GET['keyword']
    url = "https://zh.wikipedia.org/wiki/"

    res = requests.get(url+keyword)
    soup = BeautifulSoup(res.text,'lxml')
    article = soup.select_one(".mw-parser-output p").text
    if len(article) > 30:
        print(article)
        data = {'triger':'wiki','article':article}
        return data
    elif len(article) <= 30:
        for i in range(0,len(soup)):
            article = soup.select(".mw-parser-output")[i].get_text()
            print(article)
            data = {'triger':'wiki','article':article}
            return data
    else:
        data = {'triger':'wiki','article':article}
        return data



def yahoo_news():
    url = "https://tw.news.yahoo.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    yahoo_news_title_info = {}
    title_lenth = soup.select(".nr-applet-main-nav-item") 
    for i in range(0,1):
        yahoo_title_1 = soup.select(".nr-applet-nav-item")[i].text
        a_link = soup.select(".nr-applet-nav-item")[i]
        yahoo_title_link = a_link.get('href')
        # print(yahoo_title_1)
        # print(yahoo_link) 
        if yahoo_title_link :
            yahoo_news = {i+1:{'class_title':yahoo_title_1,'yahoo_title_link':yahoo_title_link}}
            print(yahoo_news)# 列選項
        yahoo_news_title_info[i+1] = {'class_title':yahoo_title_1,'yahoo_title_link':yahoo_title_link}
        choice = 1
        user_choice = yahoo_news_title_info[choice]
        # print(user_choice)
        # print(type(user_choice))
        u_link = user_choice['yahoo_title_link']
        webbrowser.open(u_link, new=0, autoraise=True) 


def exchange():
    x = []
    exchange = "usd"
    exchange = exchange.upper()
    url = "http://www.taiwanrate.org/exchange_rate.php?c=" + exchange
    res = requests.get(url)
    res.encoding = 'utf-8'
    # soup = BeautifulSoup(res.text,'lxml')
    soup = BeautifulSoup(res.text,'html.parser')
    # print(soup)
    # ch = input('請問要即期還是現金: ')
    ch = "現金"
    if ch == "即期" or ch == "即期匯率":
        for i in range(0,19):
            bank_name = soup.select("#accounts a")[i].text
            print(bank_name)
            for i in range(0,57,1):
                bank_buy_sale = soup.select("#accounts td")[i].text
                print(bank_buy_sale)
    elif ch == "現金" or ch == "現金匯率":
        for i in range(0,18): #19間銀行
            bank_name = soup.select("#accounts2 a")[i].text
            print(bank_name)
            for i in range(0,54,1):
                bank_buy_sale = soup.select("#accounts2 td")[i].text
                # print(bank_buy_sale)
                x.append(bank_buy_sale+"\n")
            return x
    
    else:
        pass