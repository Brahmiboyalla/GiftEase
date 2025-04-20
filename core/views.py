from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import CustomUserCreationForm, GiftCardForm, ReceivePaymentForm, SalePaymentForm, TransactionForm, PaymentMethodForm
from .models import GiftCard, Transaction, Payment, SalePayment

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def base(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def profile(request):
    payments = Payment.objects.filter(user = request.user)
    return render(request, 'profile.html', {'orders': orders, 'payments': payments})

def orders(request):
    user_transactions = Transaction.objects.filter(user=request.user)

    sold_orders = user_transactions.filter(transaction_type='SELL')
    bought_orders = user_transactions.filter(transaction_type='BUY')

    return render(request, 'orders.html', {
        'sold_orders': sold_orders,
        'bought_orders': bought_orders,
    })


def add_payment_method(request):
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.user = request.user  # Associate the payment with the logged-in user
            payment_method.save()
            return redirect('profile')  # Redirect to profile after saving
    else:
        form = PaymentMethodForm()

    return render(request, 'add_payment.html', {'form': form})
from decimal import Decimal

# Define brand margins for profit calculation
BRAND_MARGINS = {
    "Amazon": 5,
    "Flipkart": 4,
    "Myntra": 6,
    "Walmart": 7,
    "Target": 3,
    "eBay": 8,
    "Starbucks": 10,
}

brand_margins = {
    "Amazon": 5,
    "Flipkart": 4,
    "Myntra": 6,
    "Walmart": 7,
    "Target": 3,
    "eBay": 8,
    "Starbucks": 10,
}
def buy_gift_card(request):

    gift_cards = GiftCard.objects.all()

    context = {
        "gift_cards": gift_cards,
        "brand_margins": brand_margins,  # ✅ Pass as a dictionary
    }

    return render(request, "buy_gift_card.html", context)



def buy_gift_card_item(request, card_id, selling_price):
    gift_card = get_object_or_404(GiftCard, id=card_id)
    return render(request, 'sale_payment.html', {'gift_card': gift_card, 'selling_price': selling_price})

def success_page(request):
    return render(request, 'success_page.html')

def sale_success_page(request):
    return render(request, 'payment_success.html')


@login_required
def sell_gift_card(request):    
    gift_form = GiftCardForm()
    transaction_form = None
    payment_form = None
    if request.method == 'POST':
        try:
            # Step 3️⃣: Handle Payment Form Submission
            if 'amount' in request.POST and 'account_number' in request.POST:
                payment_form = ReceivePaymentForm(request.POST)
                last_transaction = Transaction.objects.filter(user=request.user).order_by('-transaction_date').first()
                if payment_form.is_valid():
                    payment = payment_form.save(commit=False)
                    payment.user = request.user

                    # Attach Payment to Last Transaction
                    if last_transaction:
                        payment.transaction = last_transaction
                        payment.save()
                        messages.success(request, "Payment successful! 🎉")

                        send_mail(
                            subject='🎉 Payment Confirmation - GiftCard Platform',
                            message=f"Hi {request.user.name},\n\nYour payment for the gift card has been successfully processed!\n\nTransaction ID: {last_transaction.id}\nAmount: ₹{payment.amount}\n\nThank you for using our platform!\n\n- GiftEase Team",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[request.user.email],
                            fail_silently=False,
                        )

                        return redirect('success_page')
                        # last_transaction.payment_id = payment.id
                        # last_transaction.save(update_fields=['payment_id'])

                    return redirect('dashboard')
                else:
                    messages.error(request, "Error processing the payment. Rolling back...")
                    Transaction.objects.filter(id=last_transaction.id).delete()
                    return redirect('sell_gift_card')
            # Step 2️⃣: Handle Transaction Form Submission
            elif 'card_number' in request.POST:
                transaction_form = TransactionForm(request.POST)
                last_gift_card = GiftCard.objects.filter(seller=request.user).order_by('-created_at').first()

                if transaction_form.is_valid() and last_gift_card:
                    try:
                        transaction = transaction_form.save(commit=False)
                        transaction.transaction_type = 'BUY'
                        transaction.user = request.user
                        transaction.gift_card = last_gift_card
                        transaction.save()

                        last_gift_card.transaction_id = str(transaction.id)
                        last_gift_card.save(update_fields=['transaction_id'])

                        messages.success(request, "Transaction recorded successfully! Proceed to payment.")

                        payment_form = ReceivePaymentForm(initial={'amount': transaction.amount})
                        return render(request, 'sell_gift_card.html', {
                            'form': payment_form,
                            'is_payment': True,
                            'amount': transaction.amount
                        })

                    except Exception as e:
                        # Just in case anything fails mid-way, rollback
                        last_gift_card.delete()
                        messages.error(request, f"Error during transaction. Rolled back. ({e})")
                        return redirect('sell_gift_card')

                else:
                    # Validation or gift card missing
                    if last_gift_card:
                        last_gift_card.delete()
                    messages.error(request, "Form is invalid or gift card missing. Rolled back.")
                    return redirect('sell_gift_card')

            else:
                gift_form = GiftCardForm(request.POST, request.FILES)
                print(gift_form.data)
                if gift_form.is_valid():
                    gift_card = gift_form.save(commit=False)
                    gift_card.seller = request.user  # ✅ Assign the logged-in user before saving

                    # Assign default brand image if no image uploaded
                    if not request.FILES.get('background_image'):
                        brand = request.POST.get('brand', 'default').lower()
                        gift_card.background_image = f"static/images/giftcards/{brand}.png"

                    gift_card.save() 

                    transaction_form = TransactionForm(initial={'amount': gift_card.buy_back_price, 'brand': gift_card.brand})
                    return render(request, 'sell_gift_card.html', {
                        'form': transaction_form,
                        'is_transaction': True,
                        'amount': gift_card.buy_back_price
                    })
                else:
                    messages.error(request, "Error submitting the gift card. Please check your inputs.")
                    return render(request, 'sell_gift_card.html', {'form': gift_form, 'is_transaction': False})    
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}. Rolling back...")
            return redirect('sell_gift_card')
    else:
        gift_form = GiftCardForm()
        return render(request, 'sell_gift_card.html', {'form': gift_form, 'is_transaction': False})
    

def initiate_payment(request, sale_id, selling_price):
    gift_card_sale = get_object_or_404(GiftCard, id=sale_id)
    form = SalePaymentForm(initial={'amount': selling_price})

    if request.method == 'POST':
        form = SalePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.gift_card_sale = gift_card_sale
            payment.amount = selling_price
            payment.status = 'PENDING'
            payment.save()

            messages.success(request, "Payment initiated successfully!")
            return redirect('sale_success')
        else:
            messages.error(request, "Payment failed. Please try again.")
    
    else:
        form = SalePaymentForm(initial={'amount': selling_price})
    
    return render(request, 'sale_payment.html', {'form': form, 'gift_card': gift_card_sale, 'selling_price': selling_price})

@login_required
def get_payment_methods(request, id):
    paymentmodes = Payment.objects.filter(user_id = id)
    return  {
        "paymentmodes": paymentmodes,
        "user_id": id
    }
