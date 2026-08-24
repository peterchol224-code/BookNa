from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path(
        'hotel/<int:hotel_id>/',
        views.hotel_detail,
        name='hotel_detail',
    ),
    path(
        'book/<int:hotel_id>/',
        views.book_hotel,
        name='book_hotel',
    ),
    path(
        'confirmation/<int:booking_id>/',
        views.booking_confirmation,
        name='booking_confirmation',
    ),
    path(
        'owners/register/',
        views.owner_register,
        name='owner_register',
    ),
    path(
        'owners/login/',
        auth_views.LoginView.as_view(
            template_name='hotels/owner_login.html',
            redirect_authenticated_user=True,
        ),
        name='owner_login',
    ),
    path(
        'owners/dashboard/',
        views.owner_dashboard,
        name='owner_dashboard',
    ),
    path(
        'owners/bookings/<int:booking_id>/status/',
        views.owner_booking_status,
        name='owner_booking_status',
    ),
    path(
        'owners/logout/',
        views.owner_logout,
        name='owner_logout',
    ),
]