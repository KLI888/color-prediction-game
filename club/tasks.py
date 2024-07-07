# from celery import shared_task
# from .models import *
# from django.utils import timezone
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from .serializers import GameRoundSerializer
# import time
# from django.contrib.auth.models import User


# @shared_task(bind=True)
# def test_func(self):
#     current_time = timezone.now()
#     game_round = GameRound.create_new_round(current_time.hour, current_time.minute, current_time.second)
#     serializer = GameRoundSerializer(game_round)
#     game_round_data = serializer.data
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         'test_consumer_group', {
#             'type': 'game_round_message',
#             'game_round': game_round_data
#         }
#     )
#     roundWinColor = RoundWinColor.objects.create(round=game_round)

#     def updateBalance(color):
#         try:
#             game_round = GameRound.objects.get(game_id=game_round.game_id)
#             bets_on_round = Bet.objects.filter(round=game_round, color=color).select_related('user')

#             user_bets = []
#             for bet in bets_on_round:
#                 user_bets.append({
#                     'user_id': bet.user.id,
#                     'username': bet.user.username,
#                     'bet_color': bet.color,
#                     'bet_amount': bet.amount
#             })
#             print("data filled in suer_bets successfully")
#             print(user_bets['user_id'])
#             for user_bet in user_bets:
#                 user = User.objects.get(id=user_bet['user_id'])
#                 profile = Profile.objects.get(user=user)
                
#                 # Calculate new_balance based on the bet amount
#                 bet_amount = int(user_bet['bet_amount'])
#                 if user_bet['bet_color'] == winning_color:
#                     new_balance = bet_amount * 2  # Double the bet amount for winners
#                 else:
#                     new_balance = bet_amount  # No change for non-winners
                
#                 profile.user_balance += new_balance
#                 profile.total_balance += new_balance
#                 profile.save()
#             print("data updated to user profile successfully")



#         except Exception as e:
#             print(e)




#     time.sleep(26)
#     roundWinColor = RoundWinColor.objects.get(round=game_round)
#     green_amount = roundWinColor.green_bet_amount
#     red_amount = roundWinColor.red_bet_amount
#     violet_amount = roundWinColor.violet_bet_amount

#     winning_color = ""
#     if green_amount > red_amount and green_amount > violet_amount:
#         # green_amount
#         roundWinColor.win_color = "Green"
#         roundWinColor.save()
#         updateBalance("Green")
#         winning_color = "Green"
#     elif red_amount > green_amount and red_amount > violet_amount:
#         # red_amount
#         roundWinColor.win_color = "Red"
#         roundWinColor.save()
#         updateBalance("Red")
#         winning_color = "Red"
#     else:
#         # violet_amount
#         roundWinColor.win_color = "Violet"
#         roundWinColor.save()
#         updateBalance("Violet")
#         winning_color = "Violet"
    

#     return "Donennnnnn"
from celery import shared_task
from .models import *
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import GameRoundSerializer, GameWin
import time
from django.contrib.auth.models import User

@shared_task(bind=True)
def test_func(self):
    current_time = timezone.now()
    game_round = GameRound.create_new_round(current_time.hour, current_time.minute, current_time.second)
    serializer = GameRoundSerializer(game_round)
    game_round_data = serializer.data
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'test_consumer_group', {
            'type': 'game_round_message',
            'game_round': game_round_data
        }
    )
    roundWinColor = RoundWinColor.objects.create(round=game_round)

    def updateBalance(winning_color):
        try:
            bets_on_round = Bet.objects.filter(round=game_round, color=winning_color).select_related('user')
            user_bets = []
            for bet in bets_on_round:
                user_bets.append({
                    'user_id': bet.user.id,
                    'username': bet.user.username,
                    'bet_color': bet.color,
                    'bet_amount': bet.amount
                })
            print("Data filled in user_bets successfully")

            for user_bet in user_bets:
                user = User.objects.get(id=user_bet['user_id'])
                profile = Profile.objects.get(user=user)
                bet_amount = int(user_bet['bet_amount'])
                new_balance = bet_amount * 2 if user_bet['bet_color'] == winning_color else 0
                profile.user_balance += new_balance
                profile.total_balance += new_balance
                profile.save()
            print("Data updated to user profile successfully")

        except Exception as e:
            print(f"Error: {e}")

    time.sleep(26)
    roundWinColor = RoundWinColor.objects.get(round=game_round)
    green_amount = roundWinColor.green_bet_amount
    red_amount = roundWinColor.red_bet_amount
    violet_amount = roundWinColor.violet_bet_amount

    winning_color = ""
    if green_amount < red_amount and green_amount < violet_amount:
        winning_color = "Green"
    elif red_amount < green_amount and red_amount < violet_amount:
        winning_color = "Red"
    else:
        winning_color = "Violet"

    roundWinColor.win_color = winning_color
    roundWinColor.save()
    updateBalance(winning_color)
    serializer = GameWin(roundWinColor)
    roundWinColor_data = serializer.data
    async_to_sync(channel_layer.group_send)(
        'test_consumer_group', {
            'type': 'game_round_message',
            'game_round': roundWinColor_data
        }
    )

    return "Done"
