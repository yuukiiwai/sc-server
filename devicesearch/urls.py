from django.urls import path,include
from .views import *

app_name = 'devicesearch'

urlpatterns = [
    path('',top),
    path('appsat/gra/',getAppSat_Gra.as_view()),
    path('appsat/gra/<id>',getGra.as_view()),
    #path('appsat/mem/',getAppSat_Mem.as_view()),
    path('apps/',AllApp.as_view()),
    path('gras/',AllGra.as_view()),
    path('recommend/',Recommend.as_view()),
]

""" 
appsat/gra/ ... app名からgraphicscard
appsat/mem/ ... app名からmemory
apps/       ... 登録アプリ名一覧
gra/        ... 登録グラフィックカード一覧
recommend/  ... おすすめ
"""