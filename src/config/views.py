from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required

@login_required
def user_panel(request):
    if request.user.is_vendor :
        return redirect ('vendor_panel')
    return render(request,'user_panel/user_panel.html')

def user_reviews (request):
    return render (request , 'user_panel/reviews.html')

def user_addresses (request):
    return render(request , 'user_panel/user_address.html')
def user_profile_page (request):
    return render (request , 'user_panel/profile.html')

@login_required
def vendor_panel(request):
    if not request.user.is_vendor :
        return redirect ('user_panel')
    return render(request , 'vendor_panel/vendor_panel.html')


def vendor_profile_page (request):
    return render (request , 'vendor_panel/vendor_profile.html')

def register_page(request):
    return render(request , 'register.html')
def register_vendor_page(request):
    return render(request , 'become_vendor.html')
def login_page(request):
    return render(request , 'login.html')

# @login_required

def home_page(request):
    return render(request , 'home.html')



def store_page (request):
    return render(request , 'store.html')


def add_product(request):
    return render (request , 'product/add_product.html')

def vendor_product (request) :
    return render (request , 'product/vendor_product.html')

def edit_product (request , pk):
    return render (request , 'product/edit_product.html' , context={'pk':pk})


def edit_shop (request):
    return render (request , 'vendor_panel/vendor_shop.html')


def all_product (request):
    return render (request , 'product/all_product.html')