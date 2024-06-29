from rest_framework import serializers
from .models import GameRound, RoundWinColor

class GameRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRound
        fields = '__all__'  # Or list the specific fields you want to include


class GameWin(serializers.ModelSerializer):
    game_id = serializers.SerializerMethodField()

    class Meta:
        model = RoundWinColor
        fields = '__all__'  # Or list the specific fields you want to include, including game_id

    def get_game_id(self, obj):
        return obj.round.game_id
