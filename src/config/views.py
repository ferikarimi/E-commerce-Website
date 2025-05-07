from django.shortcuts import render



# _________________________________ user panel _________________________________
def user_panel(request):
    return render(request,'panels/user_panel/user_panel.html')
def user_comments (request):
    return render (request , 'panels/user_panel/comments.html')
def user_addresses (request):
    return render(request , 'panels/user_panel/user_address.html')
def user_profile_page (request):
    return render (request , 'panels/user_panel/profile.html')
def user_order (request):
    return render (request , 'panels/user_panel/user_order.html')
def user_order_detail (request ,pk):
    return render (request , 'panels/user_panel/user_order_detail.html' , context={'pk':pk})
def product_rating (request):
    return render (request , 'panels/user_panel/product_rating.html')
#_______________________________________________________________________________

#_________________________________ vendor panel ________________________________
def vendor_panel(request):
    return render(request , 'panels/vendor_panel/vendor_panel.html')
def vendor_profile_page (request):
    return render (request , 'panels/vendor_panel/vendor_profile.html')
def edit_shop (request):
    return render (request , 'panels/vendor_panel/vendor_shop.html')
def register_operator_or_manager(request):
    return render (request , 'panels/vendor_panel/operator_manager.html')
def vendor_order (request):
    return render (request , 'panels/vendor_panel/vendor_order.html')
def manage_comments (request):
    return render (request , 'panels/vendor_panel/manage_comments.html')
def operator_panel(request):
    return render (request , 'panels/vendor_panel/operator_panel.html')
def manager_panel(request):
    return render (request , 'panels/vendor_panel/manager_panel.html')
#______________________________________________________________________________

#_________________________________ registration _______________________________
def register_page(request):
    return render(request , 'registration/register.html')
def register_vendor_page(request):
    return render(request , 'registration/become_vendor.html')
def login_page(request):
    return render(request , 'registration/login.html')
def verify_otp(request):
    return render(request , 'registration/verify_otp.html')
#______________________________________________________________________________

#_________________________________ admin panel _________________________________
def admin_panel(request):
    return render (request , 'panels/admin_panel/admin_panel.html')
def admin_profile(request):
    return render (request , 'panels/admin_panel/profile.html')
def add_vendor_code(request):
    return render (request , 'panels/admin_panel/add_vendor_code.html')
def vendor_code(request):
    return render (request , 'panels/admin_panel/vendor_code.html')
#_______________________________________________________________________________

#___________________________________ product ___________________________________
def all_product (request):
    return render (request , 'product/all_product.html')
def add_product(request):
    return render (request , 'product/add_product.html')
def vendor_product (request) :
    return render (request , 'product/vendor_product.html')
def edit_product (request , pk):
    return render (request , 'product/edit_product.html' , context={'pk':pk})
def single_product_page(request, pk):
    return render (request , 'product/single_product.html' , context={'pk':pk})
#______________________________________________________________________________

#____________________________________ base ____________________________________
def home_page(request):
    return render(request , 'home.html')
def shop_page (request , pk):
    return render(request , 'shop/single_shop.html' , context={'pk':pk})
def all_shop (request):
    return render(request , 'shop/all_shop.html')
#______________________________________________________________________________

#___________________________________ cart _____________________________________
def cart (request):
    return render (request , 'cart.html')
def checkout (request):
    return render (request , 'checkout.html')
def thankyou(request):
    return render (request , 'thankyou.html')
#______________________________________________________________________________