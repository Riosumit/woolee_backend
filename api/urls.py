from django.urls import path
from .views import ProducerView, LoginView, RegisterView, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view(), name='regiser'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('producers', ProducerView.as_view(), name='producer_list'),
    path('producer/<int:pk>', ProducerView.as_view(), name='producer_detail'),
]
