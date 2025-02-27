from django.shortcuts import render , redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingAddress
from payment.models import ShippingAddress
from django.http import HttpRequest
from django.db.models import Q
import json
from cart.cart import Cart

def search(request:HttpRequest):
    if request.method == "POST":
        searched = request.POST['searched']
        #Search the product in the db
        searched = Product.objects.filter(Q(name__icontains = searched) | Q(description__icontains = searched))
        if not searched:
            messages.success(request, "That product does not exist")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request:HttpRequest):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #cart login persistance
            current_user = Profile.objects.get(user__id = request.user.id)
            #fetch saved cart
            saved_cart = current_user.old_cart
            #convert db str to py dict
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                #Get the cart and the loaded cart to the db
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ("You have been logged in"))
            return redirect('home')
        else:
            messages.success(request, ("An occured while trying to log you in"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')

def register_user(request:HttpRequest):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            #log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been registered successfully, Welcome !"))
            return redirect('home')
        else:
            messages.success(request, ("Unable to register you due to an error occured"))
            return redirect('register.html')
    else:
        return render(request, 'register.html', {'form': form})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})    

def category(request, foo):
    foo = foo.replace("-", "")
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("That category doesnt exist"))

def update_user(request:HttpRequest):
    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance = current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User has been updated")
            return redirect('home')
        return render(request, 'update_user.html', {"user_form" : user_form})
    else:
        messages.success(request, "You must have been logged in, to acccess this page")
        return redirect()
    
def update_password(request: HttpRequest):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            #
            form = ChangePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated, please log in again')
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else :
            form = ChangePasswordForm(current_user)
        return render(request, 'update_password.html', {"form" : form})
    else:
        messages.success(request, 'You must be logged in to see this page')
        return redirect('home')

def update_info(request:HttpRequest):
    if request.user.is_authenticated:
        #Get current user
        current_user = Profile.objects.get(user__id = request.user.id)
        #Get current user shipping info
        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
        form =UserInfoForm(request.POST or None, instance = current_user)
        #Get user shipping form
        shipping_form = shipping_form(request.POST or None, isinstance = shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your Infos has been updated")
            return redirect('home')
        return render(request, 'update_info.html', {"form" : form, "shipping_form":shipping_form})
    else:
        messages.success(request, "You must have been logged in, to acccess this page")
        return redirect()                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          