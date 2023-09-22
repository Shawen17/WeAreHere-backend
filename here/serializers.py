from djoser.serializers import UserCreateSerializer,UserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ServiceCharge,RealEstate,User,Appointment,Transaction,RealEstateBooking

# User=get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    document = serializers.FileField()
    
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields= ('id','first_name','last_name','email','state','password','phone_number','business_name','business_address','service','client_status')


class UserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User



class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields=('id','service','address','date_booked','service_date')


class RealEstateSerializer(serializers.ModelSerializer):
    agent=serializers.CharField(source='agent.email',read_only=True)
    class Meta:
        model = RealEstate
        fields=('id','agent','description','facility','price','image1','image2','image3','image4','image5','image6','videofile','details','location','state','category','already_sold')


class RealEstateBookingSerializer(serializers.ModelSerializer):
    agent=serializers.CharField(source='agent.email')
    class Meta:
        model= RealEstateBooking
        fields=('id','agent','customer_email','schedule_date','customer_phone','apartment','location','state','is_meeting_scheduled','agreement_made')