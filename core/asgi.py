import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from simple_app.consumers import BingoConsumer, BMIConsumer, EchoConsumer, SocialNetworkConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter([
            re_path(r'^ws/echo/$', EchoConsumer.as_asgi()),
            re_path(r'^ws/bingo/$', BingoConsumer.as_asgi()),
            re_path(r'^ws/bmi/$', BMIConsumer.as_asgi()),
            re_path(r'^ws/social-network/$', SocialNetworkConsumer.as_asgi()),
        ])
    )
})