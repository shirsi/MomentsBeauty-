# Generated by Django 3.0.5 on 2020-04-10 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_orderproduct_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='products',
            new_name='product',
        ),
    ]