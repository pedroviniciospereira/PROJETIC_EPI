from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    foto = models.ImageField(upload_to='perfil/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Sinais para criar/atualizar o perfil automaticamente quando o usuário for criado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Garante que o perfil exista antes de salvar
    UserProfile.objects.get_or_create(user=instance)
    instance.profile.save()