from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.http import HttpRequest
from django.contrib import messages

# Create your views here.

def cart_summary(request):
    cart = Cart
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total
    return render(request, 'cart_summary.html', {"cart_products :" : cart_products, "quantities :" : quantities, "totals :" : totals})

def cart_add(request: HttpRequest):
    #get the cart
    cart = Cart(request)

    #test for POST
    if request.POST.get('action') == 'post':

        #get the product id from the ajax POST request
        
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #Search product into the DB
        product = get_object_or_404(Product, id=product_id)

        #save to the session
        cart.add(product=product, quantity=product_qty)

        #Get cart quantity
        cart_quantity = cart.__len__()

        #return response
        #response = JsonResponse({'Product :' : product.name})
        response = JsonResponse({'qty :' : cart_quantity})
        messages.success(request, ("Your product has been succesfully added to the cart"))
        return response

def cart_delete(request: HttpRequest):
    cart = Cart(request)
    #test for POST
    if request.POST.get('action') == 'post':

        #get the product id from the ajax POST request
        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)
        response = JsonResponse({'qty :' : product_id})
        return response
    

def cart_update(request: HttpRequest):
    cart = Cart(request)
    #test for POST
    if request.POST.get('action') == 'post':

        #get the product id from the ajax POST request
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty :' : product_qty})
        return response
    
