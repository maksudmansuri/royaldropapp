# Generated by Django 4.0.2 on 2022-05-01 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0025_product_discount_percentage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]
