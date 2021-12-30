# Generated by Django 4.0 on 2021-12-30 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('front', '0010_alter_product_product_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_cart_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_rate', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_type', models.CharField(choices=[('Amount', 'amount'), ('Rate', 'rate')], default='rate', max_length=6)),
                ('discount_rate', models.IntegerField(blank=True, null=True)),
                ('discount_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('min_purchased_items', models.IntegerField()),
                ('apply_to', models.CharField(choices=[('Product', 'product'), ('Category', 'category'), ('SubCategory', 'subcategory'), ('ChildSubCategory', 'childsubcategory')], default='product', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('target_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='front.productcategory')),
                ('target_childsubcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='front.productchildsubcategory')),
                ('target_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='front.product')),
                ('target_subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='front.productsubcategory')),
            ],
        ),
    ]