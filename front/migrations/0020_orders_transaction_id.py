# Generated by Django 4.0.2 on 2022-02-09 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0019_alter_product_gst_percentage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='transaction_id',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
    ]