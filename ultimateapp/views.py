from django.shortcuts import render,redirect
from .models import webpagedata,androidData,SmartHomeProduct,Property
from .forms import SmartHomeProductForm,PropertyForm
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Payment,Contact

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request):
    if request.method == "POST":
        amount = int(request.POST.get("amount", 100))  # Convert to cents

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=[
                    "card",  # Supports Visa, MasterCard, etc.
                    "apple_pay",
                    "google_pay",
                    "alipay",
                    "link",
                    "wechat_pay",
                ],
                customer_email=request.user.email,
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": "Django Payment"},
                            "unit_amount": amount * 100,  # Convert dollars to cents
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url="http://127.0.0.1:8000/payment/success/?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://127.0.0.1:8000/payment/cancel/",
            )

            # Save payment record
            Payment.objects.create(
                user=request.user,
                amount=amount,
                stripe_session_id=session.id,
                status="Pending"
            )

            return JsonResponse({"id": session.id})

        except Exception as e:
            return JsonResponse({"error": str(e)})

def PaymentPageView(request):
    return render(request,'payments/payments.html')


# Create your views here.
def home(request):

    return render(request,'home.html')
def webpage(request):
    if request.method == 'POST':
        web_name = request.POST.get('name')
        web_email = request.POST.get('email')
        web_phone =request.POST.get('number')
        web_message = request.POST.get('message')
        web = webpagedata(web_name=web_name,web_email=web_email,web_phone=web_phone,web_message=web_message)
        web.save()
    return render(request,'webpage.html')
def android(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        ANDROID = androidData(name=name,email=email,phone=phone,message=message)
        ANDROID.save()
    return render(request,'android.html')
def photo(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        Contact.objects.create(name=name, email=email, message=message)
        return redirect('home')

    return render(request,'photopage.html')
def videoediting(request):
    return render(request,'videoediting.html')
def local(request):
    return render(request,'local.html')
#electric work repare
def repair(request):
    return render(request,'ele_repair.html')
def smart_home_view(request):
    switches = SmartHomeProduct.objects.filter(category='switch')
    sensors = SmartHomeProduct.objects.filter(category='sensor')
    modules = SmartHomeProduct.objects.filter(category='module')
    others = SmartHomeProduct.objects.filter(category='other')

    return render(request, 'smarthome.html', {
        'switches': switches,
        'sensors': sensors,
        'modules': modules,
        'others': others
    })





@staff_member_required
def add_product_view(request):
    if request.method == "POST":
        form = SmartHomeProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('smarthome')
    else:
        form = SmartHomeProductForm()
    
    return render(request, 'adding_smartproducts.html', {'form': form})

def contact(request):
    return render(request,'contact.html')

def rentalhome(request):
     if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Refresh after submission

     else:
        form = PropertyForm()

     properties = Property.objects.all()
     return render(request, 'rentalhome.html', {'properties': properties, 'form': form})

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'property_detail.html', {'property': property_obj})



def car_home_page(request):
    return render(request, 'carrental/index.html')




#car rental
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from .models import CarDealer
from .models import Vehicles
from .models import Area
from .models import Customer
from .models import Orders
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'carrental/index.html')
    else:
        return render(request, 'car_dealer/home_page.html')

def car_dealer_login(request):
    return render(request, 'car_dealer/login.html')


def auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'car_dealer/home_page.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            car_dealer = CarDealer.objects.get(car_dealer = user)
        except:
            car_dealer = None
        if car_dealer is not None:
            auth.login(request, user)
            return render(request, 'car_dealer/home_page.html')
        else:
            return render(request, 'car_dealer/login_failed.html')

def logout_view(request):
    auth.logout(request)
    return render(request, 'car_dealer/login.html')

def register(request):
    return render(request, 'car_dealer/register.html')

def registration(request):
    username = request.POST['username']
    password = request.POST['password']
    mobile = request.POST['mobile']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']

    try:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    except:
        return render(request, 'car_dealer/registration_error.html')
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        car_dealer = CarDealer(car_dealer = user, mobile = mobile, area=area)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        car_dealer = CarDealer(car_dealer = user, mobile = mobile, area=area)
    car_dealer.save()
    return render(request, 'car_dealer/registered.html')

@login_required
def add_vehicle(request):
    car_name = request.POST['car_name']
    color = request.POST['color']
    cd = CarDealer.objects.get(car_dealer=request.user)
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']
    description = request.POST['description']
    capacity = request.POST['capacity']
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        car = Vehicles(car_name=car_name, color=color, dealer=cd, area = area, description = description, capacity=capacity)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        car = Vehicles(car_name=car_name, color=color, dealer=cd, area = area,description=description, capacity=capacity)
    car.save()
    return render(request, 'car_dealer/vehicle_added.html')

@login_required
def manage_vehicles(request):
    username = request.user
    user = User.objects.get(username = username)
    car_dealer = CarDealer.objects.get(car_dealer = user)
    vehicle_list = []
    vehicles = Vehicles.objects.filter(dealer = car_dealer)
    for v in vehicles:
        vehicle_list.append(v)
    return render(request, 'car_dealer/manage.html', {'vehicle_list':vehicle_list})

@login_required
def order_list(request):
    username = request.user
    user = User.objects.get(username = username)
    car_dealer = CarDealer.objects.get(car_dealer = user)
    orders = Orders.objects.filter(car_dealer = car_dealer)
    order_list = []
    for o in orders:
        if o.is_complete == False:
            order_list.append(o)
    return render(request, 'car_dealer/order_list.html', {'order_list':order_list})

@login_required
def complete(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    vehicle = order.vehicle
    order.is_complete = True
    order.save()
    vehicle.is_available = True
    vehicle.save()
    return HttpResponseRedirect('/car_dealer_portal/order_list/')


@login_required
def history(request):
    user = User.objects.get(username = request.user)
    car_dealer = CarDealer.objects.get(car_dealer = user)
    orders = Orders.objects.filter(car_dealer = car_dealer)
    order_list = []
    for o in orders:
        order_list.append(o)
    return render(request, 'car_dealer/history.html', {'wallet':car_dealer.wallet, 'order_list':order_list})

@login_required
def delete(request):
    veh_id = request.POST['id']
    vehicle = Vehicles.objects.get(id = veh_id)
    vehicle.delete()
    return HttpResponseRedirect('/car_dealer_portal/manage_vehicles/')



# Create your views here.customer

def customer_index(request):
    if not request.user.is_authenticated:
        return render(request, 'customer/login.html')
    else:
        return render(request, 'customer/home_page.html')

def login(request):
    return render(request, 'customer/login.html')

def Customer_auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'customer/home_page.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            customer = Customer.objects.get(user = user)
        except:
            customer = None
        if customer is not None:
            auth.login(request, user)
            return render(request, 'customer/home_page.html')
        else:
            return render(request, 'customer/login_failed.html')

def logout_view(request):
    auth.logout(request)
    return render(request, 'customer/login.html')

def register(request):
    return render(request, 'customer/register.html')

def registration(request):
    username = request.POST['username']
    password = request.POST['password']
    mobile = request.POST['mobile']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']
    try:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    except:
        return render(request, 'customer/registration_error.html')
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        customer = Customer(user = user, mobile = mobile, area = area)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        customer = Customer(user = user, mobile = mobile, area = area)

    customer.save()
    return render(request, 'customer/registered.html')

@login_required
def search(request):
    return render(request, 'customer/search.html')

@login_required
def search_results(request):
    city = request.POST['city']
    city = city.lower()
    vehicles_list = []
    area = Area.objects.filter(city = city)
    for a in area:
        vehicles = Vehicles.objects.filter(area = a)
        for car in vehicles:
            if car.is_available == True:
                vehicle_dictionary = {'name':car.car_name, 'color':car.color, 'id':car.id, 'pincode':car.area.pincode, 'capacity':car.capacity, 'description':car.description}
                vehicles_list.append(vehicle_dictionary)
    request.session['vehicles_list'] = vehicles_list
    return render(request, 'customer/search_results.html')


@login_required
def rent_vehicle(request):
    id = request.POST['id']
    vehicle = Vehicles.objects.get(id = id)
    cost_per_day = int(vehicle.capacity)*13
    return render(request, 'customer/confirmation.html', {'vehicle':vehicle, 'cost_per_day':cost_per_day})

@login_required
def confirm(request):
    vehicle_id = request.POST['id']
    username = request.user
    user = User.objects.get(username = username)
    days = request.POST['days']
    vehicle = Vehicles.objects.get(id = vehicle_id)
    if vehicle.is_available:
        car_dealer = vehicle.dealer
        rent = (int(vehicle.capacity))*13*(int(days))
        car_dealer.wallet += rent
        car_dealer.save()
        try:
            order = Orders(vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days)
            order.save()
        except:
            order = Orders.objects.get(vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days)
        vehicle.is_available = False
        vehicle.save()
        return render(request, 'customer/confirmed.html', {'order':order})
    else:
        return render(request, 'customer/order_failed.html')

@login_required
def manage(request):
    order_list = []
    user = User.objects.get(username = request.user)
    try:
        orders = Orders.objects.filter(user = user)
    except:
        orders = None
    if orders is not None:
        for o in orders:
            if o.is_complete == False:
                order_dictionary = {'id':o.id,'rent':o.rent, 'vehicle':o.vehicle, 'days':o.days, 'car_dealer':o.car_dealer}
                order_list.append(order_dictionary)
    return render(request, 'customer/manage.html', {'od':order_list})

@login_required
def update_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    vehicle = order.vehicle
    vehicle.is_available = True
    vehicle.save()
    car_dealer = order.car_dealer
    car_dealer.wallet -= int(order.rent)
    car_dealer.save()
    order.delete()
    cost_per_day = int(vehicle.capacity)*13
    return render(request, 'customer/confirmation.html', {'vehicle':vehicle}, {'cost_per_day':cost_per_day})

@login_required
def delete_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    car_dealer = order.car_dealer
    car_dealer.wallet -= int(order.rent)
    car_dealer.save()
    vehicle = order.vehicle
    vehicle.is_available = True
    vehicle.save()
    order.delete()
    return HttpResponseRedirect('/customer_portal/manage/')

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *

@login_required
def custom_admin_dashboard(request):
    model_list = [
        ('Web Page Data', webpagedata),
        ('Android Data', androidData),
        ('Smart Products', SmartHomeProduct),
        ('Properties', Property),
        ('Payments', Payment),
        ('Areas', Area),
        ('Car Dealers', CarDealer),
        ('Vehicles', Vehicles),
        ('Customers', Customer),
        ('Orders', Orders),
        ('Contact Messages', Contact)
    ]

    tables = []
    for title, model in model_list:
        fields = [field.name for field in model._meta.fields]
        data = model.objects.all()
        tables.append({
            "title": title,
            "fields": fields,
            "data": data,
        })

    return render(request, "custom_admin_dashboard.html", {"tables": tables})

