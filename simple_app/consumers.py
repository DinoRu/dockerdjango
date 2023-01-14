from this import d
import threading
import time
from datetime import datetime
from random import randint

from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from django.template.loader import render_to_string

from asgiref.sync import async_to_sync

from .models import Message

class EchoConsumer(WebsocketConsumer):

    def connect(self):
        """Event when client connets"""
        # Informs client of successful connection
        self.accept()

        # Send message to client
        self.send(text_data="You are connected by WebSockets!")

        # Send message to client every second
        def send_time(self):
            while True:
                # Send message to client
                self.send(text_data=str(datetime.now().strftime("%H:%M:%S")))
                # Sleep for 1 second
                time.sleep(1)
        threading.Thread(target=send_time, args=(self,)).start()
    
    def disconnect(self, close_code):
        """Event when client disconnect"""
        pass
    
    def receive(self, text_data):
        """Event when data is received"""
        pass

class BingoConsumer(JsonWebsocketConsumer):
    
    def connect(self):
        self.accept()
        ## Send numbers to client
        # Generates numbers 5 random numbers, approximately, between 1 and 10
        random_numbers = list(set([randint(0, 10) for _ in range(5)]))
        messages = {
            'action': 'New ticket',
            'ticket': random_numbers,
        }
        self.send_json(content=messages)

        ## Send balls
        def send_balls(self):
            while True:
                # Send message to client
                random_ball = randint(1, 10)
                message = {
                    'action': 'New ball',
                    'ball': random_ball
                }
                self.send_json(content=message)
                # Sleep for 1 second
                time.sleep(1)
        threading.Thread(target=send_balls, args=(self,)).start()

    def disconnect(self, close_code):
        pass

    def receive_json(self, data):
        pass
    

class BMIConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
    
    def disconnect(self, close_code):
        pass
    def receive_json(self, data):
        """Event when data is received"""
        height = data['height'] / 100
        weight = data['weight']
        bmi = round(weight / (height ** 2), 1)
        self.send_json(content={
            "action": "BMI result",
            "html": render_to_string("components/_bmi_result.html", {'weight': weight, 'height': height, 'bmi': bmi}),

        })


class SocialNetworkConsumer(JsonWebsocketConsumer):
    room_name = 'broadcast'

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.send_list_messages()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive(self, data):

        author = data['author']
        text = data['text']
        contenu = author + '\n' + text
        self.send_json(content={
            'action': 'Add messages',
            'html': render_to_string("components/_list_messages.html", {'author': author, 'text': text, 'contenu': contenu})
        })