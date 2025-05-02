import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Pair_room, Message
from lk.models import UserProfile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['match_id']
        self.group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if not all(key in data for key in ['message', 'sender']):
                raise ValueError('Invalid data format')

            saved = await self.save_message(
                data['message'],
                data['sender'],
                self.room_name
            )

            if saved:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'chat_message',
                        'message': data['message'],
                        'sender': data['sender'],
                        'saved': True
                    }
                )

        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error processing message: {str(e)}")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'saved': event['saved']
        }))

    @database_sync_to_async
    def save_message(self, message, sender_username, room_name):
        try:
            user = UserProfile.objects.get(user__username=sender_username)
            room = Pair_room.objects.get(room_name=room_name)

            if user == room.user1:
                receiver = room.user2
            elif user == room.user2:
                receiver = room.user1
            else:
                raise ValueError("Sender is not a room participant")

            Message.objects.create(
                room=room,
                sender=user,
                receiver=receiver,
                message=message
            )
            return True

        except UserProfile.DoesNotExist:
            print(f"User {sender_username} not found")
            return False
        except Pair_room.DoesNotExist:
            print(f"Room {room_name} not found")
            return False
        except Exception as e:
            print(f"Error saving message: {str(e)}")
            return False