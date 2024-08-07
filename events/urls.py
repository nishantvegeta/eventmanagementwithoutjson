from django.urls import path
from . import views

urlpatterns = [
    path('event/', views.events, name='event_list'),
    path('event/create/', views.create_event, name='event_create'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path('event/update/<int:id>/', views.update_event, name='event_update'),
    path('event/delete/<int:id>/', views.delete_event, name='event_delete'),
    path('book/<int:id>/', views.book_event, name='book_event'),
]