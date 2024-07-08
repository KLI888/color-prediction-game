from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code

import random

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    code = models.CharField(max_length=50, default='', blank=True)
    user_code = models.CharField(max_length=12, blank=True, null=True)
    recomended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
    referals_number = models.IntegerField(blank=True, default=0)


    user_balance = models.IntegerField(blank=True, default=0)

    refer_code = models.CharField(max_length=50, blank=True, null=True)

    total_balance = models.IntegerField(blank=True, default=0)
    total_withdraw = models.IntegerField(blank=True, default=0)
    total_deposite = models.IntegerField(blank=True, default=0)


    def __str__(self):
        return f"{self.user.username}"

    def get_recommended_profiles(self):
        pass

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)

from django.utils import timezone
from django.db.models import Max

class GameRound(models.Model):


    game_id = models.IntegerField(default=20000000) 

    start_hour = models.IntegerField(default=0)
    start_minute = models.IntegerField(default=0)
    start_second = models.IntegerField(default=0)


    duration = models.IntegerField(default=30)
    # created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     get_latest_by = 'created_at'

    def save(self, *args, **kwargs):
        if self.game_id == 20000000:
            max_id = GameRound.objects.aggregate(max_id=Max('game_id'))['max_id']
            if max_id is None:
                self.game_id = 20000000
            else:
                self.game_id = max_id + 1
        super().save(*args, **kwargs)


    @staticmethod
    def give_round_details(game_id):
        round = GameRound.objects.get(game_id=game_id)
        data = {}
        data['game_id'] = round.game_id
        data['start_hour'] = round.start_hour
        data['start_minute'] = round.start_minute
        data['start_second'] = round.start_second
        data['duration'] = round.duration

        return data


    @staticmethod
    def create_new_round(hour, minute, second):
        return GameRound.objects.create(
            start_hour=hour,
            start_minute=minute,
            start_second=second
        )


    def __str__(self):
        return f"{self.game_id}->{self.start_hour}:{self.start_minute}:{self.start_second}"
    
            

class RoundWinNumber(models.Model):
    NUMBER_CHOICES = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
    ]
    round = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    default_number = str(random.randint(0, 9))
    win_number = models.CharField(max_length=10, choices=NUMBER_CHOICES, blank=True, default=default_number)

    zero_bet_amount = models.IntegerField(default=0)
    one_bet_amount = models.IntegerField(default=0)
    two_bet_amount = models.IntegerField(default=0)
    three_bet_amount = models.IntegerField(default=0)
    four_bet_amount = models.IntegerField(default=0)
    five_bet_amount = models.IntegerField(default=0)
    six_bet_amount = models.IntegerField(default=0)
    seven_bet_amount = models.IntegerField(default=0)
    eight_bet_amount = models.IntegerField(default=0)
    nine_bet_amount = models.IntegerField(default=0)


    def __str__(self):
        return f"Round: {self.round.game_id}"
    

class RoundWinSize(models.Model):
    SIZE_CHOICES = [
        ('Big', 'Big'),
        ('Small', 'Small'),
    ]
    round = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    win_size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True, default="Small")
    big_bet_amount = models.IntegerField(default=0)
    small_bet_amount = models.IntegerField(default=0)
    violet_bet_amount = models.IntegerField(default=0)

    
    def __str__(self):
        return f"Round: {self.round.game_id}"


class RoundWinColor(models.Model):
    COLOR_CHOICES = [
        ('Red', 'Red'),
        ('Green', 'Green'),
        ('Violet', 'Violet')
    ]
    round = models.ForeignKey(GameRound, on_delete=models.CASCADE)

    win_color = models.CharField(max_length=10, choices=COLOR_CHOICES, blank=True, default="Violet")
    red_bet_amount = models.IntegerField(default=0)
    green_bet_amount = models.IntegerField(default=0)
    violet_bet_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"Round: {self.round.game_id}"
    
class RoundWinAll(models.Model):
    round = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    roundWinColor = models.ForeignKey(RoundWinColor, on_delete=models.CASCADE)
    roundWinSize = models.ForeignKey(RoundWinSize, on_delete=models.CASCADE)
    roundWinNumber = models.ForeignKey(RoundWinNumber, on_delete=models.CASCADE)

    def __str__(self):
        return f"Round Win {round}"
    

class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.ForeignKey(GameRound, on_delete=models.CASCADE)
    color = models.CharField(max_length=10, null=True, blank=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    size = models.CharField(max_length=10, null=True, blank=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Bet on {self.color} in Round {self.round_id}"


class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)
    upi_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user}->{self.amount}"


class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)
    utr_no = models.CharField(max_length=100)
    payment_img = models.ImageField(upload_to="depositeScreenshot/")

    def __str__(self):
        return f"Deposite: {self.user}->{self.amount}"

