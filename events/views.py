from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Event, Booking
from django.shortcuts import redirect, render, get_object_or_404
from .forms import EventForm, EventFilterForm, EventBookingForm
from django.contrib import messages


def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func


@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
@login_required


def home_page(request):
    return render(request, 'events/base.html', {})

def events(request):
    events = Event.objects.all()

    filter_form = EventFilterForm(request.GET)
    if filter_form.is_valid():
        title = filter_form.cleaned_data.get('title')
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')

        if title:
            events = events.filter(title__icontains=title)

    for event in events:
        event.is_booked = Booking.objects.filter(user=request.user, event=event).exists()

    return render(request, 'events/event_list.html', {'events':events, 'filter_form': filter_form})
    
@login_required
def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'events/event_detail.html', {'event': event})

@csrf_exempt
@require_http_methods(['GET', 'POST'])
@admin_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form':form})
        
@admin_required
def update_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'GET':
        return render(request, 'events/event_form.html', { 'event': event})
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return render(request, 'events/event_list.html')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_list.html', {'form': form})

@admin_required
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'GET':
        return render(request, 'events/event_confirm_delete.html',{'event':event})
    elif request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return redirect(request, 'events/event_list.html', {'event': event})

@login_required
def book_event(request, id):
    event = get_object_or_404(Event,id=id)
    if request.method == 'GET':
        return render(request, 'events/book_event.html',{'event': event})

    if request.method == 'POST':
        booking_form = EventBookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.event = event
            booking.save()
            event.total_participants += 1
            messages.success(request, f'You have successfully booked {event.title}!')
            return redirect('event_list')
    else:
        booking_form = EventBookingForm()

    return render(request, 'events/book_event.html',{'booking_form': booking_form, 'event': event})