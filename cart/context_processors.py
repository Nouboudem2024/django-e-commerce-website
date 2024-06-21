from .cart import Cart

#Create context processor so our cart can work everywhere
def cart(request):
    return {'cart': Cart(request)} #Return default data from our cart