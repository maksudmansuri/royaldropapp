# Generated by Django 3.2 on 2021-05-21 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0006_alter_product_added_by_merchant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_desc',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_l_desc',
            field=models.TextField(),
        ),
    ]
