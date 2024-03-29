from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from here.views import UserViewSet
from django.contrib import admin
from django.conf.urls.static import static 
from  django.conf import settings
from here import views
from django.views.static import serve


router = DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/book/', views.make_appointment, name='make_appointment' ),
    path('api/appointments/', views.fetch_appointment, name='fetch_appointment' ),
    path('api/add-property/', views.add_property, name='add_property' ),
    path('api/get-property/', views.get_property_admin, name='get_property_admin' ),
    path('api/properties/', views.get_properties, name='get_properties' ),
    path('api/realestate-booking/', views.realestate_booking, name='realestate_booking' ),
    path('api/delete-property/<int:id>/', views.delete_property, name='delete_property' ),
    path('api/delete-properties/', views.delete_properties, name='delete_properties' ),
    path('api/update-bookings/', views.update_bookings, name='update_bookings' ),
    path('api/charges/', views.get_charges, name='get_charges' ),
    path('api/contact/', views.contact_us, name='contact_us' ),
    path('api/initiate-payment/', views.initiate_subscription, name='initiate_subscription' ),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)', serve, {'document_root':settings.MEDIA_DIR})]   
urlpatterns += static(settings.AWS_LOCATION,document_root= settings.STATIC_URL)  
