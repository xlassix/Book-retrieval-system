from django.contrib.auth.base_user import BaseUserManager
import django
from django.db.models import Q

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,username, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,username=str.strip(username), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email,username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password,username, **extra_fields)
    def create_staff(self, email,username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password,username, **extra_fields)
    def create_superuser(self, email, password, username, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password,username, **extra_fields)
def update_user(self,username,data):
    Model=self.model()
    try:
        obj = Model.objects.get(Q(username__iexact=username))
        print(obj)
        for i,j in data.items():
            print(i,j)
        #obj.field = new_value
        #obj.save()
    except Model.DoesNotExist:
        raise ValueError("nice try")