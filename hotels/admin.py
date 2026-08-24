from django.contrib import admin

from .models import Booking, Hotel, HotelPhoto, OwnerProfile


class HotelPhotoInline(admin.TabularInline):
    model = HotelPhoto
    extra = 3


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'city',
        'price_per_night',
        'rooms_available',
        'is_verified',
    )
    search_fields = ('name', 'city')
    list_filter = ('city', 'is_verified')
    inlines = [HotelPhotoInline]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'guest_name',
        'hotel',
        'check_in',
        'check_out',
        'number_of_guests',
        'number_of_rooms',
        'status',
        'created_at',
    )
    search_fields = (
        'guest_name',
        'guest_phone',
        'guest_email',
        'hotel__name',
    )
    list_filter = ('status', 'hotel', 'check_in')


@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'hotel',
        'created_at',
    )
    search_fields = (
        'user__username',
        'user__email',
        'hotel__name',
    )
    list_filter = ('hotel',)