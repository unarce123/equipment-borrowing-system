from .models import UserProfile

def is_admin(user):
    return user.is_authenticated and user.is_superuser


def is_staff(user):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return (
        hasattr(user, 'userprofile') and
        user.userprofile.role == 'staff'
    )