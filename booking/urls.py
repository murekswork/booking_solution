from django.urls import path

from .views import BookingListCreateAPIView, BookingRetrieveUpdateAPIView

urlpatterns = [
    path('', BookingListCreateAPIView.as_view(), name='booking-create'),
    path('', BookingListCreateAPIView.as_view(), name='booking-my'),
    path('<int:pk>', BookingRetrieveUpdateAPIView.as_view(), name='booking-detail'),
    path('<int:pk>', BookingRetrieveUpdateAPIView.as_view(), name='booking-update')
]
