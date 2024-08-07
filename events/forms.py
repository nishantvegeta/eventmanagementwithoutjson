from django import forms
from .models import Event, Booking

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'total_participants', 'start_date', 'end_date', 'image','location']


class EventFilterForm(forms.Form):
    title = forms.CharField(required=False, label='Title')


class EventBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []

        