import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs']['ride_id']

        # Check if user belongs to this ride
        user = self.scope["user"]
        if not await self.is_user_allowed(self.ride_id, user):
            # If user is not allowed, close the connection
            await self.close()
            return

        # Join the ride group
        self.room_group_name = f'ride_{self.ride_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'message': f'Connected to chat for ride {self.ride_id}',
            'username': 'System'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')

        user = self.scope["user"] if self.scope["user"].is_authenticated else None
        await self.save_message(self.ride_id, user, message)

        username = user.username if user else "Guest"

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    @database_sync_to_async
    def save_message(self, ride_id, user, message):
        from .models import ChatMessage, SharedRide
        # Use your existing ChatMessage model
        ride = SharedRide.objects.get(id=ride_id)
        ChatMessage.objects.create(
            ride=ride,
            sender=user,
            content=message
        )

    @database_sync_to_async
    def is_user_allowed(self, ride_id, user):
        """Check if the user is organizer or invited to this ride."""
        from .models import SharedRide
        try:
            ride = SharedRide.objects.get(id=ride_id)
        except SharedRide.DoesNotExist:
            return False

        # Allow only organizer or invited users
        return (
            user.is_authenticated and
            (user == ride.organizer or ride.invites.filter(invitee=user).exists())
        )
