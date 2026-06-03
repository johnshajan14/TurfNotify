from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache  # ← ADD HERE
from .models import Event
from responses.models import Response

@never_cache
def create_event_view(request):

    if request.method == "POST":

        Event.objects.create(
            title=request.POST['title'],
            event_date=request.POST['event_date'],
            event_time=request.POST['event_time'],
            location=request.POST['location'],
            max_players=request.POST['max_players'],
            announcement=request.POST.get('announcement', ''),
            created_by=request.user
        )

        return redirect('/dashboard/')

    return render(request, 'create_event.html')

@never_cache
def event_detail_view(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    confirmed_players = Response.objects.filter(
        event=event,
        response='YES'
    )

    # Mark Paid / Unpaid
    if request.method == "POST" and "payment_response_id" in request.POST:

        response_obj = get_object_or_404(
            Response,
            id=request.POST["payment_response_id"]
        )

        if request.user == event.created_by:
            response_obj.is_paid = not response_obj.is_paid
            response_obj.save()

        return redirect(f'/event/{event.id}/')

    # YES / NO Response
    if request.method == "POST":

        response_value = request.POST.get('response')

        if response_value:

            if (
                response_value == "YES"
                and confirmed_players.count() >= event.max_players
            ):
                return redirect(f'/event/{event.id}/')

            reason = request.POST.get('reason', '')

            Response.objects.update_or_create(
                user=request.user,
                event=event,
                defaults={
                    'response': response_value,
                    'reason': reason
                }
            )

            return redirect(f'/event/{event.id}/')

    confirmed_players = Response.objects.filter(
        event=event,
        response='YES'
    )

    declined_players = Response.objects.filter(
        event=event,
        response='NO'
    )

    confirmed_count = confirmed_players.count()

    declined_count = declined_players.count()

    paid_count = confirmed_players.filter(
        is_paid=True
    ).count()

    unpaid_count = confirmed_players.filter(
        is_paid=False
    ).count()

    spots_left = event.max_players - confirmed_count

    is_full = confirmed_count >= event.max_players

    return render(
        request,
        'event_detail.html',
        {
            'event': event,
            'confirmed_players': confirmed_players,
            'declined_players': declined_players,
            'confirmed_count': confirmed_count,
            'declined_count': declined_count,
            'paid_count': paid_count,
            'unpaid_count': unpaid_count,
            'spots_left': spots_left,
            'is_full': is_full
        }
    )

@never_cache
def edit_event_view(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    if request.user != event.created_by:
        return redirect('/dashboard/')

    if request.method == "POST":
        event.title = request.POST['title']
        event.event_date = request.POST['event_date']
        event.event_time = request.POST['event_time']
        event.location = request.POST['location']
        event.max_players = request.POST['max_players']
        event.announcement = request.POST.get('announcement', '')
        event.save()

        from chat.models import Announcement
        announcement_text = request.POST.get('announcement', '').strip()
        announcement_title = request.POST.get('announcement_title', '').strip()
        if announcement_text:
            Announcement.objects.update_or_create(
                title=f"📅 New Event: {event.title}",
                defaults={
                    'title': announcement_title or f"📅 {event.title} - Update",
                    'content': f"{announcement_text}\n\n📍 {event.location} | 🗓 {event.event_date} | ⏰ {event.event_time}"
                }
            )

        return redirect(f'/event/{event.id}/')

    return render(request, 'edit_event.html', {'event': event})

@never_cache
def delete_event_view(request, event_id):

    event = get_object_or_404(
        Event,
        id=event_id
    )

    if request.user != event.created_by:
        return redirect('/dashboard/')

    if request.method == "POST":

        event.delete()

        return redirect('/dashboard/')

    return render(
        request,
        'delete_event.html',
        {
            'event': event
        }
    )