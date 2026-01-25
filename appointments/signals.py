from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Patient

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    # Only create a Patient profile if a new User was just created
    if created:
        Patient.objects.create(
            user=instance, 
            name=instance.username, 
            phone="Update Phone"
        )