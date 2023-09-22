from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import User,Appointment,Transaction,RealEstate,RealEstateBooking
from .serializers import UserCreateSerializer,AppointmentSerializer,RealEstateSerializer,RealEstateBookingSerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django import template
from django.core.mail import send_mail
from django.conf import settings
import json


class UserViewSet(UserViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_appointment(request):
    data=request.data
    user=User.objects.get(email=data['email'])
    
    if user:
        trans_data={
            'full_name':user.get_full_name(),
            'customer_email':user.email,
            'phone_number':'0'+ str(user.phone_number),
            'service':data['service'],
            'address':data['address'],
            'state':data['state'],
            'service_date':data['date']
        }
        Appointment.objects.create(**trans_data)
        
        plaintext = template.loader.get_template('here/appointment.txt')
        htmltemp = template.loader.get_template('here/appointment.html')

        c={
            'full_name':user.get_full_name(),
            'customer_email':user.email,
            'phone_number':'0'+ str(user.phone_number),
            'service':data['service'],
            'address':data['address'],
            'state':data['state'],
        }
        text_content = plaintext.render(c)
        html_content = htmltemp.render(c)
        subject = 'New Appointment Booked'  
        msg = text_content
        to = user.email
        send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])

        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def fetch_appointment(request):
    email=request.data['email']
    orders= Appointment.objects.filter(customer_email=email).order_by('-date_booked')
    order_serializer = AppointmentSerializer(orders,many=True)
    return Response({'orders':order_serializer.data})

@api_view(['POST','PUT'])
@permission_classes([IsAuthenticated])
def add_property(request):
    data = request.data
    
    updateable_field={key: value for key, value in data.items() if key != 'email' and key!='facility' }
    facility_fields = {key: value for key, value in data.items() if key == 'facility'}
    user = User.objects.get(email=data['email'])
    if request.method=='POST':
        if user:
            facility = json.loads(data['facility'])
            property_data = {
                'agent': user.id,
                'description': data['description'],
                'facility': facility,
                'category': data['category'],
                'price': data['price'],
                'image1': data['file1'],
                'image2': data['file2'],
                'image3': data['file3'],
                'image4': data['file4'],
                'image5': data['file5'],
                'image6': data['file6'],
                'videofile': data['videofile'],
                'details': data['details'],
                'location': data['location'],
                'state': data['state']
            }
            serializer = RealEstateSerializer(data=property_data)
            

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method=='PUT':
        filtered_fields = {key: value for key, value in updateable_field.items() if value != 'undefined'}
        
        prop = RealEstate.objects.filter(pk=data['id'])
        prop.update(**filtered_fields)
        
        if facility_fields:
            json_data = prop[0].facility
            facility_data=json.loads(facility_fields['facility'])
            
            for key, value in facility_data.items():
                json_data[str(key)]=str(value)
            prop.update(facility=json_data)
                
        return Response(status=status.HTTP_201_CREATED)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def get_property_admin(request):
    email=request.data['email']
    
    user=User.objects.get(email=email,is_service_provider=True,service='real estate')
    if user:
        bookings= RealEstateBooking.objects.filter(agent=user).order_by('-schedule_date')
        apart = RealEstate.objects.filter(agent=user)
        bookings_serializer=RealEstateBookingSerializer(bookings,many=True)
        apart_serializer = RealEstateSerializer(apart,many=True)
        return Response({'orders':apart_serializer.data,'bookings':bookings_serializer.data})
    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_properties(request):
    apartments = RealEstate.objects.filter(already_sold=False)
    apartments_serializer = RealEstateSerializer(apartments,many=True)
    
    return Response({'orders':apartments_serializer.data})


@api_view(['POST','PUT'])
@permission_classes([IsAuthenticated])
def realestate_booking(request):
    if request.method=='POST':
        data=request.data
        agent=User.objects.get(email=data['agent'])
        customer=User.objects.get(email=data['email'])
        if agent:
            booking_data={
                'agent':agent,
                'business_name':agent.business_name,
                'customer_email':data['email'],
                'customer_phone':'0' + str(customer.phone_number),
                'apartment':data['apartment'],
                'location':data['location'],
                'state':data['state']
                }
            serializer=RealEstateBooking.objects.create(**booking_data)
            return Response(status=status.HTTP_201_CREATED)
            
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method=='PUT':
        data=request.data
    
        if data['date']!='undefined':
            RealEstateBooking.objects.filter(pk=int(data['id'])).update(schedule_date=data['date'])
        
        if data['meeting']!= 'false':
            RealEstateBooking.objects.filter(pk=int(data['id'])).update(is_meeting_scheduled=True)
            
        if data['deal']!='false':
            RealEstateBooking.objects.filter(pk=int(data['id'])).update(agreement_made=True)
        return Response(status=status.HTTP_201_CREATED)
        


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_property(request,id):
    RealEstate.objects.get(pk=id).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_properties(request):
    data = request.GET.get('my_array', '[]')
    split_data=data.split(',')
    property_id = [int(item) for item in split_data ]
    RealEstate.objects.filter(pk__in=property_id).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_bookings(request):
    data=request.GET.get('my_array','[]')
    action=request.data
    split_data=data.split(',')
    booking_ids = [int(item) for item in split_data ]
    bookings=RealEstateBooking.objects.filter(pk__in=booking_ids)
    if action['action']=='meeting':
        bookings.update(is_meeting_scheduled=True)
    else:
        bookings.update(agreement_made=True)
    return Response(status=status.HTTP_201_CREATED)
    


    


