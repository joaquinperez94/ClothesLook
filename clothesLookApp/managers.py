from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, nickName, password=None):
        if nickName is None:
            raise TypeError('Users must have an nickName')
        user = self.model(nickName=nickName)
        user.set_password(password)
        user.save()

        return user


    def create_superuser(self, nickName, password):
        user = self.create_user(nickName, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user