from rest_framework.throttling import UserRateThrottle

class MyCustomThrottle(UserRateThrottle):
    rate = '3/minute' # Limit to 3 requests per minute