# Generated by Django 5.0 on 2024-01-22 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_customuser_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]