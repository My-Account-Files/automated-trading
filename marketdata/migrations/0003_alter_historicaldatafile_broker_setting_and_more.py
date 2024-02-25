# Generated by Django 4.2.7 on 2024-02-25 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_brokersetting'),
        ('marketdata', '0002_alter_brokersetting_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaldatafile',
            name='broker_setting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.brokersetting'),
        ),
        migrations.AlterField(
            model_name='historicalmarketdatasetting',
            name='broker_setting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.brokersetting'),
        ),
        migrations.AlterField(
            model_name='masterinstrumentlist',
            name='broker_setting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.brokersetting'),
        ),
        migrations.DeleteModel(
            name='BrokerSetting',
        ),
    ]
