# Generated by Django 3.0.5 on 2020-04-10 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200410_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]