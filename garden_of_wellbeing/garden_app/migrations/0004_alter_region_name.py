# Generated by Django 5.1.1 on 2024-09-08 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden_app', '0003_remove_driver_first_name_remove_driver_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(choices=[('Šumava', 'Šumava'), ('Českobudějovicko', 'Českobudějovicko'), ('Strakonicko', 'Strakonicko'), ('Krumlovsko', 'Krumlovsko'), ('Třeboňsko', 'Třeboňsko'), ('Lipensko', 'Lipensko')], max_length=128),
        ),
    ]
