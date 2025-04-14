from .models import UserProfile

def user_profile_context(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get_or_create(user=request.user)
            return {'user_profile': profile}
        except UserProfile.DoesNotExist:
            pass
    return {}
