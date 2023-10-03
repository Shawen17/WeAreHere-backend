from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .managers import UserManager,MultiImageField
from django.contrib.postgres.fields import JSONField 
from datetime import datetime,timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets
from django.utils import timezone


services=(
    ('',''),
    ('painting','painting'),
    ('upholstery','upholstery'),
    ('interior decoration','interior decoration'),
    ('cleaning services','cleaning services'),
    ('evacuation services','evacuation services'),
    ('tiling service','tiling service'),
    ('estate management', 'estate management'),
    ('real estate','real estate'),
    ('construction','construction'),
    ('event planning','event planning'),
    ('plumbing service','plumbing service'),
)

states=(
    ('',''),
    ('Lagos','Lagos'),
    ('Ogun','Ogun'),
)

status=(
    
    ('on','on'),
    ('off','off'),
)
# Create your models here.
class User(AbstractUser):
    username= None
    email=models.EmailField(_('email address'),unique=True)
    state=models.CharField(max_length=50,default='Lagos')
    phone_number=models.IntegerField(default=int('08000000000'))
    subscription_end_date=models.DateTimeField(default=timezone.now)
    business_name=models.CharField(max_length=50,null=True,blank=True)
    business_address=models.TextField(null=True,blank=True)
    document=models.FileField(upload_to='here/files',null=True,blank=True)
    client_status = models.CharField(max_length=20,choices=status,default='off')
    service=models.CharField(max_length=50,blank=True,default='',choices=services)
    is_service_provider=models.BooleanField(default=False)
    
    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','state','phone_number','password','business_name','business_address','service','document','client_status']

    class Meta:
        verbose_name=_('user')
        verbose_name_plural=_('users')

    def __str__(self):
        return self.email


    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

        


   


class ServiceCharge(models.Model):
    service=models.CharField(max_length=50,blank=True,default='',choices=services)
    state=models.CharField(max_length=50,blank=True,default='',choices=states)
    city=models.CharField(max_length=244,blank=True,null=True)
    charge=models.IntegerField()

    def __str__(self):
        return self.service


class RealEstateImage(models.Model):
    # description = models.OneToOneField(RealEstate,on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='here/images',blank=True, null=True)
    image2 = models.ImageField(upload_to='here/images',blank=True, null=True)
    image3 = models.ImageField(upload_to='here/images',blank=True, null=True)
    image4 = models.ImageField(upload_to='here/images',blank=True, null=True)
    image5 = models.ImageField(upload_to='here/images',blank=True, null=True)
    image6 = models.ImageField(upload_to='here/images',blank=True, null=True)

    def __str__(self):
        return self.description.description


class RealEstate(models.Model):
    agent=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    description=models.CharField(max_length=70,null=True,blank=True)
    facility=models.JSONField(default=dict,null=True)
    price=models.IntegerField()
    image1 = models.ImageField(upload_to='here/images',blank=True, null=True)
    image2 = models.ImageField(upload_to='here/images',blank=True, null=True)
    image3 = models.ImageField(upload_to='here/images',blank=True, null=True)
    image4 = models.ImageField(upload_to='here/images',blank=True, null=True)
    image5 = models.ImageField(upload_to='here/images',blank=True, null=True)
    image6 = models.ImageField(upload_to='here/images',blank=True, null=True)
    videofile=models.FileField(upload_to='here/videos',blank=True, null=True)
    details=models.TextField()
    location=models.TextField()
    date=models.DateTimeField(default=timezone.now)
    category=models.CharField(max_length=50)
    state=models.CharField(max_length=50,blank=True)
    already_sold=models.BooleanField(default=False)

    class Meta:
        unique_together = ["agent", "description",'location']

    def __str__(self):
        return self.description



class Appointment(models.Model):
    full_name=models.CharField(max_length=100,blank=True,null=True)
    customer_email=models.EmailField(max_length=100)
    phone_number=models.CharField(max_length=30)
    service=models.CharField(max_length=60)  
    address=models.TextField()
    state=models.CharField(max_length=60)
    date_booked = models.DateTimeField(auto_now_add=True)
    service_date = models.DateField(default=timezone.now)
    is_client_called=models.BooleanField(default=False) 
   

    def __str__(self):
        return self.full_name

class Transaction(models.Model):
    appointment=models.OneToOneField(Appointment,on_delete=models.CASCADE)
    treated_by=models.CharField(max_length=100,blank=True,null=True)
    customer_specification = models.TextField(blank=True,null=True)
    has_client_committed=models.BooleanField(default=False) 
    full_payment_made=models.BooleanField(default=False) 
    partner_involved=models.CharField(max_length=100,blank=True,null=True)
    partner_quotation=models.FileField(upload_to='here/files',null=True,blank=True)
    is_completed=models.BooleanField(default=False) 
    close_deal=models.BooleanField(default=False)
    customer_invoice=models.FileField(upload_to='here/files',null=True,blank=True)
    total_bill=models.IntegerField(blank=True, null = True)


    def __str__(self):
        return self.appointment.full_name


@receiver(post_save,sender=Appointment)   
def create_transaction_profile(sender,instance,created,**kwargs):
    from django.core import serializers
    if created:
        Transaction.objects.create(appointment=instance)


class RealEstateBooking(models.Model):
    agent=models.ForeignKey(User,on_delete=models.CASCADE)
    business_name=models.CharField(max_length=100)
    customer_email=models.EmailField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    apartment= models.ForeignKey(RealEstate,on_delete=models.CASCADE,null=True, blank=True)
    location=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    is_meeting_scheduled=models.BooleanField(default=False)
    schedule_date=models.DateField(null=True,blank=True)
    agreement_made=models.BooleanField(default=False)

    def __str__(self):
        return self.customer_email


class Subscription(models.Model):
    ref = models.CharField( max_length=200,blank=True,null=True)
    made_by= models.ForeignKey(User,on_delete=models.CASCADE)
    bundle=models.CharField(max_length=50,default='basic')
    amount=models.IntegerField()
    start_date=models.DateTimeField(auto_now_add=True)
    end_date=models.DateTimeField()
    

    def __str__(self):
        return self.ref
    
    def save(self, *args, **kwargs):
        query=Subscription.objects.filter(made_by=self.made_by)
        if query.exists():
            sub=query.latest('start_date')
            self.end_date=sub.end_date + timedelta(days=30)
        else:
            self.end_date=datetime.now() + timedelta(days=30)
        while not self.ref:
            
            ref = secrets.token_urlsafe(16)
            object_with_similar_ref = Subscription.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref=ref
        super().save(*args, **kwargs)

class Charge(models.Model):
    name= models.CharField(max_length=50)
    charge= models.IntegerField()

    def __str__(self):
        return self.name


class Contactus(models.Model):
    full_name=models.CharField(max_length=100)
    email=models.EmailField()
    message=models.TextField()


    def __str__(self):
        return self.full_name