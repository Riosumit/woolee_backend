from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from enum import Enum

class Producer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=100)
    phone = PhoneNumberField(blank=True, null=True)
    pincode = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100)
    state = models. CharField(max_length=100)
    sheep_count = models.PositiveIntegerField()
    
    def __str__(self):
        return self.farm_name
    
class Processor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    factory_name = models.CharField(max_length=100)
    phone = PhoneNumberField(blank=True, null=True)
    pincode = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100)
    state = models. CharField(max_length=100)
    labour_count = models.PositiveIntegerField()
    
    def __str__(self):
        return self.factory_name
    
class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    available_services = models.CharField(max_length=100)
    service_prices = models.JSONField()

class ServiceRequest(models.Model):
    producer = models.ForeignKey(User, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    processing_details = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    producer_delivery_address = models.TextField(blank=True, null=True)
    producer_delivery_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producer.username} - {', '.join([tag.value for tag in self.service_types.all()])} Request"

# class Shop(models.Model):
#     owner = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     account_holder_name = models.CharField(max_length=255)
#     account_number = models.CharField(max_length=20)
#     bank_name = models.CharField(max_length=255)
#     branch_name = models.CharField(max_length=255)
#     ifsc_code = models.CharField(max_length=20)

#     def __str__(self):
#         return self.name   

class Batch(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, default="raw wool")
    quantity = models.PositiveIntegerField(default=0)
    qr_code = models.CharField(max_length=50, unique=True)
    production_date = models.DateField()
    current_location = models.CharField(max_length=50, default='In Farm')

    # Quality parameters
    thickness = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=50)
    softness = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = str(uuid.uuid4().hex)[:12].upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.qr_code} - {self.producer.farm_name}"
    
class Store(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    batch = models.OneToOneField(Batch, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.batch} - Price: {self.price} - Quantity Available: {self.quantity_available}"


# class WoolQuality(models.Model):
#     batch = models.OneToOneField(WoolBatch, on_delete=models.CASCADE)
#     grade = models.CharField(max_length=20)
#     certification_date = models.DateField()
    
#     def __str__(self):
#         return f"{self.batch.qr_code} - {self.grade}"

# class WoolStorage(models.Model):
#     producer = models.OneToOneField(WoolProducer, on_delete=models.CASCADE)
#     inventory_count = models.PositiveIntegerField()
    
#     def __str__(self):
#         return f"{self.producer.farm_name} - Storage"

# class WoolTransaction(models.Model):
#     batch = models.ForeignKey(WoolBatch, on_delete=models.CASCADE)
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE)
#     transaction_date = models.DateTimeField(auto_now_add=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
    
#     def __str__(self):
#         return f"{self.batch.qr_code} - {self.buyer.username}"
