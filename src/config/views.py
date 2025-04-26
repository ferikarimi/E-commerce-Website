from django.shortcuts import render


# user panel
def user_panel(request):
    return render(request,'panels/user_panel/user_panel.html')
def user_reviews (request):
    return render (request , 'panels/user_panel/reviews.html')
def user_addresses (request):
    return render(request , 'panels/user_panel/user_address.html')
def user_profile_page (request):
    return render (request , 'panels/user_panel/profile.html')


# vendor panel
def vendor_panel(request):
    return render(request , 'panels/vendor_panel/vendor_panel.html')


# admin panel
def admin_panel(request):
    return render (request , 'panels/admin_panel/admin_panel.html')


# registration
def register_page(request):
    return render(request , 'registration/register.html')

def register_vendor_page(request):
    return render(request , 'registration/become_vendor.html')

def login_page(request):
    return render(request , 'registration/login.html')








def vendor_profile_page (request):
    return render (request , 'vendor_panel/vendor_profile.html')



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