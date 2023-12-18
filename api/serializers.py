from rest_framework import serializers
from .models import Producer, ServiceRequest, ServiceProvider, Processor, Batch, Store, Order
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'username']

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'farm_name', 'phone', 'pincode', 'district', 'state', 'sheep_count']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        producer = Producer.objects.create(user=user, **validated_data)
        return producer

class ProducerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Producer
        fields = ['id', 'user', 'farm_name', 'phone', 'pincode', 'district', 'state', 'sheep_count']
        read_only_fields = ['user']

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
        fields = ['id', 'factory_name', 'phone', 'pincode', 'district', 'state', 'labour_count']
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
    
class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
        read_only_fields = ['qr_code', 'producer']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        producer = Producer.objects.get(user=user)
        batch = Batch.objects.create(producer=producer, **validated_data)
        return batch
        # return Batch.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.production_date = validated_data.get('production_date', instance.production_date)
        instance.current_location = validated_data.get('current_location', instance.current_location)
        instance.thickness = validated_data.get('thickness', instance.thickness)
        instance.color = validated_data.get('color', instance.color)
        instance.softness = validated_data.get('softness', instance.softness)
        instance.save()
        return instance
    
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'producer', 'batch', 'price', 'quantity_available']
        read_only_fields = ['quantity_available', 'producer']

    def create(self, validated_data):
        batch = validated_data['batch']
        price = validated_data['price']
        request = self.context.get('request')
        user = request.user
        producer = Producer.objects.get(user=user)

        # Assuming the Batch model has a 'quantity' field
        quantity_available = batch.quantity  # Adjust this based on your Batch model

        store_data = {
            'producer': producer,
            'batch': batch,
            'price': price,
            'quantity_available': quantity_available,
        }

        store = Store.objects.create(**store_data)
        return store
    
class StoreDetailSerializer(serializers.ModelSerializer):
    producer = ProducerSerializer()
    batch = BatchSerializer()
    class Meta:
        model = Store
        fields = ['id', 'producer', 'batch', 'price', 'quantity_available']
        read_only_fields = ['quantity_available', 'producer']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('__all__')
        read_only_fields = ['customer', 'order_id', 'total_price']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        total_price=validated_data["store"].price*validated_data["quantity"]
        order = Order.objects.create(customer=user, total_price=total_price, **validated_data)
        return order

    def update(self, instance, validated_data):
        # instance.customer = validated_data.get('customer', instance.customer)
        # instance.store = validated_data.get('store', instance.store)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.order_id = validated_data.get('order_id', instance.order_id)
        instance.address = validated_data.get('address', instance.address)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.location = validated_data.get('location', instance.location)
        instance.ref = validated_data.get('lref', instance.ref)
        instance.save()
        return instance