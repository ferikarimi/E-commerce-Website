from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Vendors



class IsVendorOrManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated :
            return False
        try :
            vendor = Vendors.objects.get(user=request.user)
            return vendor.role in ['owner','manager']
        except Vendors.DoesNotExist :
            return False


class IsVendorOwner (permissions.BasePermission):
    def has_permission(self, request, view):
        try :
            return request.user.is_authenticated and Vendors.objects.get(user=request.user).role == 'owner'
        except Vendors.DoesNotExist :
            return False


class IsVendorManager (permissions.BasePermission):
    def has_permission(self, request, view):
        try :
            return request.user.is_authenticated and Vendors.objects.get(user=request.user).role == 'manager'
        except Vendors.DoesNotExist :
            return False


class IsVendorOperator (permissions.BasePermission):
    def has_permission(self, request, view):
        try :
            return request.user.is_authenticated and Vendors.objects.get(user=request.user).role == 'operator'
        except Vendors.DoesNotExist :
            return False


class IsAuthenticatedVendor (BasePermission) :
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_vendor   