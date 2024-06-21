from store.models import Product, Profile
from django.http import HttpRequest

class Cart():
    
    def __init__(self, request:HttpRequest):
        self.session = request.session
        #Get request
        self.request = request

        #get the current session key if it exists
        cart = self.session.get('session_key')

        #if the user is new then no session key, create one !
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make sure cart is available in all pages of site
        self.cart = cart
    
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else :
            #self.cart[product_id] = {'price' : str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        #user logged in
        if self.request.user.is_authenticated:
            #Get current user
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert cart to string to store in db
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #Save cart
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else :
            #self.cart[product_id] = {'price' : str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        #user logged cart items in
        if self.request.user.is_authenticated:
            #Get current user
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert cart to string to store in db
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #Save cart
            current_user.update(old_cart=str(carty))
    
    def cart_total(self):
        #get products ids
        product_ids = self.cart.keys()
        #search product in our product db model
        products = Product.objects.filter(id__in=product_ids)
        #get quantity
        quantities = self.cart
        #counting
        total = 0
        for key, value in quantities.items:
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total= total + (product.price * value)
        return total

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys()
        #use ids to search products in db
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity) 
        #update cart
        ourcart = self.cart
        ourcart[product_id] = product_qty

        self.session.modified = True
         #user logged in
        if self.request.user.is_authenticated:
            #Get current user
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert cart to string to store in db
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #Save cart
            current_user.update(old_cart=str(carty))
            
        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
         #user logged in
        if self.request.user.is_authenticated:
            #Get current user
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #convert cart to string to store in db
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #Save cart
            current_user.update(old_cart=str(carty))
