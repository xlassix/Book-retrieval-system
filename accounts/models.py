from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = models.CharField('username', max_length=30,unique=True,error_messages={'unique':"This matric has already been registered."})
    #username = models.CharField('username', max_length=30)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('active', default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username",'first_name','last_name',"avatar"]
    class Meta:
        managed=True
        db_table = 'Users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('-date_joined', )

    def get_full_name(self):
        full_name = '%s %s' % (str.title(self.first_name),str.title(self.last_name))
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def update_user(self):
        """
        update User info
        """
        print(extra_fields,password)
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,username=str.strip(username), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)