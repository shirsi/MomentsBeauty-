# Generated by Django 3.0.5 on 2020-04-10 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
