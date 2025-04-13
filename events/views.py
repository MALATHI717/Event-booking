from django.shortcuts import render, redirect
from .models import Event, Booking
from django.contrib.auth.decorators import login_required
from .forms import EventForm  # You'll need to create this form
from .forms import ChatMessageForm 
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')  
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})
def chat_view(request):
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat_view')  # or reload the page
    else:
        form = ChatMessageForm()

    return render(request, 'events/chat.html', {'form': form})


@login_required
def book_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        seats = int(request.POST['seats'])
        if seats <= event.seats_available:
            booking = Booking.objects.create(user=request.user, event=event, seats_booked=seats)
            event.seats_available -= seats
            event.save()
            return redirect('booking_success')
        else:
            return render(request, 'events/book_event.html', {'event': event, 'error': 'Not enough seats available'})

    return render(request, 'events/book_event.html', {'event': event})

def booking_success(request):
    return render(request, 'events/booking_success.html')
