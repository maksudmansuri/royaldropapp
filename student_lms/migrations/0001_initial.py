# Generated by Django 3.2 on 2021-05-08 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('front', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_date', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='front.product')),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('discount', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('percentage', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('expired_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='paytm_payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('CURRENCY', models.CharField(max_length=50)),
                ('GATEWAYNAME', models.CharField(max_length=500)),
                ('RESPMSG', models.CharField(max_length=1000)),
                ('BANKNAME', models.CharField(max_length=150)),
                ('PAYMENTMODE', models.CharField(max_length=150)),
                ('RESPCODE', models.CharField(max_length=150)),
                ('TXNID', models.CharField(max_length=500)),
                ('TXNAMOUNT', models.CharField(max_length=150)),
                ('ORDERID', models.CharField(max_length=150)),
                ('STATUS', models.CharField(max_length=500)),
                ('BANKTXNID', models.CharField(max_length=500)),
                ('TXNDATE', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Ratting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ratting', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.product')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customers')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('orders_date', models.DateTimeField(auto_now_add=True)),
                ('student_phone', models.CharField(default=0, max_length=50, null=True)),
                ('student_email', models.EmailField(default='', max_length=254, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='front.product')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customers')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customers')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=255)),
                ('leave_message', models.TextField()),
                ('leave_status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customers')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customers')),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('attendance_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_lms.attendance')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.customers')),
            ],
        ),
    ]
