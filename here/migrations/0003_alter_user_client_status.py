# Generated by Django 4.2.4 on 2023-09-06 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('here', '0002_realestate_category_realestate_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='client_status',
            field=models.CharField(choices=[('on', 'on'), ('off', 'off')], default='off', max_length=20),
        ),
    ]
