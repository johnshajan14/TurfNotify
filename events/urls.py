from django.urls import path
from .views import (
    create_event_view,
    event_detail_view,
    edit_event_view,
    delete_event_view
)

urlpatterns = [

    path(
        'create-event/',
        create_event_view,
        name='create_event'
    ),

    path(
        'event/<int:event_id>/',
        event_detail_view,
        name='event_detail'
    ),

    path(
        'event/<int:event_id>/edit/',
        edit_event_view,
        name='edit_event'
    ),

    path(
        'event/<int:event_id>/delete/',
        delete_event_view,
        name='delete_event'
    ),

]