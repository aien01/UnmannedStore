from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.Purchase,name='Bot'),
    path('bot/',views.BOT,name='BotConversation'),
    path('checkout/',views.Checkout,name='checkout'),
    path('speechbot/',views.SpeechBot,name='speechbot'),
    path('YoutubeSearch/',views.youtube_serach,name='YoutubeSearch'),
    path('googleSearch/',views.google_search,name='googleSearch'),
    path('wiki_key/',views.wiki_key,name='wiki_key'),
    path('yahoo_news/',views.yahoo_news,name='yahoo_news'),
    path('exchange/',views.exchange,name='exchange'),


]
