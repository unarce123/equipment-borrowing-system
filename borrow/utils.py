from .models import Notification


def create_notification(user, message, notif_type="system"):
    Notification.objects.create(
        user=user,
        message=message,
        notif_type=notif_type
    )