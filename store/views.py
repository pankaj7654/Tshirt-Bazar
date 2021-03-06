from django.shortcuts import render, HttpResponse , redirect
from store.forms.authforms import CustomerCreationForm , CustomerAuthForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate , login as loginUser
from store.models import Tshirt , SizeVariant , Cart , Order , OrderItem , Payment , Occasion , Brand , Color , IdealFor , NeckType , Sleeve , Subscribe

from django.contrib.auth.decorators import login_required
from store.forms.checkout_form import CheckoutForm

from django.core.paginator import Paginator
from urllib.parse import urlencode

from math import floor
from django.db.models import Min

from instamojo_wrapper import Instamojo
from Tshirt.settings import API_KEY , AUTH_TOKEN
API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, 
endpoint='https://test.instamojo.com/api/1.1/')

# Create your views here.

def show_product(request,slug):
    tshirt = Tshirt.objects.get(slug=slug)
    size = request.GET.get('size')

    if size is None:
        size_obj = tshirt.sizevariant_set.all().order_by('price').first()
        active_size = None
    else:
        size_obj = tshirt.sizevariant_set.get(size=size)
        active_size = size

    size_price = size_obj.price
    sell_price = size_price - (size_price * (tshirt.descount / 100))
    sell_price = floor(sell_price)
    context = {'tshirt':tshirt  , 'size_price':size_price , 'sell_price':sell_price , 'active_size':active_size }
    return render(request, template_name='store/product_details.html', context=context)




def home(request):
    query = request.GET
    tshirts = []
    tshirts = Tshirt.objects.all()

    brand = query.get('brand')
    neckType = query.get('necktype')
    color = query.get('color')
    idealFor = query.get('idealfor')
    sleeve = query.get('sleeve')

    page = query.get('page')
    if (page is None or page == ''):
        page = 1

    if brand != '' and brand is not None:
        tshirts = tshirts.filter(brand__slug = brand)
        
    if neckType != '' and neckType is not None:
        tshirts = tshirts.filter(neck_type__slug = neckType)

    if color != '' and color is not None:
        tshirts = tshirts.filter(color__slug = color)

    if sleeve != '' and sleeve is not None:
        tshirts = tshirts.filter(sleeve__slug = sleeve)

    if idealFor != '' and idealFor is not None:
        tshirts = tshirts.filter(ideal_for__slug = idealFor)
    



    occasions = Occasion.objects.all()
    brands = Brand.objects.all()
    sleeves = Sleeve.objects.all()
    idealFor = IdealFor.objects.all()
    neckTypes = NeckType.objects.all()
    colors = Color.objects.all()


    cart = request.session.get('cart')

    #paginator
    paginator = Paginator(tshirts , 12)
    page_object = paginator.get_page(page)
    query = request.GET.copy()
    query['page'] = ''
    pageurl = urlencode(query)
    #pagination
    

    context = {
        "page_object" : page_object,
        "occasions" : occasions,
        "brands" : brands,
        "colors" : colors,
        "sleeves" : sleeves,
        "neckTypes" : neckTypes,
        "idealFor" : idealFor,
        "pageurl" : pageurl
        }
    return render(request , template_name='store/home.html', context = context )



def cart(request):
    cart = request.session.get('cart')
    if cart is None:
        cart = []
        
    for c in cart:
        
        tshirt_id = c.get('tshirt')
        tshirt = Tshirt.objects.get(id=tshirt_id)
        c['size'] = SizeVariant.objects.get(tshirt=tshirt_id, size=c['size'])
        c['tshirt'] = tshirt

    return render(request , template_name='store/cart.html', context = {'cart':cart})
    

@login_required(login_url = '/login/')
def order(request):
    user = request.user
    orders = Order.objects.filter(user = user).order_by('-date').exclude(order_status='PENDING')
    context = {
        "order" : orders
    }
    return render(request , template_name='store/order.html' , context = context )



def login(request):
    if(request.method == 'GET'):
        form = CustomerAuthForm()
        next_page = request.GET.get('next')
        if next_page is not None:
            request.session['next_page'] = next_page
        return render(request , template_name='store/login.html', context={"form":form})
    
    else:
        form = CustomerAuthForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password )
            if user:
                loginUser(request , user)

                session_cart = request.session.get('cart')
                if session_cart is None:
                    session_cart = []
                else:
                    for c in session_cart:
                        size = c.get('size')
                        tshirt_id = c.get('tshirt')
                        quantity = c.get('quantity')
                        cart_obj = Cart()
                        cart_obj.sizeVariant = SizeVariant.objects.get(size = size , tshirt = tshirt_id)
                        cart_obj.quantity = quantity
                        cart_obj.user = user
                        cart_obj.save()
        

                cart = Cart.objects.filter(user = user)
                print(cart," cart of user ",user)
                session_cart = []
                for c in cart:
                    obj = {
                        'size' : c.sizeVariant.size,
                        'tshirt' : c.sizeVariant.tshirt.id,
                        'quantity' : c.quantity
                    }
                    session_cart.append(obj)
            
                request.session['cart'] = session_cart
                next_page = request.session.get('next_page')
                if next_page is None:
                    next_page = 'homepage'
                return redirect(next_page)
        else:
            return render(request , template_name='store/login.html', context={"form":form})
        
        



def signup(request):
    if(request.method == 'GET'):
        form = CustomerCreationForm()
        context = {
            "form": form
            }
        return render(request , template_name='store/signup.html', context=context)
    
    else:
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            print(user)
            return redirect('login')
           
        context = {
            "form": form
            }
        return render(request , template_name='store/signup.html', context=context)



def logout(request):
    request.session.clear()
    #otherwire we can user here inbuilt method "logout(request)" after import "logout" in the top
    return redirect('homepage')



def add_to_cart(request , slug , active_size):
    user = None
    if request.user.is_authenticated:
        user = request.user
        
    cart = request.session.get('cart')
    if cart is None:
        cart = []
    
    tshirt = Tshirt.objects.get(slug=slug)
    add_cart_for_anom_user(cart , active_size , tshirt)
    
    if user is not None:
        add_cart_to_database(user , active_size , tshirt)
        

    request.session['cart'] = cart
    return_url = request.GET.get('return_url')
    return redirect(return_url)

#when user is login
def add_cart_to_database(user , active_size , tshirt):
    size = SizeVariant.objects.get(size = active_size , tshirt = tshirt)
    existing = Cart.objects.filter(user = user, sizeVariant = size)

    if len(existing) > 0:
        obj = existing[0]
        obj.quantity = obj.quantity+1
        obj.save()

    else:
        c = Cart()
        c.user = user
        c.sizeVariant = size
        c.quantity = 1
        c.save()


#when user is not login
def add_cart_for_anom_user(cart , active_size , tshirt):
    flag = True
    for cart_obj in cart:
        t_id = cart_obj.get('tshirt')
        size_short = cart_obj.get('size')
        if t_id == tshirt.id and  active_size == size_short:
            flag = False
            cart_obj['quantity'] = cart_obj['quantity']+1
        
    if flag:
        cart_obj = {
            'tshirt':tshirt.id,
            'size':active_size,
            'quantity':1
        }
        cart.append(cart_obj)


#utility
def cal_total_payable_amount(cart):
    total = 0
    for c in cart:
        descount = c.get('tshirt').descount
        price = c.get('size').price
        sale_price = floor(price - (price * ( descount / 100)))
        total_of_single_product = sale_price * c.get('quantity')
        total = total + total_of_single_product

    return total


@login_required(login_url = '/login/')
def checkout(request):
    #get request
    if request.method == 'GET':
        form = CheckoutForm()
        cart = request.session.get('cart')
        if cart is None:
            cart = []
        for c in cart:
            size_str = c.get('size')
            tshirt_id = c.get('tshirt')
            size_obj = SizeVariant.objects.get(size=size_str, tshirt=tshirt_id)
            c['size'] = size_obj
            c['tshirt'] = size_obj.tshirt

        return render(request,'store/checkout.html', {"form":form , "cart":cart})
    else:
        #post request
        form = CheckoutForm(request.POST)
        if request.user.is_authenticated:
            user = request.user
        if form.is_valid():
            #payment
            cart = request.session.get('cart')
            if cart is None:
                cart = []
            for c in cart:
                size_str = c.get('size')
                tshirt_id = c.get('tshirt')
                size_obj = SizeVariant.objects.get(size=size_str, tshirt=tshirt_id)
                c['size'] = size_obj
                c['tshirt'] = size_obj.tshirt

            shipping_address = form.cleaned_data.get('shipping_address')
            phone = form.cleaned_data.get('phone')
            payment_method = form.cleaned_data.get('payment_method')
            total = cal_total_payable_amount(cart)
            print(shipping_address , phone , payment_method , total)
            
            order = Order()
            print("EEEEEEEEEEEEEEEEEEEEEEE")
            order.shipping_address = shipping_address
            order.phone = phone
            order.payment_method = payment_method
            order.total = total
            order.order_status = "PENDING"
            order.user = user
            order.save()
            
            #saving order Item
            for c in cart:
                order_item = OrderItem()
                order_item.order = order
                size = c.get('size')
                tshirt = c.get('tshirt')
                order_item.price = floor(size.price - (size.price * (tshirt.descount / 100)))
                order_item.quantity = c.get('quantity')
                order_item.size = size
                order_item.tshirt = tshirt
                order_item.save()

            #Creating payment
            response = API.payment_request_create(
            amount=order.total,
            purpose="Payment for Tshirts",
            send_email=True,
            buyer_name = f'{user.first_name} {user.last_name}',
            email=user.email,
            redirect_url="http://localhost:8000/validate_payment"
            )

            #print(response['payment_request'],['id'])
            payment_request_id = response['payment_request']['id']
            url = response['payment_request']['longurl']

            payment = Payment()
            payment.order = order
            payment.payment_request_id = payment_request_id
            payment.save()
            return redirect(url)
        else:
            return redirect('/checkout/')






# Buy Now product
@login_required(login_url = '/login/')
def buynow(request):
    #get request
    if request.method == 'GET':
        form = CheckoutForm()
        print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQq")
        return render(request,'store/checkout.html', {'form' : form})
    else:
        # post request
        pass





# Check Payment Validation
def validatePayment(request):
    user = None
    if request.user.is_authenticated:
       user = request.user 
    payment_request_id = request.GET.get('payment_request_id')
    payment_id = request.GET.get('payment_id')
    print(payment_id, payment_request_id)
    response = API.payment_request_payment_status(payment_request_id , payment_id)
    status = response.get('payment_request').get('payment').get('status')  


    if status != "Failed":
        print('Payment Success')
        try:
            payment = Payment.objects.get(payment_request_id=payment_request_id)
            payment.payment_id = payment_id
            payment.payment_status = status
            payment.save()

            order = payment.order
            order.order_status = 'PLACED'
            order.save()
            
            cart = []
            request.session['cart'] = cart

            Cart.objects.filter(user = user).delete()

            return redirect('order')
        except:
            return render(request , 'store/payment_failed.html')

    else:
        return render(request , 'store/payment_failed.html')
        #return error page




def subscribe(request):
    email = request.POST.get('email')
    if email:
        email = Subscribe(email=email)
        result = email.save()
        return redirect('homepage')
    else:
        return redirect('homepage')