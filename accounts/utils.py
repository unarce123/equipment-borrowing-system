def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'admin'