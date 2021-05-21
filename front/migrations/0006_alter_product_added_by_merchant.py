# Generated by Django 3.2 on 2021-05-21 04:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210517_1833'),
        ('front', '0005_remove_product_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='added_by_merchant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.merchants'),
        ),
    ]