from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum

from .models import Booking, Hotel


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'guest_name',
            'guest_email',
            'guest_phone',
            'check_in',
            'check_out',
            'number_of_guests',
            'number_of_rooms',
        ]
        labels = {
            'guest_name': 'Full name',
            'guest_email': 'Email address (optional)',
            'guest_phone': 'Phone or WhatsApp number',
            'check_in': 'Check-in date',
            'check_out': 'Check-out date',
            'number_of_guests': 'Number of guests',
            'number_of_rooms': 'Number of rooms',
        }
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, hotel=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.hotel = hotel

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        number_of_rooms = cleaned_data.get('number_of_rooms')

        if check_in and check_out and check_out <= check_in:
            self.add_error(
                'check_out',
                'Check-out must be after the check-in date.',
            )
            return cleaned_data

        if (
            self.hotel
            and check_in
            and check_out
            and number_of_rooms
        ):
            reserved_rooms = Booking.objects.filter(
                hotel=self.hotel,
                status__in=['pending', 'confirmed'],
                check_in__lt=check_out,
                check_out__gt=check_in,
            ).aggregate(
                total=Sum('number_of_rooms')
            )['total'] or 0

            remaining_rooms = (
                self.hotel.rooms_available - reserved_rooms
            )

            if number_of_rooms > remaining_rooms:
                self.add_error(
                    'number_of_rooms',
                    (
                        f'Only {remaining_rooms} room(s) are '
                        'available for these dates.'
                    ),
                )

        return cleaned_data


class OwnerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class HotelAvailabilityForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ('rooms_available',)
        labels = {
            'rooms_available': 'Total rooms available',
        }


class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('status',)