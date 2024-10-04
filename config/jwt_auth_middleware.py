import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()



@database_sync_to_async
def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return User.objects.get(id=payload['user_id'])
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return AnonymousUser()

class JWTAuthMiddleware:
    """
    Custom middleware that extracts JWT from the headers and authenticates the user.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        token = None

        # Extract the token from the headers
        for header in scope['headers']:
            if header[0] == b'authorization':
                auth_header = header[1].decode('utf-8')
                parts = auth_header.split(' ')
                if len(parts) == 2 and parts[0].lower() == 'bearer':
                    token = parts[1]  # Get the token part
                break

        # Default to AnonymousUser
        scope['user'] = AnonymousUser()

        if token:
            # Set the user based on the JWT token
            scope['user'] = await get_user_from_token(token)

        return await self.app(scope, receive, send)