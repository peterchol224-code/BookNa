from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import OwnerProfile, Booking, Hotel


def home(request):
    return render(request, "hotels/home.html")


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    return render(
        request,
        "hotels/hotel_detail.html",
        {
            "hotel": hotel,
        },
    )


@login_required
def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    return render(
        request,
        "hotels/book_hotel.html",
        {
            "hotel": hotel,
        },
    )


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    return render(
        request,
        "hotels/booking_confirmation.html",
        {
            "booking": booking,
        },
    )


def owner_register(request):
    return render(request, "hotels/owner_register.html")


@login_required
def owner_dashboard(request):
    profile, created = OwnerProfile.objects.get_or_create(
        user=request.user
    )

    if not profile.hotel:
        return render(
            request,
            "hotels/owner_dashboard.html",
            {
                "profile": profile,
                "hotel": None,
                "bookings": [],
            },
        )

    hotel = profile.hotel

    bookings = Booking.objects.filter(
        hotel=hotel
    ).order_by("-created_at")

    return render(
        request,
        "hotels/owner_dashboard.html",
        {
            "profile": profile,
            "hotel": hotel,
            "bookings": bookings,
        },
    )
@login_required
def owner_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    return render(
        request,
        "hotels/owner_booking_status.html",
        {
            "booking": booking,
        },
    )
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def owner_logout(request):
    logout(request)
    return redirect("owner_login")