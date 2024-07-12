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
from .serializers import GameRoundSerializer, GameWinSerializer
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
    roundWinNumber = RoundWinNumber.objects.create(round=game_round)
    roundWinSize = RoundWinSize.objects.create(round=game_round)
    roundWinAll = RoundWinAll.objects.create(round=game_round)

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


    def updateBalanceNumber(winning_number):
        try:
            bets_on_round = Bet.objects.filter(round=game_round, number=winning_number).select_related('user')
            user_bets = []
            for bet in bets_on_round:
                user_bets.append({
                    'user_id': bet.user.id,
                    'username': bet.user.username,
                    'bet_number': bet.number,
                    'bet_amount': bet.amount
                })
            print("Data filled in user_bets successfully")

            for user_bet in user_bets:
                user = User.objects.get(id=user_bet['user_id'])
                profile = Profile.objects.get(user=user)
                bet_amount = int(user_bet['bet_amount'])
                new_balance = bet_amount * 2 if user_bet['bet_number'] == winning_number else 0
                profile.user_balance += new_balance
                profile.total_balance += new_balance
                profile.save()
            print("Data updated to user profile successfully")

        except Exception as e:
            print(f"Error: {e}")


    def updateBalanceSize(winning_size):
        try:
            bets_on_round = Bet.objects.filter(round=game_round, size=winning_size).select_related('user')
            user_bets = []
            for bet in bets_on_round:
                user_bets.append({
                    'user_id': bet.user.id,
                    'username': bet.user.username,
                    'bet_size': bet.size,
                    'bet_amount': bet.amount
                })
            print("Data filled in user_bets successfully")

            for user_bet in user_bets:
                user = User.objects.get(id=user_bet['user_id'])
                profile = Profile.objects.get(user=user)
                bet_amount = int(user_bet['bet_amount'])
                new_balance = bet_amount * 2 if user_bet['bet_size'] == winning_number else 0
                profile.user_balance += new_balance
                profile.total_balance += new_balance
                profile.save()
            print("Data updated to user profile successfully")

        except Exception as e:
            print(f"Error: {e}")


    time.sleep(26)


    ## selecting the winning color
    roundWinColor = RoundWinColor.objects.get(round=game_round)
    green_amount = roundWinColor.green_bet_amount
    red_amount = roundWinColor.red_bet_amount
    violet_amount = roundWinColor.violet_bet_amount

    print("Winning color choosing here")
    winning_color = ""
    if green_amount < red_amount and green_amount < violet_amount:
        winning_color = "Green"
    elif red_amount < green_amount and red_amount < violet_amount:
        winning_color = "Red"
    else:
        winning_color = "Violet"
    print("Winning color choosing complete")
    roundWinColor.win_color = winning_color
    roundWinColor.save()
    updateBalance(winning_color)


    ## selecting the winning number
    roundWinNumber = RoundWinNumber.objects.get(round=game_round)

    # Extracting the bet amounts and mapping them to their corresponding numbers
    amounts = {
        0: roundWinNumber.zero_bet_amount,
        1: roundWinNumber.one_bet_amount,
        2: roundWinNumber.two_bet_amount,
        3: roundWinNumber.three_bet_amount,
        4: roundWinNumber.four_bet_amount,
        5: roundWinNumber.five_bet_amount,
        6: roundWinNumber.six_bet_amount,
        7: roundWinNumber.seven_bet_amount,
        8: roundWinNumber.eight_bet_amount,
        9: roundWinNumber.nine_bet_amount,
    }

    # Finding the minimum value
    min_amount = min(amounts.values())

    # Finding the number corresponding to the first occurrence of the minimum value
    for number, amount in amounts.items():
        if amount == min_amount:
            winning_number = number
            break
    roundWinNumber.win_number = str(winning_number)
    roundWinNumber.save()
    updateBalanceNumber(roundWinNumber.win_number)
    print(f"The first minimum bet amount is: {min_amount}, corresponding to number: {winning_number}")


    ## selecting the winning size
    roundWinSize = RoundWinSize.objects.get(round=game_round)
    if roundWinSize.big_bet_amount < roundWinSize.small_bet_amount:
        winning_size = "Big"
    else:
        winning_size = "Small"
    roundWinSize.win_size = winning_size
    roundWinSize.save()
    updateBalanceSize(winning_size)




    roundWinAll = RoundWinAll.objects.get(round=game_round)
    roundWinAll.win_color = winning_color
    roundWinAll.win_number = winning_number
    roundWinAll.win_size = winning_size
    print(winning_color)
    print(winning_number)
    print(winning_size)
    serializer = GameWinSerializer(roundWinAll)
    roundWinAll_data = serializer.data
    async_to_sync(channel_layer.group_send)(
        'test_consumer_group', {
            'type': 'game_round_result',
            'game_result_data': roundWinAll_data
        }
    )

    return "Done"
