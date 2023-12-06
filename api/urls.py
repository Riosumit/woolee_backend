from django.urls import path
from .views import ProducerView

urlpatterns = [
    path('producers', ProducerView.as_view(), name='producer_list'),
    path('producer/<int:pk>', ProducerView.as_view(), name='producer_detail'),
]
