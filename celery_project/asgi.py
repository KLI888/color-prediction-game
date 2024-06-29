import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_project.settings')

# Setup Django before importing consumers
django.setup()

from club.consumers import TestConsumer

ws_patterns = [
    path('ws/test/', TestConsumer.as_asgi()),  # Use .as_asgi() here
    path('ws/game_result/', TestConsumer.as_asgi()),  # Use .as_asgi() here
]

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(ws_patterns),
})
