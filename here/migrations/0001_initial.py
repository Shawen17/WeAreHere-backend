# Generated by Django 4.2.4 on 2023-10-03 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import here.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('state', models.CharField(default='Lagos', max_length=50)),
                ('phone_number', models.IntegerField(default=8000000000)),
                ('subscription_end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('business_name', models.CharField(blank=True, max_length=50, null=True)),
                ('business_address', models.TextField(blank=True, null=True)),
                ('document', models.FileField(blank=True, null=True, upload_to='here/files')),
                ('client_status', models.CharField(choices=[('on', 'on'), ('off', 'off')], default='off', max_length=20)),
                ('service', models.CharField(blank=True, choices=[('', ''), ('painting', 'painting'), ('upholstery', 'upholstery'), ('interior decoration', 'interior decoration'), ('cleaning services', 'cleaning services'), ('evacuation services', 'evacuation services'), ('tiling service', 'tiling service'), ('estate management', 'estate management'), ('real estate', 'real estate'), ('construction', 'construction'), ('event planning', 'event planning'), ('plumbing service', 'plumbing service')], default='', max_length=50)),
                ('is_service_provider', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', here.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_email', models.EmailField(max_length=100)),
                ('phone_number', models.CharField(max_length=30)),
                ('service', models.CharField(max_length=60)),
                ('address', models.TextField()),
                ('state', models.CharField(max_length=60)),
                ('date_booked', models.DateTimeField(auto_now_add=True)),
                ('service_date', models.DateField(default=django.utils.timezone.now)),
                ('is_client_called', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('charge', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Contactus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RealEstate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=70, null=True)),
                ('facility', models.JSONField(default=dict, null=True)),
                ('price', models.IntegerField()),
                ('image1', models.ImageField(blank=True, null=True, upload_to='here/images')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='here/images')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='here/images')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='here/images')),
                ('image5', models.ImageField(blank=True, null=True, upload_to='here/images')),
                ('image6', models.ImageField(blank=True, null=True, upload_to='here/images')),
                ('videofile', models.FileField(blank=True, null=True, upload_to='here/videos')),
                ('details', models.TextField()),
                ('location', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.CharField(max_length=50)),
                ('state', models.CharField(blank=True, max_length=50)),
                ('already_sold', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('agent', 'description', 'location')},
            },
        ),
        migrations.CreateModel(
            name='RealEstateImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='here/images')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='here/images')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='here/images')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='here/images')),
                ('image5', models.ImageField(blank=True, null=True, upload_to='here/images')),
                ('image6', models.ImageField(blank=True, null=True, upload_to='here/images')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(blank=True, choices=[('', ''), ('painting', 'painting'), ('upholstery', 'upholstery'), ('interior decoration', 'interior decoration'), ('cleaning services', 'cleaning services'), ('evacuation services', 'evacuation services'), ('tiling service', 'tiling service'), ('estate management', 'estate management'), ('real estate', 'real estate'), ('construction', 'construction'), ('event planning', 'event planning'), ('plumbing service', 'plumbing service')], default='', max_length=50)),
                ('state', models.CharField(blank=True, choices=[('', ''), ('Lagos', 'Lagos'), ('Ogun', 'Ogun')], default='', max_length=50)),
                ('city', models.CharField(blank=True, max_length=244, null=True)),
                ('charge', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treated_by', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_specification', models.TextField(blank=True, null=True)),
                ('has_client_committed', models.BooleanField(default=False)),
                ('full_payment_made', models.BooleanField(default=False)),
                ('partner_involved', models.CharField(blank=True, max_length=100, null=True)),
                ('partner_quotation', models.FileField(blank=True, null=True, upload_to='here/files')),
                ('is_completed', models.BooleanField(default=False)),
                ('close_deal', models.BooleanField(default=False)),
                ('customer_invoice', models.FileField(blank=True, null=True, upload_to='here/files')),
                ('total_bill', models.IntegerField(blank=True, null=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='here.appointment')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(blank=True, max_length=200, null=True)),
                ('bundle', models.CharField(default='basic', max_length=50)),
                ('amount', models.IntegerField()),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('made_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RealEstateBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=100)),
                ('customer_email', models.EmailField(max_length=100)),
                ('customer_phone', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('is_meeting_scheduled', models.BooleanField(default=False)),
                ('schedule_date', models.DateField(blank=True, null=True)),
                ('agreement_made', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('apartment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='here.realestate')),
            ],
        ),
    ]
