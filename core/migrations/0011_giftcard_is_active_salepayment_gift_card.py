# Generated by Django 4.2.5 on 2025-04-20 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_alter_paymentmethod_method"),
    ]

    operations = [
        migrations.AddField(
            model_name="giftcard",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="salepayment",
            name="gift_card",
            field=models.ForeignKey(
                default=9,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.giftcard",
            ),
            preserve_default=False,
        ),
    ]
