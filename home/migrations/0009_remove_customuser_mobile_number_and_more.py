# Generated by Django 4.2.7 on 2023-12-04 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_rename_name_customuser_city_customuser_mobile_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='Mobile_number',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='city',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='gender',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
