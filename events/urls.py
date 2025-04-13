from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('add/', views.add_event, name='add_event'),  # This is the important line
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('chat/', views.chat_view, name='chat_view'),
]
