# Generated by Django 3.2.4 on 2021-07-24 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0007_rename_hsn_nunber_productgst_hsn_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdiscount',
            name='end_date',
            field=models.DateField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='productdiscount',
            name='start_date',
            field=models.DateField(default='', null=True),
        ),
    ]
