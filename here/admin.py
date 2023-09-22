from django.contrib import admin
from .models import User,ServiceCharge,RealEstate,RealEstateImage,Appointment,Transaction, RealEstateBooking
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
# from .forms import MultiImageForm

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','state')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
         (_('Business and Subscription info'), {'fields': ('is_service_provider','phone_number','service', 'business_name',
                                       'business_address', 'document','client_status','subscription_end_date')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    list_display=['email','first_name','last_name','phone_number','state','business_name','business_address','document','client_status','service','is_service_provider','subscription_end_date']
    ordering=('email',)





@admin.register(ServiceCharge)
class ServiceChargeAdmin(ModelAdmin):
    list_display= ('service','state','city','charge')


@admin.register(RealEstate)
class RealEstateAdmin(ModelAdmin):
    
    list_display=('description','agent','price','facility','image1','image2','image3','image4','image5','image6','videofile','details','location','state','already_sold','date','category')
    search_fields=('state','description','location')
    list_filter=('price','description')
    ordering=('-date',)
    actions=['mark_sold']

    def mark_sold(self,request,queryset):
        queryset.update(status=True)

    mark_sold.short_description='Mark As Sold'


@admin.register(RealEstateImage)
class RealEstateImageAdmin(ModelAdmin):
    list_display=('image1','image2','image3','image4','image5','image6')


@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display=('full_name','customer_email','phone_number','service','address','state','date_booked','service_date','is_client_called')
    actions=['mark_client_called']

    def mark_client_called(self,request,queryset):
        queryset.update(is_client_called=True)
        for i in queryset:
            trans = Transaction.objects.get(appointment=i)
            trans.treated_by=request.user.get_full_name()
            trans.save(update_fields=['treated_by'])

    mark_client_called.short_description="Mark As Called"


@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display=('appointment','treated_by','customer_specification','has_client_committed','full_payment_made','partner_involved','partner_quotation','is_completed','close_deal','customer_invoice','total_bill')


@admin.register(RealEstateBooking)
class RealEstateBookingAdmin(ModelAdmin):
    list_display=('agent','business_name','customer_email','customer_phone','apartment','location','state','is_meeting_scheduled','schedule_date','agreement_made')