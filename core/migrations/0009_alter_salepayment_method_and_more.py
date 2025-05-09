# Generated by Django 4.2.5 on 2025-04-20 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_salepayment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="salepayment",
            name="method",
            field=models.CharField(
                choices=[
                    ("DEBIT_CARD", "Debit Card"),
                    ("CREDIT_CARD", "Credit Card"),
                    ("NETBANKING", "Net Banking"),
                    ("WALLETS_GOOGLE", "Wallet - Google Pay"),
                    ("WALLETS_AMAZON", "Wallet - Amazon Pay"),
                    ("WALLETS_OLA", "Wallet - Ola Money"),
                    ("GIFT_VOUCHER", "Gift Voucher"),
                ],
                max_length=50,
                verbose_name="Payment Method",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="transaction_type",
            field=models.CharField(
                choices=[("SELL", "Sell to Platform"), ("BUY", "Buy from Platform")],
                default="SELL",
                max_length=4,
            ),
        ),
        migrations.CreateModel(
            name="PaymentMethod",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "method",
                    models.CharField(
                        choices=[
                            ("UPI", "UPI"),
                            ("DEBIT_CARD", "Debit Card"),
                            ("CREDIT_CARD", "Credit Card"),
                            ("NETBANKING", "Net Banking"),
                        ],
                        max_length=50,
                        verbose_name="Payment Mode",
                    ),
                ),
                ("upi_id", models.CharField(blank=True, max_length=50, null=True)),
                ("card_number", models.CharField(blank=True, max_length=16, null=True)),
                (
                    "card_holder_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("expiry_date", models.CharField(blank=True, max_length=5, null=True)),
                (
                    "account_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("bank_name", models.CharField(blank=True, max_length=100, null=True)),
                ("ifsc_code", models.CharField(blank=True, max_length=20, null=True)),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment_methods",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
