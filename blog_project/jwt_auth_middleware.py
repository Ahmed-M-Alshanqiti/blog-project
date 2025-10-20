from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

@database_sync_to_async
def get_user_from_token(token_key):
    try:
        
        token = AccessToken(token_key)
        user_id = token['user_id']
        
        
        User = get_user_model()
        return User.objects.get(id=user_id)
        
    except TokenError:
        
        return AnonymousUser()
    except User.DoesNotExist:
        
        return AnonymousUser()
    except Exception:
        
        return AnonymousUser()

class JWTAuthMiddleware:
    
    def __init__(self, app):
        
        self.app = app

    async def __call__(self, scope, receive, send):
       
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        
        token_key = query_params.get('token', [None])[0]

        if token_key:
            
            scope['user'] = await get_user_from_token(token_key)
        else:
           
            scope['user'] = AnonymousUser()

        
        return await self.app(scope, receive, send)

def JWTAuthMiddlewareStack(app):
    return JWTAuthMiddleware(app) 