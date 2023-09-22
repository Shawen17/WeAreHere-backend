from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations=True

    now = timezone.now()
    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('the given email must be set')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_staff',False)
        return self._create_user(email,password,**extra_fields)

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email,password,**extra_fields)





class MultiImageField(models.Field):
    description = _("A field that represents six ImageFields.")

    def __init__(self, *args, **kwargs):
        
        self.image1 = models.ImageField(upload_to='here/images', blank=True, null=True)
        self.image2 = models.ImageField(upload_to='here/images', blank=True, null=True)
        self.image3 = models.ImageField(upload_to='here/images', blank=True, null=True)
        self.image4 = models.ImageField(upload_to='here/images', blank=True, null=True)
        self.image5 = models.ImageField(upload_to='here/images', blank=True, null=True)
        self.image6 = models.ImageField(upload_to='here/images', blank=True, null=True)
        super().__init__(*args, **kwargs)
        

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs

    # def check(self, **kwargs):
    #     errors = super().check(**kwargs)
    #     errors.extend(self.image1.check(**kwargs))
    #     errors.extend(self.image2.check(**kwargs))
    #     errors.extend(self.image3.check(**kwargs))
    #     errors.extend(self.image4.check(**kwargs))
    #     errors.extend(self.image5.check(**kwargs))
    #     errors.extend(self.image6.check(**kwargs))
    #     return errors

    # def from_db_value(self, value, expression, connection):
    #     return self.to_python(value)

    # def get_prep_value(self, value):
    #     if value is None:
    #         return None
    #     return str(value)

    # def to_python(self, value):
    #     return value

    # def get_internal_type(self):
    #     return 'CharField'

    # def formfield(self, **kwargs):
    #     # We don't want to use the form field for this custom field.
    #     # It is better to handle file uploads separately.
    #     return None
