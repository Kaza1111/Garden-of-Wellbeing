# Generated by Django 5.1.1 on 2024-10-04 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden_app', '0026_alter_productcost_total_product_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcost',
            name='total_product_cost',
            field=models.FloatField(default=0),
        ),
    ]
