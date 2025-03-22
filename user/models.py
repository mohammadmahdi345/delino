from django.utils.translation import gettext as _
from django.core import validators
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail,User
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('وارد کردن شماره تلفن الزامی است.')
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    # phone_number = models.CharField(max_length=13,unique=True)
    phone_number = models.CharField(_('mobile number'),max_length=13,unique=True,null=True, blank=True,
                                          validators=[
                                              validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                                                        ('Enter a valid mobile number.'), 'invalid'),
                                          ],
                                          error_messages={
                                              'unique': _("A user with this mobile number already exists."),
                                          }
                                          )
    email = models.EmailField(unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name','password','email']

    def __str__(self):
        return str(self.full_name)


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    res = models.ForeignKey('food.Restorant',related_name='comments',on_delete=models.CASCADE)
    description = models.TextField(max_length=250)
    created_time = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.full_name


class Gateway(models.Model):
    title = models.CharField(_('title'), max_length=120)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='pakages/')
    is_enable = models.BooleanField(_('is_enable'), default=True)
    created_time = models.DateTimeField(_('created_time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated_time'), auto_now=True)

    class Meta:
        db_table = 'gateway'
        verbose_name= _('gateway')
        verbose_name_plural = _('gateways')

    def __str__(self):
        return self.title