from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')

    return render(request, 'login.html')


def register_view(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('/')

    return render(request, 'register.html')


def dashboard_view(request):

    from events.models import Event

    events = Event.objects.all().order_by('-event_date')

    return render(
        request,
        'dashboard.html',
        {'events': events}
    )


def logout_view(request):
    logout(request)
    return redirect('/')