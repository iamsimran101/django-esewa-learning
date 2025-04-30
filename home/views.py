from django.shortcuts import render,get_object_or_404,redirect
from esewa import EsewaPayment
from .models import Product, Transaction
import uuid 


def index(request):
    products = Product.objects.all()
    context={
        'products': products
        }
    return render(request, 'index.html',context)

def buy(request, id):
    product = get_object_or_404(Product, id=id)
    uid = uuid.uuid4()
    transaction = Transaction.objects.create(
        product=product,
        transaction_uuid=str(uid),
        transaction_amount=product.price,
        transaction_status='pending'
    )
    epayment = EsewaPayment(
        product_code="EPAYTEST",
        success_url=f'http://localhost:8000/success/{transaction.id}/',
        failure_url=f'http://localhost:8000/failure/{transaction.id}/',
        secret_key='8gBm/:&EnhH.1/q',
    )
    epayment.create_signature(
        total_amount=product.price,
        transaction_uuid= transaction.transaction_uuid 
    )
    context = {
        'product': product,
        'form':epayment.generate_form(),
    }
    return render(request, 'buy.html',context )  

def success(request, id):
    transaction = Transaction.objects.get(id=id)
    epayment = EsewaPayment(
        product_code="EPAYTEST",
        success_url=f'http://localhost:8000/success/{transaction.id}/',
        failure_url=f'http://localhost:8000/failure/{transaction.id}/',
        secret_key='8gBm/:&EnhH.1/q',
    )
    epayment.create_signature(
        total_amount=transaction.product.price,
        transaction_uuid= transaction.transaction_uuid 
    )
    if epayment.is_completed(True):     
        transaction.transaction_status = 'completed'
        transaction.save()
        return render(request, 'success.html')
    else:
        return redirect('failure', id=transaction.id)

def failure(request, id):
    transaction = Transaction.objects.get(id=id)
    transaction.transaction_status = 'failed' 
    transaction.save()  
    return render(request, 'failure.html') 