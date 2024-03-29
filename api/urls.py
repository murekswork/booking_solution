from django.urls import include, path

urlpatterns = [
    path('rooms/', include('rooms.urls')),
    path('bookings/', include('booking.urls')),
    path('accounts/', include('accounts.urls'))
]
