"""Ultimate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ultimateapp import urls
from ultimateapp import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('webpage/',views.webpage,name='webpage'),
    path('andriod/',views.android,name='android'),
    path('photo/',views.photo,name='photoediting'),
    path('video/',views.videoediting,name='videoediting'),
    path('local/',views.local,name='local'),
    path('repair/',views.repair,name='repair'),
    path('smarthome/',views.smart_home_view,name='smarthome'),
    path('addproductsele/',views.add_product_view,name='add_product'),
    path('contact/',views.contact,name='contact'),
    path('rentalhome/', views.rentalhome, name='rentalhome'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('payment/', views.login_required(views.PaymentPageView), name='payment-page'),
    path('create-checkout-session/',views.create_checkout_session, name='create-checkout-session'),
    
    #car_rental
    path('car_rental/',views.car_home_page,name='car_rent'),
    path('index/', views.index, name='index'),
    path('car_dealer_portal/login/', views.car_dealer_login, name='car_dealer_portal/login/'),
    path('car_dealer_portal/auth/', views.auth_view, name='car_dealer_auth'),
    path('car_dealer_portal/logout/', views.logout_view, name='car_dealer_logout'),
    path('car_dealer_portal/register/', views.register, name='car_dealer_register'),
    path('car_dealer_portal/registration/', views.registration, name='car_dealer_registration'),
    path('car_dealer_portal/add_vehicle/', views.add_vehicle, name='car_dealer_portal/add_vehicle'),
    path('car_dealer_portal/manage_vehicles/', views.manage_vehicles, name='car_dealer_manage_vehicles'),
    path('car_dealer_portal/order_list/', views.order_list, name='car_dealer_order_list'),   
    path('car_dealer_portal/complete/', views.complete, name='car_dealer_complete'),
    path('car_dealer_portal/history/', views.history, name='car_dealer_portal/history'),
    path('car_dealer_portal/delete/', views.delete, name='car_dealer_delete'),
    
    path('customer_portal/index/', views.customer_index, name='customer_index'),
    path('customer_portal/login/', views.login, name='login'),
    path('customer_portal/auth/', views.Customer_auth_view, name='auth'),
    path('customer_portal/logout/', views.logout_view, name='logout'),
    path('customer_portal/register/', views.register, name='register'),
    path('customer_portal/registration/', views.registration, name='registration'),
    path('customer_portal/search/', views.search, name='search'),
    path('customer_portal/search_results/', views.search_results, name='search_results'),
    path('customer_portal/rent/', views.rent_vehicle, name='rent_vehicle'),
    path('customer_portal/confirmed/', views.confirm, name='confirm'),
    path('customer_portal/manage/', views.manage, name='manage'),
    path('customer_portal/update/', views.update_order, name='update_order'),
    path('customer_portal/delete/', views.delete_order, name='delete_order'),
     path("admin-dashboard/", views.custom_admin_dashboard, name="custom_admin_dashboard"),
    
    ]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)