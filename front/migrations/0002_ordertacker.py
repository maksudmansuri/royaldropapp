# Generated by Django 3.2.4 on 2021-08-11 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTacker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ordes_id', models.IntegerField()),
                ('desc', models.CharField(max_length=5000)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
