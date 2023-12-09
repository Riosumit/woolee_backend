from rest_framework import serializers
from .models import Producer, ServiceRequest, ServiceProvider, Processor
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'usernmae']

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'farm_name', 'phone', 'district', 'state', 'sheep_count']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        producer = Producer.objects.create(user=user, **validated_data)
        return producer

class ServiceRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServiceRequest
        fields = ['id', 'service_provider', 'processing_details', 'quantity', 'producer_delivery_address', 'producer_delivery_date', 'status', 'created_at']
        read_only_fields = ['producer']

    def create(self, validated_data):
        request = self.context.get('request')
        producer = request.user
        service_request = ServiceRequest.objects.create(producer=producer, **validated_data)
        return service_request

class ProcessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processor
        fields = ['id', 'factory_name', 'phone', 'district', 'state', 'labour_count']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        processor = Processor.objects.create(user=user, **validated_data)
        return processor
    
class ServiceProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceProvider
        fields = ['id', 'available_services', 'service_prices']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        service_provider = ServiceProvider.objects.create(user=user, **validated_data)
        return service_provider