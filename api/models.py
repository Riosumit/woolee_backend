from django.db import models
from django.contrib.auth.models import User

class Producer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models. CharField(max_length=100)
    sheep_count = models.PositiveIntegerField()
    
    def __str__(self):
        return self.farm_name

# class WoolBatch(models.Model):
#     producer = models.ForeignKey(WoolProducer, on_delete=models.CASCADE)
#     qr_code = models.CharField(max_length=50, unique=True)
#     production_date = models.DateField()
#     transport_status = models.CharField(max_length=50, default='In Farm')
    
#     def __str__(self):
#         return f"{self.qr_code} - {self.producer.farm_name}"

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

# class WoolProcessingService(models.Model):
#     service_name = models.CharField(max_length=100)
#     service_type = models.CharField(max_length=50)
    
#     def __str__(self):
#         return self.service_name

# class WoolTransaction(models.Model):
#     batch = models.ForeignKey(WoolBatch, on_delete=models.CASCADE)
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE)
#     transaction_date = models.DateTimeField(auto_now_add=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
    
#     def __str__(self):
#         return f"{self.batch.qr_code} - {self.buyer.username}"
