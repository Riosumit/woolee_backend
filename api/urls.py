from django.urls import path
from .views import ProducerView, LoginView, RegisterView, LogoutView, QRCodeView, ProcessorView, ServiceProviderView, ServiceRequestView

urlpatterns = [
    path('register', RegisterView.as_view(), name='regiser'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('producers', ProducerView.as_view(), name='producer_list'),
    path('producer/<int:pk>', ProducerView.as_view(), name='producer_detail'),
    path('service_requests', ServiceRequestView.as_view(), name='service_request_list'),
    path('service_request/<int:pk>', ServiceRequestView.as_view(), name='service_request_detail'),
    path('processors', ProcessorView.as_view(), name='processor_list'),
    path('processor/<int:pk>', ProcessorView.as_view(), name='processor_detail'),
    path('service_providers', ServiceProviderView.as_view(), name='service_provider_list'),
    path('service_provider/<int:pk>', ServiceProviderView.as_view(), name='service_provider_detail'),
    path('qrcode/<int:pk>', QRCodeView.as_view(), name='qrcode'),
]
