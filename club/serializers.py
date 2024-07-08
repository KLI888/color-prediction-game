from rest_framework import serializers
from .models import *

class GameRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRound
        fields = '__all__'  # Or list the specific fields you want to include


# class GameWin(serializers.ModelSerializer):
#     game_id = serializers.SerializerMethodField()

#     class Meta:
#         model = RoundWinColor
#         fields = '__all__'  # Or list the specific fields you want to include, including game_id

#     def get_game_id(self, obj):
#         return obj.round.game_id


from rest_framework import serializers
from .models import RoundWinColor, RoundWinSize, RoundWinNumber, RoundWinAll

class RoundWinColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundWinColor
        fields = '__all__'

class RoundWinSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundWinSize
        fields = '__all__'

class RoundWinNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoundWinNumber
        fields = '__all__'

class GameWinSerializer(serializers.ModelSerializer):
    roundWinColor = RoundWinColorSerializer()
    roundWinSize = RoundWinSizeSerializer()
    roundWinNumber = RoundWinNumberSerializer()

    class Meta:
        model = RoundWinAll
        fields = ('id', 'game_id', 'roundWinColor', 'roundWinSize', 'roundWinNumber')

    def get_game_id(self, obj):
        return obj.round.game_id
