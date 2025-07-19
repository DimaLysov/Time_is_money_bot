from django.urls import path, include
from rest_framework import routers

from api.viewsets.user import UserViewSet
from api.viewsets.notice import NoticeViewSet
from api.viewsets.payment import PaymentViewSet
from api.viewsets.event import EventViewSet


router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'notice', NoticeViewSet)
router.register(r'payment', PaymentViewSet)
router.register(r'event', EventViewSet)


urlpatterns = [
    path('', include(router.urls)),
]