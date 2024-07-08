from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import *



class TestConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = 'test_consumer'
        self.room_group_name = 'test_consumer_group'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'you are connected successfully'}))
    
    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=json.dumps({'status': 'we have your data'}))

    
    async def disconnect(self, close_code):
        # await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # await self.send(close_code=json.dumps({'status': 'Disconnected'}))
        print("Disconnected")

    async def game_round_message(self, event):
        game_round = event['game_round']
        await self.send(text_data=json.dumps({
            'game_round': game_round
        }))

    async def game_round_result(self, event):
        game_round_winner = event['game_result_data']
        await self.send(text_data=json.dumps({
            'game_result_data': game_round_winner
        }))

