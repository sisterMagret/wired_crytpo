import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timesince import timesince
from .models import Message, Room
from account.models import User
from .templatetags.chatextras import initials


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs'].get('room_name')
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        # Join room group
        await self.get_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        #inform user
        if self.user.is_staff:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'users_update', 
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        if not self.user.is_staff:
            await self.set_room_close()

    async def receive(self, text_data=None, bytes_data=None):
        # receive message from the client
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']
        agent = text_data_json.get('agent','')

        if type == 'message':
            new_message = await self.create_message(name, message, agent)
            # send message room
            await self.channel_layer.group_send(
                self.room_group_name,{
                    'type': 'chat_message', 
                    'message': message,
                    'name': name,
                    'agent': agent,
                    'initials': initials(name),
                    'created_at': timesince(new_message.created_at)
            })
        # elif type == 'update':
        #     # send update to the room
        #     await self.channel_layer.group_send(
        #         self.room_group_name,{
        #             'type': 'writing_active', 
        #             'message': message,
        #             'name': name,
        #             'agent': agent,
        #             'initials': initials(name),
        #     })

    # async def writing_active(self, event):
    #     # send writing is active to user
    #     await self.send(text_data=json.dumps({
    #         'type': event.get('type'),
    #         'message': event.get('message'),
    #         'name': event.get('name'),
    #         'agent': event.get('agent'),
    #         'initials': event.get('initials')
    #     }))


    async def chat_message(self,event):
        #send message to client

        await self.send(text_data=json.dumps({
            'type': event.get('type'),
            'message': event.get('message'),
            'name': event.get('name'),
            'agent': event.get('agent'),
            'initials': event.get('initials'),
            'created_at': event.get('created_at'),
        }))

    async def users_update(self,event):
        #send information to the client 
        await self.send(text_data=json.dumps({
            'type': 'users_update',
        }))

    @sync_to_async
    def create_message(self,sent_by,message,agent):
        message = Message.objects.create(body=message,sent_by=sent_by) 

        if agent:
            message.created_by = User.objects.get(pk=agent)
            message.save()

        self.room.messages.add(message)

        return message
    
    @sync_to_async
    def get_room(self):
        self.room = Room.objects.get(uuid=self.room_name)

    @sync_to_async
    def set_room_close(self):
        self.room = Room.objects.get(uuid=self.room_name)
        self.room.status = Room.CLOSED
        self.room.save() 
