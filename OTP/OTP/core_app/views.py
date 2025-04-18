from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def show_otp_view (request,code):
    print(code)
    return HttpResponse (f"code:{code}")