# adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Save additional user data from social account provider
        # print(sociallogin)
        # print(user)
        # print(form)
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            if 'picture' in extra_data:
                user.profile_image = extra_data['picture']
            if 'name' in extra_data:
                user.full_name = extra_data['name']
                
            user.is_third_party = True
            user.save()
        return user
