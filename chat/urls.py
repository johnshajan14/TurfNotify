from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('send-message/', views.send_message, name='send_message'),
    path('get-messages/', views.get_messages, name='get_messages'),
    path('announcement/create/', views.create_announcement_view, name='create_announcement'),
    path('announcement/edit/<int:announcement_id>/', views.edit_announcement_view, name='edit_announcement'),
    path('announcement/delete/<int:announcement_id>/', views.delete_announcement_view, name='delete_announcement'),
]