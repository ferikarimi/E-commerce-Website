from django.db import models
from Accounts.models import User

# Create your models here.
# class Customers (User):
#     # phone_number = PhoneNumberField()
#     # birth_date = models.DateField()
#     # created_at = models.DateTimeField(auto_now_add=True)
#     # updated_at = models.DateTimeField()


#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
    

class Addresses (models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"address : {self.city} : {self.address}"
    

