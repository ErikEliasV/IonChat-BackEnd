from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, verbose_name="Primeiro Nome")
    last_name = models.CharField(max_length=30, verbose_name="Segundo Nome")
    email = models.EmailField(unique=True, verbose_name="Email")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now, verbose_name="Última vez online")
    last_login_time = models.DateTimeField(null=True, blank=True, verbose_name="Último login")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_time_offline(self):
        if self.is_online:
            return "Online"
        now = timezone.now()
        time_diff = now - self.last_seen
        total_seconds = int(time_diff.total_seconds())
        if total_seconds < 60:
            return f"{total_seconds} segundos"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            return f"{minutes} minuto{'s' if minutes != 1 else ''}"
        elif total_seconds < 86400:
            hours = total_seconds // 3600
            return f"{hours} hora{'s' if hours != 1 else ''}"
        else:
            days = total_seconds // 86400
            return f"{days} dia{'s' if days != 1 else ''}"
    
    def set_online(self):
        self.is_online = True
        self.last_seen = timezone.now()
        self.last_login_time = timezone.now()
        self.save(update_fields=['is_online', 'last_seen', 'last_login_time'])
    
    def set_offline(self):
        self.is_online = False
        self.last_seen = timezone.now()
        self.save(update_fields=['is_online', 'last_seen'])