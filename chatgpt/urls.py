from django.urls import path
from .views import Askgpt,listen,askGroqDeck,CorreccionFrase


urlpatterns=[

    path('askgpt/',Askgpt),
    path('listenword/',listen),
    path('askGroq/',askGroqDeck),
    path ('SentenceCorrection/',CorreccionFrase)
]