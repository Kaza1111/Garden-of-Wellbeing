# Generated by Django 5.1.1 on 2024-09-17 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden_app', '0016_remove_productcost_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='preparing_time',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='DeliveryCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuel_price', models.IntegerField(default=32)),
                ('date', models.DateField(auto_now=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden_app.car')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden_app.region')),
            ],
        ),
        migrations.DeleteModel(
            name='DriverCar',
        ),
    ]
