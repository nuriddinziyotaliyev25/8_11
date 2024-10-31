from rest_framework.throttling import UserRateThrottle


class TypeThrottle(UserRateThrottle):
    scope = 'type'