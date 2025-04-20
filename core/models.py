from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=150, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    contact = models.CharField(
        max_length=15,
        verbose_name="Contact Number",
        null=True,
        blank=True,
        validators=[RegexValidator(r'^\d{10,15}$', 'Enter a valid phone number (10-15 digits).')],
    )

    # Override username field to email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'contact']

    def __str__(self):
        return self.email


class GiftCard(models.Model):
    BRAND_CHOICES = [
        ('Amazon', 'Amazon'),
        ('Flipkart', 'Flipkart'),
        ('Myntra', 'Myntra'),
        ('Walmart', 'Walmart'),
        ('Target', 'Target'),
        ('eBay', 'eBay'),
        ('Starbucks', 'Starbucks'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='giftcards')
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, verbose_name="Gift Card Brand")
    background_image = models.ImageField(upload_to='static/images/giftcards/', blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    buy_back_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)

    def get_default_image(self):
        """Return the default image path for the selected brand."""
        return f"/static/images/giftcards/{self.brand.lower()}.png"

    def get_image_url(self):
        """Return the uploaded image or default brand image."""
        return self.background_image.url if self.background_image else self.get_default_image()
    
    def __str__(self):
        return f"{self.brand} Gift Card - ${self.value}"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('SELL', 'Sell to Platform'),
        ('BUY', 'Buy from Platform'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE_CHOICES, default='SELL')
    card_number = models.CharField(max_length=16)
    card_holder = models.CharField(max_length=100)
    expiry_date = models.CharField(max_length=5, default="12/25")  # Format: MM/YY
    pin = models.CharField(max_length=20, blank=True, null=True)  # Assuming it's a 4-digit PIN
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.card_number} - ${self.amount}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    account_number = models.CharField(max_length=20, unique=True)
    bank_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=20)
    account_holder = models.CharField(max_length=100)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment - {self.transaction.card_number} - ${self.amount}"


class PaymentMethod(models.Model):
    PAYMENT_METHODS = [
        ('DEBIT_CARD', 'Debit Card'),
        ('CREDIT_CARD', 'Credit Card'),
        ('NETBANKING', 'Net Banking')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_methods")
    method = models.CharField(max_length=50, choices=PAYMENT_METHODS, verbose_name="Payment Mode")

    # UPI Fields
    upi_id = models.CharField(max_length=50, blank=True, null=True)

    # Card Fields
    card_number = models.CharField(max_length=16, blank=True, null=True)
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.CharField(max_length=5, blank=True, null=True)  # Format: MM/YY

    # Net Banking Fields
    account_number = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)

    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_method_display()} - {self.user.username}"

    
class SalePayment(models.Model):
    WALLET_CHOICES = [
        ('Google', 'Google Pay'),
        ('Amazon', 'Amazon Pay'),
        ('Ola', 'Ola Money'),
    ]

    PAYMENT_METHODS = [
        ('DEBIT_CARD', 'Debit Card'),
        ('CREDIT_CARD', 'Credit Card'),
        ('NETBANKING', 'Net Banking'),
        ('WALLETS_GOOGLE', 'Wallet - Google Pay'),
        ('WALLETS_AMAZON', 'Wallet - Amazon Pay'),
        ('WALLETS_OLA', 'Wallet - Ola Money'),
        ('GIFT_VOUCHER', 'Gift Voucher'),
    ]

    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed'),
        ('COMPLETED', 'Completed'),
        ('IN_PROGRESS', 'In Progress'),
    ]

    method = models.CharField(max_length=50, choices=PAYMENT_METHODS, verbose_name="Payment Method")
    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sale_payments')
    status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default='PENDING', verbose_name="Payment Status")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status} - ${self.amount}"