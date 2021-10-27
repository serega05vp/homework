from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.EmailHandlerAPIView.as_view(), name="email-handler"),

    # authorization
    path('account/token/', obtain_jwt_token, name="token"),
]
