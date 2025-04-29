from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save , sender=User)
def set_superuser_not_customer(sender , instance , created , **kwargs):
    if instance.is_superuser and instance.is_customer :
        instance.is_customer = False
        instance.save(update_fields=["is_customer"])