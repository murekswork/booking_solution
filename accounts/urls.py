from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from accounts.views import LoginAPIView, LogoutAPIView, SignUpAPIView

urlpatterns = [
    path('obtain_token/', obtain_auth_token, name='obtain_token'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('signup/', SignUpAPIView.as_view(), name='signup'),
]
