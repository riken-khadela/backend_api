# Generated by Django 4.2.10 on 2024-02-29 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_remove_customuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchedhistory',
            name='platform',
            field=models.CharField(choices=[('Instagram', 'Instagram'), ('Youtube', 'Youtube'), ('Youtube1', 'Youtube1')], max_length=25),
        ),
    ]
