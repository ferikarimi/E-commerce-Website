from django.core.cache import cache
from django.http import HttpResponse



RATE_LIMIT = 3
TIME_WINDOW = 60

def rate_limit(view_function):
    def wrapper(self , *args , **kwargs):
        ip = self.request.META.get('REMOTE_ADDR')
        request_count = cache.get(ip , 0)
        if request_count >= RATE_LIMIT :
            return HttpResponse('too many atempt. try again after 1 minute.')
        if request_count == 0 :
            cache.set(ip , 1 ,TIME_WINDOW)
        cache.incr(ip)
        return view_function(self , *args , **kwargs)
    return wrapper