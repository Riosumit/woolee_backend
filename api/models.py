from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import uuid
import base64
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
    
class Collector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district = models.CharField(max_length=100)
    state = models. CharField(max_length=100)
    
    def __str__(self):
        return self.district
    
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
    
class Shearer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shearing_company = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()

    def __str__(self):
        return self.shearing_company
    
class ShearingRequest(models.Model):
    producer = models.ForeignKey(User, on_delete=models.CASCADE)
    shearer = models.ForeignKey(Shearer, on_delete=models.CASCADE)
    producer_address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producer.username} - Shearing Request"
    
class Batch(models.Model):
    producers = models.ManyToManyField(Producer)
    type = models.CharField(max_length=100, default="raw wool")
    quantity = models.PositiveIntegerField(default=0)
    qr_code = models.CharField(max_length=50, unique=True, blank=True, null=True)

    # Quality parameters
    thickness = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=50)
    softness = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = str(uuid.uuid4().hex)[:12].upper()

        super().save(*args, **kwargs)

    def __str__(self):
        producer_names = ', '.join([producer.farm_name for producer in self.producers.all()])
        return f"{self.qr_code} - {producer_names}"
    
# class Case(models.Model):
#     producer = models.ListForeignKey(Producer, on_delete=models.CASCADE)
#     shearer = models.ForeignKey(Shearer, on_delete=models.CASCADE, blank=True, null=True)
#     collector = models.ForeignKey(Collector, on_delete=models.CASCADE, blank=True, null=True)
#     processor = models.ForeignKey(Processor, on_delete=models.CASCADE, blank=True, null=True)
#     batch = models.ForeignKey(Batch, on_delete=models.CASCADE, blank=True, null=True)
#     description = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     parent_case = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='child_cases')

    # def __str__(self):
    #     return f"Case #{self.id}: {self.description}"
    
# class Batch(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_from = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='created_batches')
#     type = models.CharField(max_length=100, default="raw wool")
#     quantity = models.PositiveIntegerField(default=0)
#     qr_code = models.CharField(max_length=50, unique=True)
#     production_date = models.DateField(auto_now_add=True)
#     current_location = models.CharField(max_length=50, default='In Farm')

#     # Quality parameters
#     thickness = models.DecimalField(max_digits=5, decimal_places=2)
#     color = models.CharField(max_length=50)
#     softness = models.CharField(max_length=50)

#     def save(self, *args, **kwargs):
#         if not self.qr_code:
#             self.qr_code = str(uuid.uuid4().hex)[:12].upper()
#             self.qr_code = base64.b64encode(self.qr_code.encode()).decode('utf-8')

#         super().save(*args, **kwargs)

# class Service(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service = models.CharField(max_length=100)
#     price = models.PositiveIntegerField()

# class ServiceRequest(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
#     processing_details = models.TextField(blank=True, null=True)
#     processed_quantity = models.PositiveIntegerField(blank=True, null=True)
#     producer_delivery_address = models.TextField(blank=True, null=True)
#     producer_delivery_date = models.DateField(blank=True, null=True)
#     status = models.CharField(max_length=100, default="pending")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.producer.username} - {self.service} Request"

# # class Shop(models.Model):
# #     owner = models.OneToOneField(User, on_delete=models.CASCADE)
# #     name = models.CharField(max_length=255)
# #     account_holder_name = models.CharField(max_length=255)
# #     account_number = models.CharField(max_length=20)
# #     bank_name = models.CharField(max_length=255)
# #     branch_name = models.CharField(max_length=255)
# #     ifsc_code = models.CharField(max_length=20)

# #     def __str__(self):
# #         return self.name   


# class Store(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     batch = models.OneToOneField(Batch, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=12, decimal_places=2)
#     quantity_available = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f"{self.batch} - Price: {self.price} - Quantity Available: {self.quantity_available}"

# class Order(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     store = models.ForeignKey(Store, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     order_id = models.CharField(max_length=50, unique=True)
#     address = models.CharField(max_length=255)
#     pincode = models.CharField(max_length=10)
#     location = models.CharField(max_length=200, default="In Farm")
#     ref = models.CharField(max_length=100)

#     def save(self, *args, **kwargs):
#         if not self.order_id:
#             self.order_id = str(uuid.uuid4().hex)[:12].upper()
#             self.order_id = base64.b64encode(self.order_id.encode()).decode('utf-8')

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Order {self.order_id} for {self.customer.username}"

# # class WoolQuality(models.Model):
# #     batch = models.OneToOneField(WoolBatch, on_delete=models.CASCADE)
# #     grade = models.CharField(max_length=20)
# #     certification_date = models.DateField()
    
# #     def __str__(self):
# #         return f"{self.batch.qr_code} - {self.grade}"

# # class WoolStorage(models.Model):
# #     producer = models.OneToOneField(WoolProducer, on_delete=models.CASCADE)
# #     inventory_count = models.PositiveIntegerField()
    
# #     def __str__(self):
# #         return f"{self.producer.farm_name} - Storage"

# # class WoolTransaction(models.Model):
# #     batch = models.ForeignKey(WoolBatch, on_delete=models.CASCADE)
# #     buyer = models.ForeignKey(User, on_delete=models.CASCADE)
# #     transaction_date = models.DateTimeField(auto_now_add=True)
# #     price = models.DecimalField(max_digits=10, decimal_places=2)
    
# #     def __str__(self):
# #         return f"{self.batch.qr_code} - {self.buyer.username}"
