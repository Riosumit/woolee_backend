from rest_framework import serializers
from .models import Producer, Collector, Processor, Shearer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'username']

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'user', 'farm_name', 'phone', 'pincode', 'district', 'state', 'sheep_count']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        producer = Producer.objects.create(user=user, **validated_data)
        return producer

class CollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collector
        fields = ['id', 'user', 'district', 'state']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        collector = Collector.objects.create(user=user, **validated_data)
        return collector
    
class ShearerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shearer
        fields = ['id', 'user', 'shearing_company', 'phone', 'pincode', 'district', 'state', 'experience_years']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        shearer = Shearer.objects.create(user=user, **validated_data)
        return shearer

# class ProducerProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = Producer
#         fields = ['id', 'user', 'farm_name', 'phone', 'pincode', 'district', 'state', 'sheep_count']
#         read_only_fields = ['user']

# class ProcessorProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = Producer
#         fields = ['id', 'user', 'farm_name', 'phone', 'pincode', 'district', 'state', 'sheep_count']
#         read_only_fields = ['user']

# class ServiceRequestSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = ServiceRequest
#         fields = ['id', 'service', 'batch', 'processing_details', 'processed_quantity', 'producer_delivery_address', 'producer_delivery_date', 'status', 'created_at']
#         read_only_fields = ['user']

#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         service_request = ServiceRequest.objects.create(user=user, **validated_data)
#         return service_request

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
    
# class ServiceSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Service
#         fields = ['id', 'service', 'price']
#         read_only_fields = ['user']

#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         service_provider = Service.objects.create(user=user, **validated_data)
#         return service_provider

# class ServiceDetailSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model = Service
#         fields = ['id', 'user', 'service', 'price']
#         read_only_fields = ['user']
    
# class BatchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Batch
#         fields = '__all__'
#         read_only_fields = ['qr_code', 'user']

#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         batch = Batch.objects.create(user=user, **validated_data)
#         return batch
#         # return Batch.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.type = validated_data.get('type', instance.type)
#         instance.production_date = validated_data.get('production_date', instance.production_date)
#         instance.current_location = validated_data.get('current_location', instance.current_location)
#         instance.thickness = validated_data.get('thickness', instance.thickness)
#         instance.color = validated_data.get('color', instance.color)
#         instance.softness = validated_data.get('softness', instance.softness)
#         instance.save()
#         return instance
    
# class StoreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Store
#         fields = ['id', 'user', 'batch', 'price', 'quantity_available']
#         read_only_fields = ['quantity_available', 'user']

#     def create(self, validated_data):
#         batch = validated_data['batch']
#         price = validated_data['price']
#         request = self.context.get('request')
#         user = request.user
#         quantity_available = batch.quantity

#         store_data = {
#             'user': user,
#             'batch': batch,
#             'price': price,
#             'quantity_available': quantity_available,
#         }

#         store = Store.objects.create(**store_data)
#         return store
    
#     def update(self, instance, validated_data):
#         request_data = self.context['request'].data
#         new_quantity_available = request_data.get('quantity', instance.quantity_available)
#         instance.quantity_available = new_quantity_available
#         instance.price = validated_data.get('price', instance.price)
#         instance.save()
#         return instance
    
# class StoreDetailSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     batch = BatchSerializer()
#     class Meta:
#         model = Store
#         fields = ['id', 'user', 'batch', 'price', 'quantity_available']
#         read_only_fields = ['quantity_available', 'user']

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
#         read_only_fields = ['customer', 'order_id', 'total_price']

#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         store = get_object_or_404(Store, id=validated_data["store"].id)
#         quantity_available = store.quantity_available
#         quantity = validated_data.get("quantity", 0)
        
#         if quantity > quantity_available:
#             raise serializers.ValidationError("Available quantity is not enough")
#         new_quantity = quantity_available - quantity
#         request.data['quantity'] = new_quantity
#         serializer = StoreSerializer(store, data={'quantity_available': new_quantity}, partial=True, context={'request': request})
        
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             raise serializers.ValidationError(serializer.errors)

#         total_price = store.price * quantity
#         order = Order.objects.create(customer=user, total_price=total_price, **validated_data)
#         return order

#     def update(self, instance, validated_data):
#         instance.quantity = validated_data.get('quantity', instance.quantity)
#         instance.total_price = validated_data.get('total_price', instance.total_price)
#         instance.order_id = validated_data.get('order_id', instance.order_id)
#         instance.address = validated_data.get('address', instance.address)
#         instance.pincode = validated_data.get('pincode', instance.pincode)
#         instance.location = validated_data.get('location', instance.location)
#         instance.ref = validated_data.get('lref', instance.ref)
#         instance.save()
#         return instance
    
# class OrderDetailSerializer(serializers.ModelSerializer):
#     customer = UserSerializer(read_only=True)
#     store = StoreDetailSerializer(read_only=True)
#     class Meta:
#         model = Order
#         fields = ['id', 'customer', 'store', 'quantity', 'total_price', 'order_id', 'address', 'pincode', 'location', 'ref']
#         read_only_fields = ['customer', 'order_id', 'total_price']