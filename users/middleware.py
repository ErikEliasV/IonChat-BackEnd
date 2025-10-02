from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from datetime import timedelta

User = get_user_model()


class OnlineStatusMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
            user.last_seen = timezone.now()
            user.save(update_fields=['last_seen'])
            if not user.is_online:
                user.is_online = True
                user.save(update_fields=['is_online'])
        return None


class AutoOfflineMiddleware(MiddlewareMixin):
    def process_request(self, request):
        timeout_minutes = 5
        cutoff_time = timezone.now() - timedelta(minutes=timeout_minutes)
        User.objects.filter(
            is_online=True,
            last_seen__lt=cutoff_time
        ).update(is_online=False)
        return None
