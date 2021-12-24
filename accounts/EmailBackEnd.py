from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import CustomUser
class EmailBackEnd(ModelBackend):
    def authenticate(self,username=None,password=None,**kwargs):
        UserModel=get_user_model()
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'phone': username}
        
        try:
            user = UserModel.objects.get(**kwargs)
            print("i m in authentication")
            print(user)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, username):
        UserModel=get_user_model()
        try:
            return UserModel.objects.get(pk=username)
        except UserModel.DoesNotExist:
            return None