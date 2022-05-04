from .models import User, Profile

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return
        try:
            user = User.objects.get(email=user.email)
            sociallogin.state['process'] = 'connect'
            perform_login(request, user, 'none')
        except User.DoesNotExist:
            pass
    def populate_user(self, request, sociallogin, data):
        user = User.objects.get(id=user.id)
        profile = Profile.objects.get(user=user.id)
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.email = data.email
        profile.photo_url = sociallogin.account.extra_data['picture']
        user.save()
        profile.save()

