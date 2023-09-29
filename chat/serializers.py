from rest_framework import serializers
from .models import Room

class ChatRoomSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=255, required=True)
    name = serializers.CharField(max_length=255, required=True)
    
    def create(self,validated_date):
        room = Room.objects.create(
            uuid=validated_date.get('uuid'),
            client=validated_date.get('name'),
            url=validated_date.get('url'),
            )
        return room
    
    def update(self,validated_date):
        pass
    