# Generated by Django 4.2.5 on 2025-02-11 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_amount_giftcard_buy_back_price_giftcard_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcard',
            name='buy_back_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
