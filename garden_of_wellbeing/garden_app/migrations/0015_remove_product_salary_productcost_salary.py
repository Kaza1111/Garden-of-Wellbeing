# Generated by Django 5.1.1 on 2024-09-16 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden_app', '0014_remove_driver_salary_product_salary_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='salary',
        ),
        migrations.AddField(
            model_name='productcost',
            name='salary',
            field=models.IntegerField(default=250),
        ),
    ]
