# Generated by Django 3.2 on 2021-05-17 03:21

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(blank=True, default='', max_length=255, null=True, unique=True)),
                ('product_mrp', models.IntegerField(blank=True, null=True)),
                ('product_selling_price', models.IntegerField(blank=True, null=True)),
                ('product_brand', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('product_model_number', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('product_weight', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('product_desc', ckeditor_uploader.fields.RichTextUploadingField()),
                ('product_l_desc', ckeditor_uploader.fields.RichTextUploadingField()),
                ('product_slug', models.CharField(blank=True, default='', max_length=255, null=True, unique=True)),
                ('is_active', models.IntegerField(default=1)),
                ('in_stock_total', models.IntegerField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('added_by_merchant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Modules',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('module', models.CharField(blank=True, max_length=500, null=True)),
                ('module_desc', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('position', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.product')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Product_Session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_name', models.CharField(blank=True, default='', max_length=2150, null=True)),
                ('session_desc', models.TextField(blank=True, default='', null=True)),
                ('is_appiled', models.BooleanField(blank=True, default=False, null=True)),
                ('is_verified', models.BooleanField(blank=True, default=False, null=True)),
                ('session_duration', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('product_in_pdf', models.FileField(blank=True, default='', null=True, upload_to='Product_Session/Docs')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('video_link', models.FileField(blank=True, default='', max_length=2000, null=True, upload_to='instructor/module/session', verbose_name='')),
                ('product_slug', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('position', models.IntegerField(default=0)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.product_modules')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250, unique=True)),
                ('slug', models.CharField(default='', max_length=255)),
                ('thumbnail', models.FileField(blank=True, null=True, upload_to='')),
                ('description', models.TextField(default='')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ProductReviews',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.IntegerField(default=1)),
                ('ratting', models.CharField(default='5', max_length=255)),
                ('reviews', models.TextField(blank=True, default='', null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.product')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='front.productreviews')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='ProductVarient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='viewed',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product', models.CharField(blank=True, max_length=50, null=True)),
                ('module_position', models.CharField(blank=True, max_length=50, null=True)),
                ('session_position', models.CharField(blank=True, max_length=50, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customers')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariantItems',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.product')),
                ('product_varient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.productvarient')),
            ],
        ),
        migrations.CreateModel(
            name='ProductTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('transation_product_count', models.IntegerField(default=1)),
                ('transation_type', models.CharField(choices=[(1, 'BUY'), (2, 'SELL')], default='', max_length=255)),
                ('transation_desc', models.CharField(default='', max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSubCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subcategory', models.CharField(max_length=255, unique=True)),
                ('thumbnail', models.FileField(default='', upload_to='')),
                ('slug', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.IntegerField(default=1)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.productcategory')),
            ],
        ),
        migrations.CreateModel(
            name='ProductReviewVoting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reviws_images', models.FileField(default='', upload_to='')),
                ('is_active', models.IntegerField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.productreviews')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='productMedia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('media_type', models.CharField(default='', max_length=255)),
                ('media_content', models.FileField(choices=[(1, 'Image'), (2, 'Video')], default='', upload_to='')),
                ('is_active', models.IntegerField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductComments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='front.productcomments')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.product_session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.productsubcategory'),
        ),
        migrations.CreateModel(
            name='OderDeliveryStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='', max_length=255)),
                ('status_msg', models.CharField(default='', max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.product')),
            ],
        ),
        migrations.CreateModel(
            name='CustomersOrders',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_price', models.CharField(default='', max_length=255)),
                ('coupon_Code', models.CharField(default='', max_length=255)),
                ('discount_amt', models.CharField(default='', max_length=255)),
                ('product_status', models.CharField(default='', max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='front.product')),
            ],
        ),
    ]
