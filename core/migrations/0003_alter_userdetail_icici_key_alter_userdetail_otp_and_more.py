# Generated by Django 5.0.1 on 2024-01-21 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_userdetails_userdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='icici_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='otp',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='zerodha_key',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
