# Generated by Django 5.1.1 on 2024-09-07 15:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('phone_number', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('days_of_growth', models.IntegerField()),
                ('sale_price', models.IntegerField(default=55)),
                ('cost_price', models.IntegerField()),
                ('seeds_amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=128)),
                ('year', models.IntegerField()),
                ('consumption', models.FloatField()),
                ('price', models.IntegerField()),
                ('users', models.ManyToManyField(related_name='cars', to='garden_app.driver')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='garden_app.driver')),
            ],
        ),
        migrations.CreateModel(
            name='DriverCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden_app.car')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden_app.driver')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden_app.region')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=128)),
                ('distance', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to='garden_app.region')),
            ],
        ),
    ]
