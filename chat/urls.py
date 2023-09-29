from django.urls import path
# from rest_framework.routers import DefaultRouter

from . import views

app_name = 'chat'
# router = DefaultRouter()
# router.register(r'api/create-room/<str:uuid>', views.ChatRoomViewSet, basename='chat-room-api')
# urlpatterns = router.urls
# [
#     path('api/create-room/<str:uuid>/', views.create_room, name='create-room'),
# ]

urlpatterns = [
    path('api/create-room/<str:uuid>/', views.create_room, name='create-room'),
    path('chat-admin/', views.admin, name='admin'),
    path('chat-admin/add-user/', views.add_user, name='add_user'),
    path('chat-admin/<uuid:uuid>/', views.get_user, name='get_user '),
    path('chat-admin/<str:uuid>/delete', views.room_delete, name='delete_room'),
    
    path('chat-admin/users/<str:uuid>/', views.room, name='room'),
]

