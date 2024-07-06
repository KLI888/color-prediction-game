from django.urls import path, include
from .views import *
urlpatterns = [
    # path('', test, name='test')
    path('', home, name='home'),
    # path('test/', test, name='test'),

    # login pages
    path('loginPage', loginPage, name='loginPage'),
    path('logoutPage', logoutPage, name='logoutPage'),
    path('registerPage', registerPage, name='registerPage'),


    # account pages
    path('accountPage', accountPage, name='accountPage'),
    path('depositePage', depositePage, name='depositePage'),
    path('withdrawPage', withdrawPage, name='withdrawPage'),
    path('walletPage', walletPage, name='walletPage'),


    # game page
    path('wingoPage', wingoPage, name='wingoPage'),

    # account info pages
    path('aboutPage', aboutPage, name='aboutPage'),
    path('settingsPage', settingsPage, name='settingsPage'),
    path('guidePage', guidePage, name='guidePage'),
    path('feedbackPage', feedbackPage, name='feedbackPage'),


    # game api
    path('api/game_bet', user_bet, name='user_bet')
]
