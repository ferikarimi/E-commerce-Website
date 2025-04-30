from django.shortcuts import render 




#_____________________________________ OTP __________________________________

# from django.http import HttpResponseBadRequest
# from .urls import create_token_view
# from .tasks import send_otp_code
# from .redis_setup import client

# def otp_generation_view (request):
#     if request.method == 'POST':
#         otp_token = request.POST.get('otp_token')
#         valid_token = client.hget("token","token")
#         str_valid_token = valid_token.decode('utf-8')
#         if otp_token == str_valid_token :
#             response = redirect("home")
#             token = create_token_view("sample")
#             print(token)
#             response.set_cockie("token", token , max_age=300)
#             return response
#         else:
#             return HttpResponseBadRequest("invalid OTP")
#     return render (request , "registration/otp_generatecode.html")