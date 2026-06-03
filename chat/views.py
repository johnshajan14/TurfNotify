from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from events.models import Event
from .models import Message, Announcement

@login_required(login_url='/')
def home_view(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    messages = Message.objects.all().order_by('created_at')
    user_events = Event.objects.filter(created_by=request.user)
    is_event_creator = user_events.exists()
    return render(request, 'home.html', {
        'announcements': announcements,
        'messages': messages,
        'is_event_creator': is_event_creator
    })

@login_required(login_url='/')
def create_announcement_view(request):
    user_events = Event.objects.filter(created_by=request.user)
    if not user_events.exists():
        return redirect('/home/')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if title and content:
            Announcement.objects.create(
                title=title,
                content=content
            )
        return redirect('/home/')

    return render(request, 'create_announcement.html')

@login_required(login_url='/')
def edit_announcement_view(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    user_events = Event.objects.filter(created_by=request.user)
    if not user_events.exists():
        return redirect('/home/')

    if request.method == 'POST':
        announcement.title = request.POST.get('title', '').strip()
        announcement.content = request.POST.get('content', '').strip()
        announcement.save()
        return redirect('/home/')

    return render(request, 'edit_announcement.html', {'announcement': announcement})

@login_required(login_url='/')
def delete_announcement_view(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    user_events = Event.objects.filter(created_by=request.user)
    if not user_events.exists():
        return redirect('/home/')
    announcement.delete()
    return redirect('/home/')

@login_required(login_url='/')
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(user=request.user, content=content)
    return redirect('/home/')

@login_required(login_url='/')
def get_messages(request):
    messages = Message.objects.all().order_by('created_at')
    data = [
        {
            'user': msg.user.username,
            'content': msg.content,
            'time': msg.created_at.strftime('%I:%M %p')
        }
        for msg in messages
    ]
    return JsonResponse({'messages': data})