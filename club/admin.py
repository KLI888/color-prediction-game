from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(GameRound)
admin.site.register(Bet)
admin.site.register(Withdraw)
admin.site.register(Deposit)
admin.site.register(RoundWinColor)